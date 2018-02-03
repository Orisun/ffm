# -*- coding: utf-8 -*-
# @Date    : 3/2/18
# @Author  : zhangchaoyang

import numpy as np
import math
from singleton import Singleton


class Logistic(object):
    __metaclass__ = Singleton  # 单例

    def __init__(self):
        exp_max = 10.0
        self.exp_scale = 0.001
        self.exp_intv = int(exp_max / self.exp_scale)
        self.exp_table = [0.0] * self.exp_intv
        for i in xrange(self.exp_intv):
            x = self.exp_scale * i
            exp = math.exp(x)
            self.exp_table[i] = exp / (1.0 + exp)

    def decide_by_table(self, x):
        '''查表获得logistic的函数值'''
        if x == 0:
            return 0.5
        i = int(np.nan_to_num(abs(x) / self.exp_scale))
        y = self.exp_table[min(i, self.exp_intv - 1)]
        if x > 0:
            return y
        else:
            return 1.0 - y

    def decide_by_tanh(self, x):
        '''直接使用1.0 / (1.0 + np.exp(-x))容易发警告“RuntimeWarning: overflowencountered in exp”，
           转换成如下等价形式后算法会更稳定
        '''
        return 0.5 * (1 + np.tanh(0.5 * x))

    def decide(self, x):
        '''原始的sigmoid函数'''
        return 1.0 / (1.0 + np.exp(-x))


if __name__ == '__main__':
    log = Logistic()
    for x in np.arange(-20, 20, 0.1):  # xrange()中的step不能是小数，所以只好手numpy.arange()
        y = log.decide(x)
        print x, y, log.decide_by_tanh(x) - y, log.decide_by_table(x) - y
