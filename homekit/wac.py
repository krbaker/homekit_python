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
import re

import dns
import dns.resolver

from homekit.log_support import setup_logging, add_log_arguments

def setup_args_parser():
    parser = argparse.ArgumentParser(description='mfi network setup pairing app')
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

def mfi_discover(timeout=10):
    """ Discover mfi device.  User must have already connected wifi to the setup network
    Returns name, address, port and seed (needed for encryption """
    
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ['224.0.0.251'] #mdns multicast address
    resolver.port = 5353 #mdns port
    resolver.time = timeout
    resolver.lifetime = timeout
    try:
        result = resolver.query('_mfi-config._tcp.local','PTR')
    except dns.exception.Timeout:
        logging.error("Couldn't find mfi device via mdns")
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
                key, value = item.split("=")
                txt_data[key] = value
    assert len(txt_data) > 0, "TXT Data Not Found"
    assert 'seed' in txt_data, "Required Key 'Seed' not found"
    assert port, "No Port Found"
    assert target, "No Target Found"
    assert address, "No Address Found"
    assert address_name == target, "A Record not SRV Target"
    logging.debug("Found MFI device %s [%s:%s], seed %s" % (target, address, port, txt_data["seed"]))
    return (target, address, port, txt_data["seed"])

def mfi_auth(address, port, seed):
    pass
    
    
if __name__ == '__main__':
    args = setup_args_parser()

    setup_logging(args.loglevel)

    if args.key:
        key_function = key_from_parameter(args.key)
    else:
        key_function = key_from_keyboard()

    try:
        print (mfi_discover())
        
        
#        finish_pairing = controller.start_pairing(args.alias, args.device)
#        finish_pairing(pin_function())
#        pairing = controller.get_pairings()[args.alias]
#        pairing.list_accessories_and_characteristics()
#        controller.save_data(args.file)
#        print('Pairing for "{a}" was established.'.format(a=args.alias))
    except Exception as e:
        print(e)
        logging.debug(e, exc_info=True)
        sys.exit(-1)
