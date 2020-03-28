#!/usr/bin/env python3

#
# Copyright 2020 Keith Baker
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import sys
import logging
import re, io

import dns
import dns.resolver

import tlv8

from homekit.protocol.tlv_types import TlvTypes

from homekit.log_support import setup_logging, add_log_arguments
from homekit.http_impl import HomeKitHTTPConnection, HttpContentTypes

from cryptography.hazmat.primitives.asymmetric import x25519

def setup_args_parser():
    parser = argparse.ArgumentParser(description='wac network setup pairing app')
    parser.add_argument('-s', action='store', required=True, dest='ssid', help='SSID')
    parser.add_argument('-k', action='store', required=False, dest='key', help='Network Key (will prompt without)')
    add_log_arguments(parser)
    return parser.parse_args()


def key_from_parameter(number):
    def tmp():
        return number
    return tmp


def key_from_keyboard():
    def tmp():
        return input('Enter Wifi Password: ')
    return tmp

def wac_discover(timeout = 10):
    """ Discover wac device.  User must have already connected wifi to the setup network
    Returns name, address, port and seed (needed for encryption) """

    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['224.0.0.251'] #mdns multicast address
    resolver.port = 5353 #mdns port
    resolver.time = 10
    resolver.lifetime = 10
    try:
        result = resolver.query('_mfi-config._tcp.local','PTR')
    except dns.exception.Timeout:
        logging.error("Couldn't find wac device looking for mfi_config via mdns")
        sys.exit(-1)
    except ValueError:
        logging.error("You might have an old version of dnspython that fails in python3")
        sys.exit(-1)
        
    port = None
    target = None
    address = None
    address_name = None
    txt_data = {}

    for rdata in result.response.additional:
        if dns.rdatatype.to_text(rdata.rdtype) == "SRV":
            port = rdata.items[0].port
            target = rdata.items[0].target
        if dns.rdatatype.to_text(rdata.rdtype) == "A":
            address_name = rdata.name
            address = rdata.items[0]
        if dns.rdatatype.to_text(rdata.rdtype) == "TXT":
            for item in rdata.items[0].strings:
                i = item.decode('utf-8')
                key, value = i.split("=")
                txt_data[key] = value
    assert len(txt_data) > 0, "TXT Data Not Found"
    assert 'seed' in txt_data, "Required Key 'Seed' not found"
    assert port, "No Port Found"
    assert target, "No Target Found"
    assert address, "No Address Found"
    assert address_name == target, "A Record not SRV Target"
    logging.debug("Found WAC device %s [%s:%s], seed %s" % (target, address, port, txt_data["seed"]))
    return (target, address, port, txt_data["seed"])

def wac_auth(setup_private_key, address, port, seed):
    public_bytes = setup_private_key.public_key().public_bytes()
    body = b'\x01' + public_bytes
    conn = HomeKitHTTPConnection(str(address), port=port)
    conn.connect()
    conn.putrequest('POST', '/auth-setup', skip_accept_encoding = True)
    conn.putheader('Content-Type', 'application/octet-stream')
    conn.putheader('Content-Length', len(body))
    conn.endheaders(body)
    response = conn.getresponse()
    response_tlv = tlv8.decode(response.read(),
                               {TlvTypes.PublicKey: tlv8.DataType.BYTES,
                                TlvTypes.Signature: tlv8.DataType.BYTES,
                                TlvTypes.Certificate: tlv8.DataType.BYTES} )
    logging.error('response: {}'.format(tlv8.format_string(response_tlv)))
    

if __name__ == '__main__':
    args = setup_args_parser()

    setup_logging(args.loglevel)

    if args.key:
        key_function = key_from_parameter(args.key)
    else:
        key_function = key_from_keyboard()

        
    setup_private_key = x25519.X25519PrivateKey.generate()
    name, address, port, seed = wac_discover()
    logging.error("Found {} {}".format(address, port))
    wac_auth(setup_private_key, address, port, seed)
    logging.error("Done")

