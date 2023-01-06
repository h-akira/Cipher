#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-01-03

# Import
import sys
import os
import itertools
import sqlite3
import random

class Key:
  def gen_key(self, target="abcdefghijklmnopqrstuvwxyz"):
    self.target = list(target)
    self.conversion = random.sample(self.target, len(self.target))
    self.key_check()
  def read_key(self, file_name):
    with open(file_name, mode='r') as f:
      data = f.readlines()
    self.target = list(data[0][:-1])
    self.conversion = list(data[1][:-1])
    self.key_check()
  def save_key(self, file_name):
    with open(file_name, mode='w') as f:
      print("".join(self.target), file=f)
      print("".join(self.conversion), file=f)
  def empty_key(self):
    self.target = []
    self.conversion = []
  def add_pair(self, target, conversion):
    if len(target) != len(conversion):
      raise ValueError
    else:
      if target.__class__ is str:
        self.target += list(target)
      else:
        self.target += target
      if conversion.__class__ is str:
        self.conversion += list(conversion)
      else:
        self.conversion += conversion
  def convert(self,w,decryption=False):
    if not decryption:
      try:
        return self.conversion[self.target.index(w)]
      except ValueError:
        return w
    else:
      try:
        return self.target[self.conversion.index(w)]
      except ValueError:
        return w
  def key_check(self):
    if len(self.target) != len(self.conversion):
      raise ValueError
    for i,w in enumerate(self.target):
      try:
        if w not in self.conversion:
          raise ValueError
        if w in self.target[i+1:]:
          raise ValueError
      except IndexError:
        break
  def upper(self):
    self.target = list("".join(self.target).upper())
    self.conversion = list("".join(self.conversion).upper())
    self.key_check()
  def lower(self):
    self.target = list("".join(self.target).lower())
    self.conversion = list("".join(self.conversion).lower())
    self.key_check()

def add_key(key1, key2):
  key = Key()
  key.empty_key()
  key.add_pair(key1.target, key1.conversion)
  key.add_pair(key2.target, key2.conversion)
  return key

def encryption(text,key,decryption=False):
  output = ""
  for w in list(text):
    output += key.convert(w,decryption=decryption)
  return output

class CipherText:
  def read_text(self, file_name):
    with open(file_name, mode='r') as f:
      data = f.read()
    self.text = data[:-1]
    self.decrypted_text = self.text
    # self.div_text()
  def input_text(self):
    self.text = input("Cipher Text:")
    self.text = input("Cipher Text:")
    self.decrypted_text = self.text
    # self.div_text()
  def read_target(self, file_name):
    with open(file_name, mode='r') as f:
      data = f.read()
    self.target = list(data[:-1])
    self.target_check()
  def input_target(self):
    self.target = list(input("Conversion Target:"))
    self.target_check()
  def upper(self):
    self.target = list("".join(self.target).upper())
    self.target_check()
    self.text = self.text.upper()
  def lower(self):
    self.target = list("".join(self.target).lower())
    self.target_check()
    self.text = self.text.lower()
  def target_check(self):
    for i,w in enumerate(self.target):
      try:
        if w in self.target[i+1:]:
          raise ValueError
      except IndexError:
        break
  def update(self, key):
    self.decrypted_text = encryption(self.text, key, decryption=True)
    # self.div_text()
    for w in self.target:
      if w in key.target:
        self.target.remove(w)
  # def div_text(self):
    # self.words = [t for t in self.text.replace("\n"," ").replace(",","").replace(".","").replace("'", "").replace('"','').split(" ")]
    # self.decrypted_words = [t for t in self.decrypted_text.replace("\n"," ").replace(",","").replace(".","").replace("'", "").replace('"','').split(" ")]

def find_the_and(FA,CT,key):
  print("Now Serch 'The' and 'And':")
  try:
    THE, AND = sorted(FA.triple, key=lambda x: x[2], reverse=True)[:2]
  except AttributeError:
    FA.cal_triple()
    THE, AND = sorted(FA.triple, key=lambda x: x[2], reverse=True)[:2]
  print("\nFound Key:")
  if THE[0][0] in "abcdefghijklmnopqrstuvwxyz".upper():
    for i,j in zip(list("THEAND"), THE[0]+AND[0]):
      print(" "+i+"->"+j)
    key.add_pair("THEAND", THE[0]+AND[0])
  else:
    for i,j in zip(list("theand"), THE[0]+AND[0]):
      print(" "+i+"->"+j)
    key.add_pair("theand", THE[0]+AND[0])
  CT.update(key)
  print("-"*30)

class Dictionary:
  def __init__(self, dbfile):
    self.conn = sqlite3.connect(dbfile)
    self.cur = self.conn.cursor()
  def check(self, word):
    sql=f'SELECT COUNT(word) FROM items WHERE word="{word.lower()}"'
    self.cur.execute(sql)
    row = self.cur.fetchall()
    if row[0][0] > 0:
      return True
    else:
      return False
  def close(self):
    self.conn.close()
  def set_words(self, text, length = 3):
    words = [t for t in text.replace("\n"," ").replace(",","").replace(".","").replace("'", "").replace('"','').split(" ")]
    self.words=[]
    self.num = []
    for w in words:
      if w in self.words:
        self.num[self.words.index(w)] += 1
      else:
        self.words.append(w)
        self.num.append(1)
    self.full = sum(self.num)
  def cal_rate(self, key=None):
    score = 0
    if key:
      words = [encryption(w,key,decryption=True) for w,n in zip(self.words, self.num)]
    else:
      words = self.words
    for w,n in zip(words, self.num):
      if self.check(w):
        score += n
    return score/self.full*100

class FrequencyAnalysis:
  def __init__(self,CT):
    self.target = CT.target
    self.text = CT.text
  def calculate(self, target):
    appearance = []
    for w in target:
      appearance.append(self.text.count(w))
    frequency = []
    for i in appearance:
      frequency.append(i/sum(appearance)*100)
    return [[i,j,k] for i,j,k in zip(target, appearance, frequency)]
  def cal_single(self):
    target = self.target
    self.single = self.calculate(target)
    # print(sorted(self.single, key=lambda x: x[2], reverse=True))
  def cal_double(self):
    target = [i+j for i in self.target for j in self.target]
    self.double = self.calculate(target)
  def cal_triple(self):
    target = [i+j+k for i in self.target for j in self.target for k in self.target]
    self.triple = self.calculate(target)
  def set_general(self, general="eiatnsorldchumpfgywkvbjqxz".upper()):
    if general.__class__ is list:
      self.general = general  # 一般的な出現頻度順
    else:
      self.general = list(general)
    if len(self.general)!=len(self.target):
      raise ValueError
    for i,w in enumerate(self.general):
      try:
        if w in self.general[i+1:]:
          raise ValueError
      except IndexError:
        break

def brute_force(CT, FA, key, N, n, dic):
  text_frequency = []
  general_frequency = FA.general.copy()
  for w,a,f in sorted(FA.single, key=lambda x: x[2], reverse=True):
    text_frequency.append(w)
  for w in key.target:
    general_frequency.remove(w)
  for w in key.conversion:
    text_frequency.remove(w)
  # dic.set_words(CT.text)
  new = [None, 0]
  counter = 0
  print("Now Serch:")
  print(" "+"".join(general_frequency[:N]))
  print(" "+"".join(text_frequency[:N]))
  for target in itertools.permutations(general_frequency[:N]):
    temporary_key = Key()
    temporary_key.empty_key()
    temporary_key.add_pair("".join(target),"".join(text_frequency[:N]))
    temporary_key.add_pair("".join(general_frequency[N:]),"".join(text_frequency[N:]))
    temporary_key.add_pair("".join(key.target),"".join(key.conversion))
    rate = dic.cal_rate(temporary_key)
    if new[1] < rate:
      new = [temporary_key, rate]
    counter += 1
  print("\nFound Key:")
  for i in range(n):
    print(" "+new[0].target[i],"->",new[0].conversion[i])
  key.add_pair(new[0].target[:n], new[0].conversion[:n])
  CT.update(key)
  print("-"*30)
  # dic.set_words(CT)








