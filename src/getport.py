import serial.tools.list_ports

# Find the USB port associated with the fingerprint scanner
def find_usb_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "USB Serial Port" in port.description:
            return port.device
    return None

# Main program
def main():
    usb_port = find_usb_port()
    if usb_port:
        print("USB port found:", usb_port)
    else:
        print("USB port not found.")

if __name__ == '__main__':
    main()