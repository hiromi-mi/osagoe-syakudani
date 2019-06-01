# osagoe-syakudani.py
# Copyright 2019 hiromi-mi
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import zlib
import hashlib
import sys
import os

def catfile(args):
    print(args)

def hashobject(args):
    content = bytes(f"blob {len(args.str)}\0" + args.str, sys.getfilesystemencoding())
    m = hashlib.sha1()
    m.update(content)
    digest = m.hexdigest()
    print(digest)
    dirname = f".git/objects/{digest[0:2]}"
    os.makedirs(dirname, exist_ok=True)
    with open("{}/{}".format(dirname, digest[2:]), "b+w") as f:
        f.write(zlib.compress(content, level=1))

def init(args):
    dirname = f".git/refs"
    os.makedirs(dirname, exist_ok=True)
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/master")

parser = argparse.ArgumentParser(description="Git subset")
subparsers = parser.add_subparsers()
subcmd = subparsers.add_parser("init")
subcmd.set_defaults(func=init)
subcmd = subparsers.add_parser("cat-file")
subcmd.set_defaults(func=catfile)
subcmd = subparsers.add_parser("hash-object")
subcmd.set_defaults(func=hashobject)
subcmd.add_argument("str")
args = parser.parse_args()
args.func(args)
