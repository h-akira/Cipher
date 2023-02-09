#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Created: Mar, 02, 2021 02:22:45 by hiroto akira
# $Author$
# $Date$
# $URL$
__giturl__ = "$URL$"


# text中にwordが存在した場合, その開始位置をリストで返す. 


def including(text,word):
  text_list = list(text)
  word_list = list(word)
  nt = len(text_list)
  nw = len(word_list)
  return_list=[]

  for i in range(nt-nw+1):    
    for j in range(nw):
      if text_list[i+j] == word_list[j]:
        if j == nw-1:
          return_list.append(i)
          break
        else:
          continue
      else:
        break
  return return_list

"""
a = including('text is sadfgtextadsgfxtext','text')
print(a)
"""

