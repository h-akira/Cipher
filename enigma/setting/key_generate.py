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

  Yn = input("スクランブラーとリフレクターを生成します. 古いデータは消えますが本当に良いですか?(Y/n):")
  if Yn == 'Y':
    f = open('text-number.txt', 'r')
    f_read=f.read()
    conversion_text=list(f_read)
    f.close()
    #print(conversion_text)
    #改行を含むか尋ねる. 
    terms=input('変換対象の文字に改行は含まれますか？[Y/n]:')
    if terms=='Y':
      n=len(conversion_text)
    elif terms=='n':
      n=len(conversion_text)
      conversion_text.pop(n-1)
      n=n-1
    else:
      print('エラーが発生しました. ')
      sys.exit()

    if n%2==1:
      print('変換対象の文字の種類は偶数にしてください. ')
      sys.exit()

      
    scrambler1 = rand_int_no(0, n-1, n)
    #print(scrambler1)
    #scrambler1.tofile('scrambler1')

    scrambler2 = rand_int_no(0, n-1, n)
    #print(scrambler1)
    #scrambler2.tofile('scrambler2')

    scrambler3 = rand_int_no(0, n-1, n)
    #print(scrambler1)
    #scrambler3.tofile('scrambler3')

    refrector = []
    for i in range(n):
      if i in refrector:
        i_index = refrector.index(i)
        refrector.append(i_index)
      else:
         while True:
           nw = random.randint(i+1, n-1)
           if not nw in refrector:
             refrector.append(nw)
             break
        
    data = numpy.zeros((n,4), dtype=">i4")
    charactor = numpy.empty(n,dtype='unicode')
    
    for i in range(n):
      data[i,0] = scrambler1[i]
      data[i,1] = scrambler2[i]
      data[i,2] = scrambler3[i]
      data[i,3] = refrector[i]
      charactor[i] = conversion_text[i]
    print('スクランブラーとリフレクターは以下の通りです. \n',data)
    print('変換の対象となる文字の一覧は以下の通りです. ',charactor)
    data.tofile('data')
    #charactor.save('charactor')
    f = open('charactor','wb')
    pickle.dump(conversion_text,f)
    f.close()


    print("生成しました. ")

def rand_int_no(a, b, k):
  ns = []
  while len(ns) < k:
    n = random.randint(a, b)
    if not n in ns:
      ns.append(n)
  return ns

if(__name__ == '__main__'):
  main()
