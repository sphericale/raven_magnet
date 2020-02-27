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

import argparse
import ravencoin
from ravencoin.rpc import RavenProxy
from magnet import decode_magnet_xt,magnet_uri

parser = argparse.ArgumentParser(description='Recover magnet links from the Ravencoin blockchain')
parser.add_argument("asset_name", help="Name of parent asset")
parser.add_argument("--datadir", help="Path to Raven config directory")
parser.add_argument("--testnet", help="Use Raven testnet",action="store_true")
args=parser.parse_args()

if args.testnet:
    ravencoin.SelectParams("testnet")
else:
    ravencoin.SelectParams("mainnet")

print(f"Recovering links with parent asset name {args.asset_name}, Testnet: {args.testnet}, RPC port: {ravencoin.params.RPC_PORT}\n")

rvn = RavenProxy(datadir=args.datadir)

assets = rvn.listassets(args.asset_name + "#*", True) # list unique assets under asset_name

for asset in assets:
   asset_name = assets[asset].get('name','')
   if asset_name != "":
       try:
           base_name, fn = asset_name.split('#')
       except ValueError:
           fn = ""
       if fn != "":
           tx_hash = assets[asset].get('txid_hash','')
           if tx_hash != "":
               try:
                   hash_type,hash_str = decode_magnet_xt(tx_hash)
                   uri = magnet_uri(hash_str,hash_type,fn)
                   print(uri)
               except Exception:
                   pass
