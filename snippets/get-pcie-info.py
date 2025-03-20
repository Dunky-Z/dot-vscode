import subprocess
import re
import argparse  # Import the argparse module


def get_pcie_info(interface_name):
    """
    Gets PCIe device information for a network interface, including bus ID,
    whether it is behind a PCIe bridge, and related bridge information.

    Args:
      interface_name: The name of the network interface, e.g., "eth0" or "enp0s3".

    Returns:
      A dictionary containing the following keys:
        "bus_id": Bus ID of the network interface's PCIe device (e.g., "0000:01:00.0").
                 None if it cannot be determined.
        "in_bridge": Boolean indicating whether the network interface is behind a PCIe bridge.
                    None if it cannot be determined.
        "bridge_bus_id": Bus ID of the PCIe bridge if in_bridge is True.
                        None if not in a bridge or cannot be determined.
        "child_bus_id": Bus ID of the PCIe bridge's child device if in_bridge is True.
                        None if not in a bridge or cannot be determined.
      Returns None on error.
    """

    try:
        # 1. Get the PCI address of the network interface (using ethtool)
        ethtool_cmd = ["ethtool", "-i", interface_name]
        ethtool_output = subprocess.check_output(
            ethtool_cmd, universal_newlines=True).strip()
        pci_id_line = next(
            (line for line in ethtool_output.splitlines() if "bus-info" in line), None)

        if not pci_id_line:
            print(
                f"Error: Could not determine PCI address for interface {interface_name}")
            return None  # Return None to indicate failure

        pci_id = pci_id_line.split(":")[2].strip()

        # 2. Get PCIe device information (using lspci)
        lspci_cmd = ["lspci", "-vvv", "-s", pci_id]
        lspci_output = subprocess.check_output(
            lspci_cmd, universal_newlines=True).strip()

        # 3. Parse the lspci output
        result = {
            "bus_id": pci_id,
            "in_bridge": False,
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

            # Get the child bus ID of the bridge
            child_bus_id = None

            # Get bridge information
            lspci_bridge_cmd = ["lspci", "-vvv", "-s", bridge_bus_id]
            lspci_bridge_output = subprocess.check_output(
                lspci_bridge_cmd, universal_newlines=True).strip()
            if lspci_bridge_output:
                # Find Bus: primary=, secondary=
                bus_pattern = r"Bus:\s*primary=(.*?),\s*secondary=(.*?),"
                bus_match = re.search(bus_pattern, lspci_bridge_output)
                if bus_match:
                    child_bus_id = bus_match.group(
                        2).strip()  # secondary bus is the child bus ID
                    result["child_bus_id"] = child_bus_id

        return result

    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return None  # Return None to indicate failure
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# Example usage
if __name__ == "__main__":
    # Use argparse to handle command-line arguments
    parser = argparse.ArgumentParser(
        description="Get PCIe information for a network interface.")
    parser.add_argument(
        "interface_name", help="The name of the network interface (e.g., eth0)")
    args = parser.parse_args()

    interface_name = args.interface_name

    pcie_info = get_pcie_info(interface_name)

    if pcie_info:
        print(f"PCIe Information for {interface_name}:")
        print(f"  Bus ID: {pcie_info['bus_id']}")
        print(f"  In PCIe Bridge: {pcie_info['in_bridge']}")
        if pcie_info["in_bridge"]:
            print(f"  Bridge Bus ID: {pcie_info['bridge_bus_id']}")
            print(f"  Bridge Child Bus ID: {pcie_info['child_bus_id']}")
    else:
        print(f"Failed to retrieve PCIe information for {interface_name}.")
