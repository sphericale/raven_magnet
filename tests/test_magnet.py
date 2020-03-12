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
import unittest

from magnet import split_magnet_uri, encode_magnet_xt, MAGIC_BYTES, MAX_HASH_LEN, hash_obj_by_name, supported_types


class Test_Magnet(unittest.TestCase):

    def check_magnet_link(self,uri_test):

        uri_magnet_link = uri_test[0]
        uri_hash_type = hash_obj_by_name(uri_test[1]).hash_type
        uri_hash_len = uri_test[2]

        hash_s,hash_type,fn = split_magnet_uri(uri_magnet_link)

        encoded_hex = encode_magnet_xt(hash_s,hash_type)
        encoded = bytes.fromhex(encoded_hex)
        t, l, binh = struct.unpack(f"<4x B B {MAX_HASH_LEN}s",encoded)

        self.assertTrue(encoded[0:4] == MAGIC_BYTES) # MAGN
        self.assertTrue(t == uri_hash_type) # hash type
        self.assertTrue(l == uri_hash_len) # length of hash

        hash_obj = hash_obj_by_name(hash_type)

        if hash_obj.encoding == "base32":
            h = base64.b32encode(binh[:l]).decode("ascii")
        elif hash_obj.encoding == "hex":
            h = binh[:l].hex()
        else:
            raise ValueError("Unsupported encoding {hash_obj.encoding}")

        self.assertTrue(h.lower() == hash_s.lower()) # hash


    def test_valid(self):

        test_list = [
        ["magnet:?xt=urn:btih:95028fb1ef3059321eac737f7d583c2a0eeda130&dn=Night.of.the.Living.Dead.1968","btih",20],
        ["magnet:?xt=urn:btih:095d0650e6536e9a7d56345973cf56bb5c5f697d&dn=debian-live-10.3.0-amd64-gnome.iso&tr=http%3A%2F%2Fbttracker.debian.org%3A6969%2Fannounce","btih",20],
        ["magnet:?xt=urn:ed2k:31D6CFE0D16AE931B73C59D7E0C089C0&xl=0&dn=zero_len.fil&xt=urn:bitprint:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ.LWPNACQDBZRYXW3VHJVCJ64QBZNGHOHHHZWCLNQ&xt=urn:md5:D41D8CD98F00B204E9800998ECF8427E","ed2k",16],
        ["magnet:?xt=urn:tree:tiger:7N5OAMRNGMSSEUE3ORHOKWN4WWIQ5X4EBOOTLJY&xt=urn:btih:QHQXPYWMACKDWKP47RRVIV7VOURXFE5Q","tth",24]
        ] # magnet link, expected type, expected hash length (bytes)

        for uri_test in test_list:
            self.check_magnet_link(uri_test)


    def test_invalid(self):

        with self.assertRaises(ValueError):
            encode_magnet_xt("95028fb1ef3059321eac737f7d583c2a0eeda1300000000000000000000","btih") # too long hash

        with self.assertRaises(ValueError):
            encode_magnet_xt("95028fb1ef3059321eac737f7d583c2a0eeda130","FFFFFFFFF") # bad hash type

        # malformed link
        with self.assertRaises(AttributeError):
            self.check_magnet_link(["magnet:urn:btih:95028fb1ef3059321eac737f7d583c2a0eeda130&dn=Night.of.the.Living.Dead.1968","btih",20])
        # unsupported hash type
        with self.assertRaises(AttributeError):
            self.check_magnet_link(["magnet:?xt=urn:zzhashzz:095d0650e6536e9a7d56345973cf56bb5c5f697d&dn=debian-live-10.3.0-amd64-gnome.iso&tr=http%3A%2F%2Fbttracker.debian.org%3A6969%2Fannounce","btih",20])
        # truncated hashes
        with self.assertRaises(ValueError):
            self.check_magnet_link(["magnet:?xt=urn:ed2k:31D6CFE0D16AE931B73C5&xl=0&dn=zero_len.fil&xt=urn:bitprint:3I42H3S6NNFQ2MSVX7XZKYAYSCX5QBYJ.LWPNACQDBZRYXW3VHJVCJ64QBZNGHOHHHZWCLNQ&xt=urn:md5:D41D8CD98F00B204E9800998ECF8427E","ed2k",16])
        with self.assertRaises(ValueError):
            self.check_magnet_link(["magnet:?xt=urn:tree:tiger:7N5OAMRNGMSSEUE3ORHOKWN4WWIQ5X4EBOOTLJ&xt=urn:btih:QHQXPYWMACKDWKP47RRVIV7VOURXFE5Q","tth",24])
        with self.assertRaises(ValueError):
            self.check_magnet_link(["magnet:?xt=urn:btih:95028fb1ef3059&dn=Night.of.the.Living.Dead.1968","btih",20])
