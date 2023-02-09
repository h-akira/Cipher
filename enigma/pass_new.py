#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Mar, 02, 2021 03:14:42 by hiroto akira
# $Author$
# $Date$
# $URL$
__giturl__ = "$URL$"

def main():
  import pass_function as pf
  #import decoding_function as df
  import sys

  content = input("直接入力(d) or ファイル名(f):")
  if content == 'd':
    str_input = input("文字列:")
  elif content == 'f':
    f_name=input("ファイル名:")
    f = open(f_name, 'r')
    str_input = f.read()
    print('読み込んだ文字列は以下の通りです. \n',str_input)
    f.close()
  else:
    print('エラーが発生しました. ')
    sys.exit()
  key1=int(input("key1:"))
  key2=int(input("key2:"))
  key3=int(input("key3:"))

  # 変換を実行
  str_output = pf.conversion(str_input,key1,key2,key3)

  print('変換結果は以下の通りです. \n', str_output)
  if_output=input('ファイルに出力しますか？[Y/n]:')
  if if_output == 'Y':
    f_output=input("出力ファイル名:")
    with open(f_output, mode='w') as f:
      f.write(str_output)

if(__name__ == '__main__'):
  main()
