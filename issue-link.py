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
import sys

import ravencoin
from ravencoin.core import b2lx
from ravencoin.rpc import RavenProxy
from ravencoin.assets import CAssetName,InvalidAssetName

from magnet import encode_magnet_xt, split_magnet_uri, yes_no

parser = argparse.ArgumentParser(description='Publish a magnet link in the Ravencoin blockchain')
parser.add_argument("asset", help="Base asset name (e.g. URN)")
parser.add_argument("magnet_link", help="Magnet link (e.g. magnet:?xt=urn:btih:95028fb1ef3059321eac737f7d583c2a0eeda130&dn=Night.of.the.Living.Dead.1968)")
parser.add_argument("--filename", type=str, default="", help="Magnet link filename (e.g. NIGHT.OF.THE.LIVING.DEAD)")
parser.add_argument("--datadir", help="Path to Raven config directory")
parser.add_argument("--testnet", help="Use Raven testnet",action="store_true")
args=parser.parse_args()

if args.testnet:
    ravencoin.SelectParams("testnet")
else:
    ravencoin.SelectParams("mainnet")

magnet_hash,magnet_type,magnet_fn = split_magnet_uri(args.magnet_link)

asset_name = args.asset.upper()
file_name = args.filename
if file_name == "":
    file_name = magnet_fn

try:
    asset = CAssetName(asset_name + "#" + file_name)
except InvalidAssetName as e:
    print(f"Asset name is invalid. Try specifying a shorter name with --filename and/or removing special characters\nError message: {e}")
    sys.exit(1)

hash_data = encode_magnet_xt(magnet_hash,magnet_type)

rvn = RavenProxy(datadir=args.datadir)

try:
   if yes_no(f"Issuing asset {asset} with magnet hash {magnet_hash}, proceed? (Testnet: {args.testnet})"):
       txid = b2lx(rvn.issue(asset, 1, "", "", 0, False, True, hash_data))
       print(f"txid: {txid}")
except Exception as e:
   print(f"Error: {e}")
