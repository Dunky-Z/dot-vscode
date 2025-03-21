import subprocess
import re
import argparse
import os
import logging

def convert_pci_bdf_to_decimal(pci_bdf):
    """
    Converts a PCI BDF (Bus:Device.Function) string to a decimal number.
    Args:
        pci_bdf (str): The PCI BDF string (e.g., "0000:01:00.0" or "01:00.0").
    Returns:
        int: The decimal representation of the BDF, or None if parsing fails.
    """
    if not pci_bdf:
        return None
    # Regular expression to match PCI BDF with optional domain
    pattern = r'^([0-9a-fA-F]{4}:)?([0-9a-fA-F]{2}):([0-9a-fA-F]{2})\.([0-9a-fA-F])$'
    match = re.match(pattern, pci_bdf)
    if not match:
        return None
    # Extract bus, device, function
    bus = match.group(2).lower()
    device = match.group(3).lower()
    function = match.group(4).lower().zfill(2)  # Pad function to two digits
    # Combine into a six-digit hex string
    combined_hex = bus + device + function
    try:
        decimal = int(combined_hex, 16)
    except ValueError:
        return None
    return decimal

def bus_location_to_bdf(bus_location):
    """
    Convert Bus Location To PCI BDF 
    For example, "1_0_0" -> "01:00.0"
    """
    try:
        logging.debug(f"bus_location: {bus_location}")
        parts = list(map(int, bus_location.split('_')))
        if len(parts) != 3:
            return None
        return f"{parts[0]:02x}:{parts[1]:02x}.{parts[2]}"
    except (ValueError, AttributeError):
        return None


def get_pci_address_from_device(device_path):
    """
    Find the BDF corresponding to the device through the 
    /proc/driver/eswin/pacs/ directory
    """
    proc_path = "/proc/driver/eswin/pacs"
    if not os.path.exists(proc_path):
        print(f"Error: ESWIN proc path not found at {proc_path}")
        return None
    
    # Traverse all subdirectories
    for entry in os.listdir(proc_path):
        bdf_dir = os.path.join(proc_path, entry)
        info_file = os.path.join(bdf_dir, "information")
        
        if not os.path.isfile(info_file):
            continue
            
        try:
            with open(info_file, 'r') as f:
                content = f.read()
                
                inode_match = re.search(r'Device inode path:\s*(.+)\s*', content)
                if not inode_match or inode_match.group(1).strip() != device_path:
                    continue
                
                # Extract Bus Location
                bus_loc_match = re.search(r'Bus Location:\s*([0-9_]+)', content)
                if not bus_loc_match:
                    print(f"Warn: No Bus Location found in {info_file}")
                    return None
                
                # Convert Bus Location to BDF
                bdf = bus_location_to_bdf(bus_loc_match.group(1))
                if not bdf:
                    print(f"Warn: Invalid Bus Location format in {info_file}")
                    return None
                
                return f"0000:{bdf}" if ':' not in bdf else bdf
                
        except Exception as e:
            print(f"Error reading {info_file}: {str(e)}")
    
    print(f"Error: No matching device found for {device_path}")
    return None
        
def get_pcie_info(device_path):
    """
    Gets PCIe device information for a device.
    Args:
      device_path: The name of device.
    Returns:
      A dictionary containing the following keys:
        "bus_id": Bus ID of the network interface's PCIe device (e.g., "0000:01:00.0").
        "in_bridge": Boolean indicating whether the network interface is behind a PCIe bridge.
        "bridge_bus_id": Bus ID of the PCIe bridge if in_bridge is True.
        "child_bus_id": Bus ID of the PCIe bridge's secondary bus if in_bridge is True.
      Returns None on error.
    """
    try:
        # Get PCI address from device
        pci_id = get_pci_address_from_device(device_path)
        logging.debug(f"pci_id: {pci_id}")
        if not pci_id:
            print(f"Error: Cannot find PCI address for {device_path}")
            return None

        # Get PCIe device information using lspci
        lspci_cmd = ["lspci", "-vvv", "-s", pci_id]
        lspci_output = subprocess.check_output(lspci_cmd, universal_newlines=True).strip()
        logging.debug(f"lspci_output: {lspci_output}")

        result = {
            "bus_id": pci_id,
            "in_bridge": 0,
            "bridge_bus_id": None,
            "child_bus_id": None
        }

        # Check for Parent Bridge
        parent_bridge_pattern = r"Parent bridge=\s*(.*?)\s*\[(.*?)\]"
        parent_bridge_match = re.search(parent_bridge_pattern, lspci_output)
        if parent_bridge_match:
            result["in_bridge"] = True
            bridge_bus_id = parent_bridge_match.group(2)
            result["bridge_bus_id"] = bridge_bus_id

            # Get the secondary bus ID of the bridge
            lspci_bridge_cmd = ["lspci", "-vvv", "-s", bridge_bus_id]
            lspci_bridge_output = subprocess.check_output(lspci_bridge_cmd, universal_newlines=True).strip()
            bus_pattern = r"Bus:\s*primary=([0-9a-fA-F]+),\s*secondary=([0-9a-fA-F]+),"
            bus_match = re.search(bus_pattern, lspci_bridge_output)
            if bus_match:
                result["child_bus_id"] = bus_match.group(2).strip()

        return result

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def format_dec_value(value):
    return str(value) if value is not None else "N/A"

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    # logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.debug("Start get_pcie_info")
    parser = argparse.ArgumentParser(description="Get PCIe information for a device.")
    parser.add_argument("device_path", help="The path to the device (e.g., /dev/eswin_dev0).")
    args = parser.parse_args()
    pcie_info = get_pcie_info(args.device_path)

    if pcie_info:
        # Convert BDF strings to decimal values
        bus_id_dec = convert_pci_bdf_to_decimal(pcie_info["bus_id"])
        bridge_bus_id_dec = convert_pci_bdf_to_decimal(pcie_info["bridge_bus_id"]) if pcie_info["bridge_bus_id"] else None
        child_bus_id_dec = convert_pci_bdf_to_decimal(pcie_info["child_bus_id"]) if pcie_info["child_bus_id"] else None

        # Output formatted results
        print(f"on_bridge: {pcie_info['in_bridge']}")
        print(f"bus_id: {format_dec_value(bus_id_dec)}")
        print(f"bridge_bus_id: {format_dec_value(bridge_bus_id_dec)}")
        print(f"bridge_sub_bus_id: {format_dec_value(child_bus_id_dec)}")
    else:
        print(f"Failed to retrieve PCIe information for {args.device_path}.")