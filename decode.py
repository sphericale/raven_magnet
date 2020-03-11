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
from magnet import magnet_uri_from_data

parser = argparse.ArgumentParser(description='Decode magnet link data')
parser.add_argument("asset", help="Name of asset")
parser.add_argument("data", help="Hex encoded magnet link data")
args=parser.parse_args()

fn = args.asset.split('#')[1]
print(magnet_uri_from_data(args.data,fn))

