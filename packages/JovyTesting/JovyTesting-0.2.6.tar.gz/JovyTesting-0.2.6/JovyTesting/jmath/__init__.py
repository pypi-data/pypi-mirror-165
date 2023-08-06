

import math
import numpy as np

__all__ = ["add", "sub", "mult", "div", "subtract", "divide", "multiply"]

#Defining Functions
def add(*args):
    """
    Add numbers together
    """
    args2 = list(np.array(args).flat)
    all_number_list = list(map(float,args2))
    sum_result = sum(all_number_list)
    remainders = sum_result%int(sum_result)
    return int(sum_result) if remainders==0 else sum_result


def sub(*args):
    """
    Subtract numbers from each other
    """
    args = np.array(args).flat
    all_number_list = list(map(float,args))
    diff_result = all_number_list[0]
    for number in all_number_list[1::]:
        diff_result -= number
    remainders = diff_result%int(diff_result)
    return int(diff_result) if remainders==0 else diff_result


def mult(*args):
    """
    Multiply numbers with each other
    """
    args = np.array(args).flat
    all_number_list = list(map(float,args))
    mult_result = all_number_list[0]
    for number in all_number_list[1::]:
        mult_result *= number
    remainders = mult_result%int(mult_result)
    return int(mult_result) if remainders==0 else mult_result

def div(*args):
    """
    Divide numbers with each other
    """
    args = np.array(args).flat
    all_number_list = list(map(float,args))
    div_result = all_number_list[0]
    for number in all_number_list[1::]:
        div_result /= number
    return div_result
    

#Cloning Functions
subtract = sub
multiply = mult
divide = div