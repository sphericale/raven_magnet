#!/usr/bin/env python3
# Copyright (C) 2020 standard-error@github
#
# This file is part of raven-magnet
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of raven-magnet, including this file, may be copied, modified,
# propagated, or distributed except according to the terms contained in the
# LICENSE file.

import base64
import struct
import re

class HashType(object):
    def __init__(self,hash_type,hash_type_str,expected_length):
        self.hash_type = hash_type
        self.hash_type_str = hash_type_str
        self.length = expected_length

    def __repr__(self):
        return f"{self.hash_type_str}"

    def __hash__(self):
        return hash(self.hash_type_str)

    def __eq__(self, other):
        return self.hash_type_str == other

hex_types = frozenset([
HashType(0,"btih",20),
HashType(1,"ed2k",16),
])

base32_types = frozenset([
HashType(2,"sha1",20),
HashType(3,"tth",24),
])

# 04-ff reserved

supported_types = frozenset(hex_types | base32_types)

TXID_HASH_LEN = 32 # length in bytes of Raven txid hash data

MAGIC_BYTES = b"\x4d\x41\x47\x4e" # MAGN
MAX_HASH_LEN = TXID_HASH_LEN-(len(MAGIC_BYTES)+1+1)

def hash_str_from_type(hash_type):
    for item in supported_types:
         if item.hash_type == hash_type:
             return item.hash_type_str

def hash_obj_by_name(hash_type_str):
    for item in supported_types:
        if item.hash_type_str == hash_type_str:
            return item


def encode_magnet_xt(hash_str,hash_type_str):

    # encode magnet link hash
    # format is:
    # 4 bytes identifier MAGIC_BYTES
    # 1 byte unsigned char: hash type (see list above)
    # 1 byte unsigned char: length of hash bytes
    # up to 26 bytes - hash bytes
    # zero padding up to 32 bytes

    if hash_type_str == "tree:tiger":
        hash_type_str = "tth"

    if hash_type_str not in supported_types:
        raise ValueError(f"Unsupported hash type {hash_type_str}")

    if hash_type_str in base32_types:
        hash_bin = base64.b32decode(hash_str)
    else: # hex
        hash_bin = bytes.fromhex(hash_str)

    expected_hash_len = hash_obj_by_name(hash_type_str).length
    len_hash_bin = len(hash_bin)

    if len_hash_bin > MAX_HASH_LEN:
        raise ValueError(f"Hash too long (max {MAX_HASH_LEN} bytes)")

    if len_hash_bin != expected_hash_len:
        raise ValueError(f"Hash wrong length {len_hash_bin} (expected {expected_hash_len} bytes)")

    hash_type = hash_obj_by_name(hash_type_str).hash_type

    len_diff = MAX_HASH_LEN - len_hash_bin
    hash_bin += b"\x00" * len_diff # pad with zeros

    result = struct.pack(f"<4s B B {MAX_HASH_LEN}s",MAGIC_BYTES,hash_type,len_hash_bin,hash_bin)

    return result.hex()


def decode_magnet_xt(magnet_data):

    magn_bin = bytes.fromhex(magnet_data)

    if len(magn_bin) != 32 or magn_bin[0:4] != MAGIC_BYTES:
        raise ValueError("Invalid magnet link data")

    hash_type, len_hash_bin, hash_bin = struct.unpack(f"<4x B B {MAX_HASH_LEN}s",magn_bin)

    hash_type_str = hash_str_from_type(hash_type)
    hash_bin = hash_bin[0:len_hash_bin]

    if hash_type_str in base32_types:
        hash_str = base64.b32encode(hash_bin).decode("ascii")
    else: # hex
        hash_str = hash_bin.hex()

    return hash_type_str,hash_str


magnet_regex = re.compile(".*\?xt=urn:(\w+):(\w+)") # extract hash type and hash from magnet link
magnet_fn_regex = re.compile(".+&dn=([\x20-\x25\x27-\x7E]+)") # filename, ascii text (excluding &)


def split_magnet_uri(uri):

    uri = uri.replace("tree:tiger","tth")
    m = magnet_regex.match(uri)
    magnet_hash = ""
    magnet_type = ""
    if m:
       try:
           magnet_hash = m[2]
       except Exception:
           pass
       try:
           magnet_type = m[1]
       except Exception:
           pass

    f = magnet_fn_regex.match(uri)
    magnet_fn = ""
    if f:
       try:
           magnet_fn = f[1]
       except Exception:
           pass

    if magnet_type in base32_types:
        missing_padding = len(magnet_hash) % 4 # if padding stripped from base32 hash we need to add it back
        if missing_padding:
            magnet_hash += '=' * (4 - missing_padding)

    if magnet_hash == "" or magnet_type == "":
        raise ValueError(f"Error decoding magnet uri {uri}")

    return magnet_hash,magnet_type,magnet_fn


def magnet_uri(hash_str,hash_type,fn):
    if hash_type == "tth":
        hash_type = "tree:tiger"
    return f"magnet:?xt=urn:{hash_type}:{hash_str}&dn={fn}"

def magnet_uri_from_data(data,fn):
    hash_type,hash_str = decode_magnet_xt(data)
    uri = magnet_uri(hash_str,hash_type,fn)
    return uri


def yes_no(q):
    yes = {'yes', 'y', 'ye'}
    no = {'no', 'n'}
    while True:
        choice = input(q + " ").lower()
        if choice in yes:
           return True
        elif choice in no:
           return False
        else:
           print("Please answer 'yes' or 'no'")
