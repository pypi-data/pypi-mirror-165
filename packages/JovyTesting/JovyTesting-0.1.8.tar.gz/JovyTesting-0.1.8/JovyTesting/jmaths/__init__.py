

import math
import numpy as np

def add(*args):
    """
    Add numbers together
    """
    args = np.array(list(args)).flat
    all_number_list = list(map(float,args))
    sum_result = sum(all_number_list)
    remainders = sum_result%int(sum_result)
    return int(sum_result) if remainders==0 else sum_result


def sub(*args):
    """
    Subtract numbers from each other
    """
    args = np.array(list(args)).flat
    all_number_list = list(map(float,args))
    diff_result = all_number_list[0]
    for number in all_number_list[1::]:
        diff_result -= number
    remainders = diff_result%int(diff_result)
    return int(diff_result) if remainders==0 else diff_result

subtract = sub