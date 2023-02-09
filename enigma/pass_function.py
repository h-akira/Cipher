#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Feb, 16, 2021 10:19:16 by hiroto akira
# $Author$
# $Date$
# $URL$
__giturl__ = "$URL$"

import numpy
import sys
import pickle

# 文字列と秘密鍵を引数とし, 暗号化（復号化）された文字列を返す. 
def conversion(str_input,key1,key2,key3):
  """
  conversion_text=list(f_read) #テキストを一文字ずつのリストにする. 
  f.close()
  """
  fp = open('charactor','rb') #文字と番号の対応を読み込む. 
  charactor = pickle.load(fp)
  n=len(charactor)
  fp.close()

  fp = open('data','rb') #暗号機のデータを読み込む. 
  data = numpy.fromfile(fp,dtype='>i4')
  data = data.reshape(n,4)
  fp.close()
  
  str_list = list(str_input)
  
  key=[]
  key.append(key1)
  key.append(key2)
  key.append(key3)

  #初期位置の入力を反映
  for i in range(len(key)):
    key[i]=key[i]%n
    for j in range(key[i]):
      rotation_sp(data,i)


  str_list = encryption(str_list,data,charactor)
  str_output = ''.join(str_list)
  #print('変換結果は以下の通りです. \n', str_output)

  return str_output

#変換する関数
def encryption(str_list,data,charactor):

  r_count = 0  #設定された初期位置から何回ローターを回転させてか=何文字目か. 
  #print(str_list)
  n_list = len(str_list)
  #文字列を数字に変換する. 
  
  n = len(charactor)

  conversion_text = []
  for i in range(n):
    conversion_text.append(charactor[i])

  #変換開始
  for j in range(n_list):
    #変換可能な文字である場合のみ変換を行う. 
    #変換可能な文字である場合, 処理のため番号に変換する. 
    if str_list[j] in conversion_text:
      str_list[j] = conversion_text.index(str_list[j])
      #番号の交換を行う. 
      for i in range(4):
        str_list[j] = data[str_list[j],i]
        #print(str_list)
      for i in range(3):
        array_where = numpy.where(data[:,2-i] == str_list[j])
        str_list[j] = array_where[0][0]
      #番号を文字に戻す. 
      str_list[j] = conversion_text[str_list[j]]
      
      r_count += 1
      #ローターを回転させる. 
      data = rotation(data,r_count)
  return str_list


#ローターを回転
def rotation(data,r_count):
  #global r_count
  
  n = len(data)

  #一つ目のローターを回転する.    
  data = rotation_sp(data,0)
 
  #二つ目のローターを回転する. 
  if r_count % n == 0:
    data = rotation_sp(data,1)
  
  #三つ目のローターを回転する. 
  if r_count % (n**2) == 0:
    data = rotation_sp(data,2)
    
  #r_count += 1
  
  #print(r_count)
  
  return data

#特定のローターを指定して回転
def rotation_sp(data,col):
  k= data[0,col]
  n = len(data)
  for i in range(n-1):
    data[i,col]=data[i+1,col]
  data[n-1,col]=k
  return data

