# from digi.xbee.devices import XBeeDevice
# import time
# import random

# device_url = "/dev/cu.usbserial-00000000"

# class ZigbeeDevice:
#     # type represents whether the zigbee is a transmitter or receiver
#     # 0 = transmitter
#     # 1 = receiver
#     def __init__(self, type, device_url):
#         # Instantiate a local XBee node.
#         # send_data_64_16(XBee64BitAddress, XBee16BitAddress, String or Bytearray, Integer)	
#         # Specifies the 64-bit and 16-bit destination addresses, the data to send, and, optionally, 
#         # the transmit options. If you do not know the 16-bit address, use XBee16BitAddress.UNKNOWN_ADDRESS.
#         self.device = XBeeDevice(device_url, 9600)
#         self.type = type

#     def get_type(self):
#         return self.type

#     def open_device(self):
#         self.device.open()
    
#     def close_device(self):
#         self.device.close()
    
#     def transmit_message(self, message):
#         self.device.send_data_broadcast(message)
    
#     def receive_message(self):
#         return None