#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:14:51 2023

@author: caesar [who is caesar?]
"""

# takes a number or string as input and outputs the numbers it contains
# as string of Unicode superscripts or subscripts

# a hyphen - is converted to a super- or subscript minus which can be used
# as a separator since there is no super-/subscript punctuation

# the function could be extended to also convert letters, although not all
# capital letters are available as super- or subscript in Unicode

def sup(input):
    output = ""
    for i in range(len(str(input))):
        if str(input)[i] == "0":
            output = output + "⁰"
        elif str(input)[i] == "1": 
            output = output + "¹"
        elif str(input)[i] == "2": 
            output = output + "²"
        elif str(input)[i] == "3": 
            output = output + "³"
        elif str(input)[i] == "4": 
            output = output + "⁴"
        elif str(input)[i] == "5": 
            output = output + "⁵"
        elif str(input)[i] == "6": 
            output = output + "⁶"
        elif str(input)[i] == "7": 
            output = output + "⁷"
        elif str(input)[i] == "8": 
            output = output + "⁸"
        elif str(input)[i] == "9": 
            output = output + "⁹"
        elif str(input)[i] == "-":
            output = output + "⁻"
        else:
            pass
    return output
    
def sub(input):
    output = ""
    for i in range(len(str(input))):
        if str(input)[i] == "0":
            output = output + "₀"
        elif str(input)[i] == "1": 
            output = output + "₁"
        elif str(input)[i] == "2": 
            output = output + "₂"
        elif str(input)[i] == "3": 
            output = output + "₃"
        elif str(input)[i] == "4": 
            output = output + "₄"
        elif str(input)[i] == "5": 
            output = output + "₅"
        elif str(input)[i] == "6": 
            output = output + "₆"
        elif str(input)[i] == "7": 
            output = output + "₇"
        elif str(input)[i] == "8": 
            output = output + "₈"
        elif str(input)[i] == "9": 
            output = output + "₉"
        elif str(input)[i] == "-":
            output = output + "₋"
        else:
            pass
    return output
