__author__ = 'jason'


"""Original author credit goes to Ole at https://ole.im/blog/2011/aug/04/warsow-server-query-script"""

"""Script that opens a UDP challenge packet to an active Warsow server to collect info or could
    be used as a heartbeat monitor"""

"""Works in python 3"""

import sys
import socket

PACKET_SIZE = 1024

class WarsowQuery:
    """When instanced, create the basic info to create a socket connection"""
    def __init__(self, ip, port=44400, timeout=1.0):
        self.ip = ip
        self.port = port
        self.timeout = 1.0 # set timeout for the socket so it won't hang on connection failure
        self.socket = None


    """Try to create a UDP socket connection or timeout if connection fails"""
    def connect(self):
       try:
           ''' Resolve hostname, if it's not an IP '''
           self.ip = socket.gethostbyname(self.ip)

       except:
           ''' if the above fails, it must not be a valid IP, or the hostname failed to resolve '''
           return

       finally:
           self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
           self.socket.settimeout(self.timeout)




    """ Make the connection defined in the function above, pass a specific challenge message,
        and return the data packet the server sends back for processing except if there
        is a timeout.All queries are done by sending UDP packet to the server or masterserver.
        These packets are marked to be connectionless (not part of in-game communication) packets
        by first four bytes of the message. These bytes are to have all bits sets.
        So these 4 byte header should be
        '\xFF\xFF\xFF\xFF'. All response packet are also UDP packets with the same header. -Warsow Wiki
    """
    def get_packet(self, message):
       self.connect()
       message = chr(255) * 4 + message
       message = bytes(message, 'iso-8859-1')

       try:
           self.socket.sendto( message, (self.ip, self.port ))
           data, addr = self.socket.recvfrom(PACKET_SIZE)
           return data

       except socket.timeout:
           return




    """A function that passes through the 'getinfo' challenge to the server and returns all the values
        in a easily parsable dictionary for subsequent functions to return data"""
    def info(self):
        packet = self.get_packet('getinfo')
        if packet:
            ''' Packets received from warsow servers are pretty simple to parse,
               just break it up by every instance of \
           '''
            raw = packet.decode('iso-8859-1').split("\\")

            ''' append the ip and port to the output (and create the dict)'''
            params = {'ip': self.ip, 'port': str(self.port)}

            ''' this is a little tricky, the parsing starts from 3
               (anything in the array before the third char is useless)
               and then counts up  by 2 for every time the loop runs
               to get a dict consisting of "setting = value" for the
               entire returned string
           '''
            for i in range(3, len(raw[1:]), 2):
                params[raw[i]] = raw[i+1]

            return params
        return {} # return empty dict if the connection attempt somehow failed.





    def hostname_challenge(self):
        """Similar to the above function but just concentrates on grabbing the hostname from the server"""
        packet = self.get_packet('getinfo')
        if packet:
            raw = packet.decode('iso-8859-1').split("\\")
            """The value for sv_hostname should be the 32nd entry in the dictionary"""
            challenge = raw[32]
            return challenge
        return []#return empty dict if the connection attempt somehow failed.

        

def main():
    """Main entry point for the script."""



if __name__ == '__main__':
    sys.exit(main())