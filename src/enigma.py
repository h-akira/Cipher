#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: 2023-02-14 11:30:56

# Import
import sys
import os
import random

class Rotor:
  def __init__(self,target="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    self.__class__.target = list(target)
  def generate(self,output):
    if os.path.isfile(output):
      if "y"!=input(f"`{output}` is exists. Overwite? (y/other):"):
        print("Stop processing.")
        sys.exit()
    self.input =  random.sample(self.__class__.target,len(self.__class__.target))
    while True:
      self.output = random.sample(self.input,len(self.input))
      for i,j in zip(self.input,self.output):
        if i==j:
          break
      else:
        break
    with open(output,mode="w") as f:
      print("".join(self.input),file=f)
      print("".join(self.output),file=f)
  def read_file(self,filename):
    with open(filename,mode="r") as f:
      data = f.readlines()
      self.input = list(data[0][:-1])
      self.output = list(data[1][:-1])
    self.check()
  def check(self):
    check_list = self.__class__.target.copy()
    for i in self.input:
      try:
        check_list.pop(check_list.index(i))
      except:
        print("The format of the rotor is wrong")
        sys.exit()
    else:
      if len(check_list) != 0:
        print("The format of the rotor is wrong")
        sys.exit()
    check_list = self.__class__.target.copy()
    for i in self.output:
      try:
        check_list.pop(check_list.index(i))
      except:
        print("The format of the rotor is wrong")
        sys.exit()
    else:
      if len(check_list) != 0:
        print("The format of the rotor is wrong")
        sys.exit()
    for i,j in zip(self.input,self.output):
      if i==j:
        print("The format of the rotor is wrong")
        sys.exit()
  def rotate(self,n=1):
    for i in range(n):
      self.input.insert(0,self.input.pop(-1))
      self.output.insert(0,self.output.pop(-1))
  def convert(self,s,reverse=False):
    if reverse:
      return self.__class__.target[self.input.index(self.output[self.__class__.target.index(s)])]
    else:
      return self.__class__.target[self.output.index(self.input[self.__class__.target.index(s)])]

class Reflector:
  def __init__(self,target="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    self.__class__.target = list(target)
  def generate(self,output):
    if os.path.isfile(output):
      if "y"!=input(f"`{output}` is exists. Overwite? (y/other):"):
        print("Stop processing.")
        sys.exit()
    check_list = self.__class__.target.copy()
    self.input = []
    self.output = []
    for i in range(len(self.__class__.target)//2):
      self.input.append(check_list.pop(random.randint(0,len(check_list)-1)))
      self.output.append(check_list.pop(random.randint(0,len(check_list)-1)))
      self.input.append(self.output[-1])
      self.output.append(self.input[-2])
    if len(check_list) != 0:
      print("Filed to generate a reflector.")
      sys.exit()
    with open(output,mode="w") as f:
      print("".join(self.input),file=f)
      print("".join(self.output),file=f)
  def read_file(self,filename):
    with open(filename,mode="r") as f:
      data = f.readlines()
      self.input = list(data[0][:-1])
      self.output = list(data[1][:-1])
  def convert(self,s):
    return self.output[self.input.index(s)]

class Enigma:
  def __init__(self,dirname=".enigma",rotor_files=["rotor1.txt","rotor2.txt","rotor3.txt"],reflector_file="reflector.txt",target="ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    self.dirname = dirname
    self.__class__.target = list(target)
    self.rotors = [Rotor(target),Rotor(target),Rotor(target)]
    self.reflector = Reflector(target)
    self.__class__.rotor_files = rotor_files
    self.__class__.reflector_file = reflector_file
    self.number = len(self.__class__.target)
    self.counter = [0,0,0]
  def keygen(self):
    if not os.path.isdir(self.dirname):
      os.makedirs(self.dirname)
    for rotor,filename in zip(self.rotors,self.__class__.rotor_files):
      rotor.generate(os.path.join(self.dirname,filename))
    self.reflector.generate(os.path.join(self.dirname,self.__class__.reflector_file))
  def read_dir(self,positions=[0,0,0]):
    for rotor,filename,p in zip(self.rotors,self.__class__.rotor_files,positions):
      rotor.read_file(os.path.join(self.dirname,filename))
      rotor.rotate(p)
    self.reflector.read_file(os.path.join(self.dirname,self.__class__.reflector_file))
  def rotate(self):
    for i,rotor in enumerate(self.rotors):
      rotor.rotate()
      self.counter[i]+=1
      if self.counter[i]==self.number:
        self.counter[i]=0
      else:
        break
  def convert(self,s):
    for rotor in self.rotors:
      s = rotor.convert(s,reverse=False)
    s = self.reflector.convert(s)
    for rotor in reversed(self.rotors):
      s = rotor.convert(s,reverse=True)
    return s
  def encryption(self,text,upper=True):
    if upper:
      text = text.upper()
    new_text = ""
    for s in list(text): if s in self.__class__.target:
        new_text += self.convert(s)
        self.rotate()
      else:
        new_text += s
    return new_text

def parse_args():
  import argparse
  parser = argparse.ArgumentParser(description="""\
This is enigma cipher machine.
""", formatter_class = argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("--version", action="version", version='%(prog)s 0.0.1')
  parser.add_argument("-e", "--enigma", metavar="enigma-dir", default=".enigma", help="enigma dirctry")
  parser.add_argument("-o", "--output", metavar="output-file", default="output.txt", help="output file")
  parser.add_argument("-p", "--positions", metavar="position", nargs=3, type=int, default=[0,0,0], help="starting position of each rotor")
  parser.add_argument("-g", "--keygen", action="store_true", help="generate key")
  parser.add_argument("-i", "--input", metavar="input-file", default="input.txt", help="input file")
  # parser.add_argument("file", metavar="input-file", help="input file")
  options = parser.parse_args()
  return options

def main():
  options = parse_args()
  enigma = Enigma(options.enigma)
  if options.keygen:
    enigma.keygen()
    sys.exit()
  enigma.read_dir(options.positions)
  with open(options.input,mode="r") as f:
  # with open(options.file,mode="r") as f:
    text = f.read()[:-1]
  new_text = enigma.encryption(text)
  with open(options.output,mode="w") as f:
    print(new_text,file=f)

if __name__ == '__main__':
  main()
