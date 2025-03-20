import subprocess
import re
import argparse

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

def get_pcie_info(interface_name):
    """
    Gets PCIe device information for a network interface, including bus ID,
    whether it is behind a PCIe bridge, and related bridge information.
    Args:
      interface_name: The name of the network interface, e.g., "eth0" or "enp0s3".
    Returns:
      A dictionary containing the following keys:
        "bus_id": Bus ID of the network interface's PCIe device (e.g., "0000:01:00.0").
        "in_bridge": Boolean indicating whether the network interface is behind a PCIe bridge.
        "bridge_bus_id": Bus ID of the PCIe bridge if in_bridge is True.
        "child_bus_id": Bus ID of the PCIe bridge's secondary bus if in_bridge is True.
      Returns None on error.
    """
    try:
        # Get the PCI address of the network interface using ethtool
        ethtool_cmd = ["ethtool", "-i", interface_name]
        ethtool_output = subprocess.check_output(ethtool_cmd, universal_newlines=True).strip()
        pci_id_line = next((line for line in ethtool_output.splitlines() if "bus-info" in line), None)
        if not pci_id_line:
            print(f"Error: Could not determine PCI address for interface {interface_name}")
            return None
        # Extract the PCI address from the line
        pci_id_line = pci_id_line.split()[-1].strip()
        # print(f"PCI address of {interface_name}: {pci_id_line}")

        # Get PCIe device information using lspci
        lspci_cmd = ["lspci", "-vvv", "-s", pci_id_line]
        lspci_output = subprocess.check_output(lspci_cmd, universal_newlines=True).strip()
        # print(f"lspci output for {pci_id_line}:\n{lspci_output}")

        result = {
            "bus_id": pci_id_line,
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
    parser = argparse.ArgumentParser(description="Get PCIe information for a network interface.")
    parser.add_argument("interface_name", help="The name of the network interface (e.g., eth0)")
    args = parser.parse_args()

    interface_name = args.interface_name
    pcie_info = get_pcie_info(interface_name)

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
        print(f"Failed to retrieve PCIe information for {interface_name}.")