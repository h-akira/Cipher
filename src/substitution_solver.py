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
単一換字式暗号を解読する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-t", "--target", metavar="target-file", help="変換対象の文字列が書かれたテキストファイル")
  parser.add_argument("-i", "--input", metavar="input-file", help="入力ファイル")
  parser.add_argument("-o", "--output", metavar="output-file", help="出力ファイル")
  parser.add_argument("-d", "--db-file", metavar="db-file", default="ejdict.sqlite3", help="データベースファイル")
  parser.add_argument("-N", "--Number", metavar="数字", type=int, default=6, help="総当り攻撃の未知数")
  parser.add_argument("-n", "--number", metavar="数字", type=int, default=2, help="総当り攻撃の決定数")
  parser.add_argument("-l", "--letter-case", choices=['upper','lower','distinguish'], default='upper', help="大文字に統一，小文字に統一，区別する")
  # parser.add_argument("-g", "--generate-key", action="store_true", help="鍵を作成して保存して終了する")
  # parser.add_argument("-d", "--decryption", action="store_true", help="復号化")
  # parser.add_argument("file", metavar="key-file", help="key file")
  options = parser.parse_args()
  return options

def main():  
  # ArgumentParser
  options = parse_args()
  
  CT = sm.CipherText()
  key = sm.Key()
  key.empty_key()

  if options.target:
    CT.read_target(options.target)
  else:
    CT.input_target()

  if options.input:
    CT.read_text(options.input)
  else:
    CT.input_text()

  if options.letter_case == 'upper':
    CT.upper()
  elif options.letter_case == 'lower':
    CT.lower()

  FA = sm.FrequencyAnalysis(CT)
  FA.cal_single()
  # FA.set_general("isorlcumpfgywkvbjqxz".upper())
  FA.set_general()
  # FA.cal_double()
  # print(sorted(FA.double, key=lambda x: x[2], reverse=True)[:10])
  # FA.cal_triple()
  if not os.path.isfile(options.db_file):
    print("辞書データがありません．")
    sys.exit()
  else:
    dic = sm.Dictionary(options.db_file)

  # dic.set_words(CT)
  sm.find_the_and(FA,CT,key)
  print(key.target)
  print(key.conversion)
  while True:
    if len(CT.target)>options.Number:
      sm.brute_force(CT,FA,key,options.Number,options.number, dic)
    else:
      sm.brute_force(CT,FA,key,len(CT.target),len(CT.target), dic)
      break
    print(key.target)
    print(key.conversion)
  print("Decrypted_Text")
  print(CT.decrypted_text)
  print("Key:")
  print("".join(key.target))
  print("".join(key.conversion))
  # output = sm.encryption(text,key,decryption=options.decryption)

  # if options.output:
  #   # if os.path.isfile(options.file):
  #     if "y" != input(f"{options.output}は既に存在します．上書きしますか？(y/other):"):
  #       print(output)
  #       sys.exit()
  #   with open(options.output, mode='w') as f:
  #     print(output, file=fkkkkk)
  # else:
  #   print(output)
  #
if(__name__ == '__main__'):
  main()
