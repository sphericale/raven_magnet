#!/usr/bin/env python3

import ravencoin
import argparse
from magnet import encode_magnet
from ravencoin.rpc import RavenProxy

parser = argparse.ArgumentParser(description='Publish a torrent magnet link in the Ravencoin blockchain')
parser.add_argument("main", help="Main asset name")
parser.add_argument("sub", help="Sub asset name")
parser.add_argument("magnet_hash", help="Torrent hash")
parser.add_argument("name", help="Torrent name")
parser.add_argument("--datadir", help="Path to Raven config directory")
parser.add_argument("--testnet", help="Use Raven testnet",action="store_true")
args=parser.parse_args()

if args.testnet: ravencoin.SelectParams("testnet")

top_level = args.main.upper()
second_level = args.sub.upper()
magnet_hash = args.magnet_hash
magnet_name = args.name

asset, ipfs_hash = encode_magnet(top_level,second_level,magnet_hash,magnet_name)

rvn = RavenProxy(datadir=args.datadir)

try:
   print(f"Issuing asset {asset.full_name}, Testnet: {args.testnet}, RPC port: {ravencoin.GetParams().RPC_PORT}\n")
   rvn.issue(asset, 1, "", "", 0, False, True, ipfs_hash)
except Exception as e:
   print(f"Error: {e}")
