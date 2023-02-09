#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Feb, 16, 2021 10:19:16 by hiroto akira
# $Author$
# $Date$
# $URL$
__giturl__ = "$URL$"

import random
import numpy
import sys
import pickle

def main():
  filename = input('ファイル名:')
  f = open(filename, 'r')
  f_read=f.read()
  text=list(f_read)
  f.close()

  small_list = list('abcdefghijklmnopqrstuvwxyz')
  large_list = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
  
  n = len(text)

  for i in range(n):
    if text[n-1-i] in small_list:
      text[n-1-i] = large_list[small_list.index(text[n-1-i])]
    elif text[n-1-i] in large_list:
      pass 
    else:
      text.pop(n-1-i)
    
  text_output = ''.join(text)
  filename_output=input("出力ファイル名:")
  with open(filename_output, mode='w') as fo:
    fo.write(text_output)

if(__name__ == '__main__'):
  main()
