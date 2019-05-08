#!/usr/bin/env python3

import argparse
import ravencoin
from ravencoin.rpc import RavenProxy
from magnet import decode_magnet

parser = argparse.ArgumentParser(description='Recover torrent magnet links from the Ravencoin blockchain')
parser.add_argument("asset_name", help="Name of parent asset")
parser.add_argument("--datadir", help="Path to Raven config directory")
parser.add_argument("--testnet", help="Use Raven testnet",action="store_true")
args=parser.parse_args()

if args.testnet: ravencoin.SelectParams("testnet")

print(f"Recovering links with parent asset name {args.asset_name}, Testnet: {args.testnet}, RPC port: {ravencoin.GetParams().RPC_PORT}\n")

rvn = RavenProxy(datadir=args.datadir)

assets = rvn.listassets(args.asset_name + "#*", True)

for asset in assets:
   asset_name = assets[asset]['name']
   ipfs_hash = assets[asset]['ipfs_hash']
   magnet = decode_magnet(ipfs_hash,asset_name)
   print(magnet)
