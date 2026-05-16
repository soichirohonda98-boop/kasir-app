import serial
import serial.tools.list_ports
from PyQt5.QtCore import QThread, pyqtSignal

class BluetoothPrinter:
    def __init__(self):
        self.serial_port = None
        self.baud_rate = 9600
    
    def get_available_ports(self):
        ports = []
        for port, desc, hwid in serial.tools.list_ports.comports():
            ports.append({'port': port, 'desc': desc})
        return ports
    
    def connect(self, port):
        try:
            self.serial_port = serial.Serial(port, self.baud_rate, timeout=1)
            return True
        except:
            return False
    
    def disconnect(self):
        if self.serial_port:
            self.serial_port.close()
    
    def print_receipt(self, data):
        if not self.serial_port:
            return False
        
        try:
            # ESC/POS Commands
            self.serial_port.write(b'\x1b\x40')  # Reset
            self.serial_port.write(b'\x1b\x45\x01')  # Emphasis ON
            
            for line in data:
                self.serial_port.write(line.encode('utf-8') + b'\n')
            
            self.serial_port.write(b'\x1b\x45\x00')  # Emphasis OFF
            self.serial_port.write(b'\x0a\x0a\x0a')  # Feed paper
            self.serial_port.write(b'\x1b\x69')  # Partial cut
            
            return True
        except:
            return False

class PrinterThread(QThread):
    print_finished = pyqtSignal(bool)
    
    def __init__(self, printer, data):
        super().__init__()
        self.printer = printer
        self.data = data
    
    def run(self):
        result = self.printer.print_receipt(self.data)
        self.print_finished.emit(result)
