#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-01-03

# Import
import sys
import os

class Key:
  def gen_key(self, target="abcdefghijklmnopqrstuvwxyz"):
    import random
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

def encryption(text,key,decryption=False):
  output = ""
  for w in list(text):
    output += key.convert(w,decryption=decryption)
  return output

