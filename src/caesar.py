#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-01-03

# Import
import sys

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
シーザー暗号を暗号化・復号化，解読する．
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-s", "--secret-key", metavar="number", type=int, default=0, help="ずらす数")
  parser.add_argument("-p", "--public-key", metavar="key-file", help="アルファベット順が記述されたファイル")
  parser.add_argument("-i", "--input", metavar="input-file", help="入力ファイル")
  parser.add_argument("-o", "--output", metavar="output-file", help="出力ファイル")
  parser.add_argument("-l", "--letter-case", choices=['upper','lower','no'], default='upper', help="大文字と小文字を区別する")
  parser.add_argument("-d", "--decipher", action="store_true", help="解読モード")
  parser.add_argument("--language", metavar="language", default="en", help="言語（pycld2に依存）")
  options = parser.parse_args()
  return options

def encryption(text,sk=0,pk="abcdefghijklmnopqrstuvwxyz"):
  output = ""
  for w in list(text):
    if w in pk:
      i = pk.index(w)+sk
      while True:
        if i>=len(pk):
          i -= len(pk)
        elif i<-len(pk):
          i += len(pk)
        else:
          break
      output += pk[i]
    else:
      output += w
  
  return output

def decipher(text,pk="abcdefghijklmnopqrstuvwxyz",language="ENGLISH"):
  import pycld2
  new = [None,None,0]  # [鍵，解読された文，言語の割合]
  for i in range(len(pk)):
    t = encryption(text,i,pk)
    isReliable, textBytesFound, details = pycld2.detect(t)
    if details[0][0] == language or details[0][1] == language:
      if new[2] < details[0][2]:
        new = [i,t,details[0][2]]
  return new

def main():  
  # ArgumentParser
  options = parse_args()

  if options.input:
    with open(options.input,mode="r") as f:
      text = f.read()[:-1]
  else:
    text = input("入力:")

  if options.public_key:
    with open(options.public_key,mode="r") as f:
      pk = f.read()[:-1]
  else:
    pk = 'abcdefghijklmnopqrstuvwxyz'

  if options.letter_case == 'upper':
    text = text.upper()
    pk = pk.upper()
  elif options.letter_case == 'lower':
    text = text.lower()
    pk = pk.lower()

  for i,w in enumerate(list(pk)):
    try:
      if w in pk[i+1:]:
        print("鍵に重複があります．")
        sys.exit()
    except IndexError:
      break

  if not options.decipher:
    output = encryption(text,options.secret_key,pk)
  else:
    secret_key, output, rate = decipher(text,pk,options.language) 
    print(f"発見された鍵: {secret_key}")
    print(f"英語の割合: {rate}%")

  if options.output:
    with open(options.output, mode='w') as f:
      print(output, file=f)
  else:
    print(output)

if(__name__ == '__main__'):
  main()
