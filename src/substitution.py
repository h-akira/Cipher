#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-01-03

# Import
import sys
import os
import substitution_module as sm

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
シーザー暗号を暗号化・復号化，解読する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-i", "--input", metavar="input-file", help="入力ファイル")
  parser.add_argument("-o", "--output", metavar="output-file", help="出力ファイル")
  parser.add_argument("-l", "--letter-case", choices=['upper','lower','distinguish'], default='upper', help="大文字に統一，小文字に統一，区別する")
  parser.add_argument("-g", "--generate-key", action="store_true", help="鍵を作成して保存して終了する")
  parser.add_argument("-d", "--decryption", action="store_true", help="復号化")
  parser.add_argument("file", metavar="key-file", help="key file")
  options = parser.parse_args()
  return options

def main():  
  # ArgumentParser
  options = parse_args()

  key = sm.Key()
  if options.generate_key:
    key.gen_key(target=input("対象:"))
    if os.path.isfile(options.file):
      if "y" != input(f"{options.file}は既に存在します．上書きしますか？(y/other):"):
        sys.exit()
    key.save_key(options.file)
    sys.exit()
  else:
    key.read_key(options.file)

  if options.input:
    with open(options.input,mode="r") as f:
      text = f.read()[:-1]
  else:
    text = input("入力:")

  if options.letter_case == 'upper':
    text = text.upper()
    key.upper()
  elif options.letter_case == 'lower':
    text = text.lower()
    key.lower()

  output = sm.encryption(text,key,decryption=options.decryption)

  if options.output:
    if os.path.isfile(options.output):
      if "y" != input(f"{options.output}は既に存在します．上書きしますか？(y/other):"):
        print(output)
        sys.exit()
    with open(options.output, mode='w') as f:
      print(output, file=f)
  else:
    print(output)

if(__name__ == '__main__'):
  main()
