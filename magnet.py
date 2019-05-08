#!/usr/bin/env python3

import binascii
from ravencoin.base58 import encode as b58encode
from ravencoin.base58 import decode as b58decode
from ravencoin.assets import CMainAsset, CSubAsset, CUniqueAsset


def encode_magnet(main_asset, sub_asset, magnet_hash, magnet_name):

   magnet_name = str.upper(magnet_name)
   
   hash_bin = binascii.unhexlify(magnet_hash) # 20 byte sha-1 hash
   # ipfs hash is 32 bytes, so pad with zeros
   ipfs_hash = "Qm" + b58encode(hash_bin + b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

   asset = CUniqueAsset(magnet_name,parent=CSubAsset(sub_asset,parent=CMainAsset(main_asset)))

   return asset, ipfs_hash


def decode_magnet(ipfs_hash, asset_name):

   delim = "#"
   magnet_name = asset_name.partition(delim)[2]

   ipfs_hash = ipfs_hash[2:] # drop the 'Qm'
   hash_bin = b58decode(ipfs_hash)[1:21] # 20 byte sha-1 hash
   hash_bin_hex = binascii.hexlify(hash_bin).decode()

   magnet = f"magnet:?xt=urn:btih:{hash_bin_hex}&dn={magnet_name}"

   return magnet

if __name__ == "__main__":
   # test
   asset,ipfs_hash = encode_magnet("URN","BTIH","8c4adbf9ebe66f1d804fb6a4fb9b74966c3ab609","UBUNTU-18.10-A64.ISO")
   print(asset.full_name,ipfs_hash)
   print(decode_magnet("QmTfxewsVrLSgSiwtnMLZqcdzaYXjomQEsqVbteyvC2Fod","URN/BTIH#UBUNTU-18.10-A64.ISO"))
