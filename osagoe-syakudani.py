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

def cattree(args):
    args.prettyprint = True
    args.type = False
    args.size = False
    catfile(args)

def catfile(args):
    with open(".git/objects/{}/{}".format(args.object[0:2], args.object[2:]), "br") as f:
        data_typesize, _, data_item = zlib.decompress(f.read(-1)).partition(b'\0')
        data_type, _, data_size = data_typesize.partition(b' ')
    item_type = data_type.decode(sys.getfilesystemencoding())

    if args.type:
        print(item_type)
    if args.size:
        print(data_size.decode(sys.getfilesystemencoding()))
    if args.prettyprint:
        if item_type == "blob" or item_type == "commit":
            print(data_item.decode(sys.getfilesystemencoding()))
        if item_type == "tree":
            while len(data_item):
                data_permission, _, data_item = data_item.partition(b' ')
                data_fname, _, data_item = data_item.partition(b'\0')
                data_hash = data_item[:20]
                data_item = data_item[20:]
                print("{}\t{}\t{}".format( 
                        data_permission.decode(sys.getfilesystemencoding()),
                        data_hash.hex(),
                        data_fname.decode(sys.getfilesystemencoding())))
                # sha1 has 40 len 20 bytes


def hashobject(args):
    datastr = ""
    if args.stdin:
        datastr = sys.stdin.read(-1)
    if args.file:
        with open(args.file, "r") as f:
            datastr = f.read(-1)
    content = bytes(f"blob {len(datastr)}\0{datastr}", sys.getfilesystemencoding())
    m = hashlib.sha1()
    m.update(content)
    digest = m.hexdigest()
    print(digest)
    dirname = f".git/objects/{digest[0:2]}"
    os.makedirs(dirname, exist_ok=True)
    with open("{}/{}".format(dirname, digest[2:]), "bw") as f:
        f.write(zlib.compress(content, level=1))

def init(args):
    dirname = f".git/refs"
    os.makedirs(dirname, exist_ok=True)
    with open(".git/HEAD", "w") as f:
        f.write("ref: refs/heads/master")

parser = argparse.ArgumentParser(description="Git subset")
subparsers = parser.add_subparsers(required=False)

subcmd = subparsers.add_parser("init")
subcmd.set_defaults(func=init)

subcmd = subparsers.add_parser("cat-file")
subcmd.set_defaults(func=catfile)
subcmd.add_argument("-p", "--prettyprint", action="store_true")
subcmd.add_argument("-t", "--type", action="store_true")
subcmd.add_argument("-s", "--size", action="store_true")
subcmd.add_argument("object")

subcmd = subparsers.add_parser("hash-object")
subcmd.set_defaults(func=hashobject)
subcmd.add_argument("-s", "--stdin", action="store_true")
subcmd.add_argument("-f", "--file")

subcmd = subparsers.add_parser("ls-tree")
subcmd.add_argument("object")
subcmd.set_defaults(func=cattree)
args = parser.parse_args()
args.func(args)
