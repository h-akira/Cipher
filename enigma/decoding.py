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
  import decoding_function as df
  import sys
  import pickle

  #####################################################
  # 以下を設定してください. 
  filename = 'aaa'  # 暗号文のファイル名
  word = ['and','the']  # 探索キーワード
  low_limit = 2  # 記録する時の探索キーワードの最低個数
  key_number = 62  # 変換対象の文字の種類の数
  start = 0  # 探索を開始する文字の位置
  end = 200  # 探索を終了する文字の位置
  #####################################################
  
  # 処理を開始します.   
  key1 = 0
  key2 = 0
  key3 = 0
  if len(word) < 1 :
    print('探索する語句をリストで指定してください. ')
    sys.exit()
  f = open(filename,'r')
  str_input = f.read()
  f.close()

  str_list = list(str_input) 
  tn = len(str_list) # 入力された文字列の文字数
  
  if start > end or end >= tn-1 or start < 0:
    print('キーワード探索の範囲を確認してください. ')
    sys.exit()
  
  # 探索の範囲外を削除をします. 不要である場合はコメントアウトしてください. 
  if tn-1 != end:
    for i in range(tn-end-1):
      str_list.pop()
  if start != 0:
    for i in range(start):
      str_list.pop(0)
  str_input = ''.join(str_list)

  candidate = []

  # 探索を行います. 
  for i in range(key_number**3):
    decoded_text = pf.conversion(str_input,key1,key2,key3)
    a = 0
    for j in range(len(word)):
      b = df.including(decoded_text,word[j])
      a += len(b)
    if a>=low_limit:
      # 配列を用いる場合はコメントアウトを解除すること. 
      # candidate.append([key1,key2,key3,a])
      print('key1:',key1,'key2:',key2,'key3:',key3)
      print('発見されたキーワードの個数:',a,'個')
      print('復号文:',decoded_text)
      
    key3 += 1
    if (i+1) % key_number == 0:
      key2 += 1
      key3 = 0
    if (i+1) % (key_number**2) == 0:
      print('key1が',key1,'の時の試行は完了しました. ')
      key1 += 1
      key2 = 0
  print('全ての試行が終了しました. ')
  
  """
  if len(candidate)==0:
    print('秘密鍵の候補は見つかりませんでした. ')
  else:
    print('秘密鍵の候補は以下の通りです. ')
    for i in range(len(candidate)):
      print('key1:',candidate[i][0],'key2:',candidate[i][1],'key3:',candidate[i][2])
      print('発見されたキーワードの個数:',candidate[i][3],'個')
      print('復号文:',pf.conversion(str_input,candidate[i][0],candidate[i][1],candidate[i][2]))
  """
  """  
    f = open('chandidate','wt')
    pickle.dump(candidate,f)
    f.close()
    print('秘密鍵の候補をファイルに出力しました. ')
  """
if(__name__ == '__main__'):
  main()
