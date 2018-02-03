# -*- coding: utf-8 -*-
# @Date    : 3/2/18
# @Author  : zhangchaoyang

import math
from ffm import FFM_Node, FFM
import re


class Sample(object):
    def __init__(self, infile):
        self.infile = infile
        self.regex = re.compile("\\s+")

    def __iter__(self):
        with open(self.infile, 'r') as f_in:
            for line in f_in:
                arr = self.regex.split(line.strip())
                if len(arr) >= 2:
                    y = float(arr[0])
                    assert math.fabs(y) == 1
                    node_list = []
                    square_sum = 0.0
                    for i in xrange(1, len(arr)):
                        brr = arr[i].split(",")
                        if len(brr) == 3:
                            j = int(brr[0])
                            f = int(brr[1])
                            v = float(brr[2])
                            square_sum += v * v
                            node_list.append(FFM_Node(j, f, v))
                    if square_sum > 0:
                        norm = math.sqrt(square_sum)
                        # 把模长缩放到1
                        normed_node_list = [FFM_Node(ele.j, ele.f, ele.v / norm) for ele in node_list]
                        yield (normed_node_list, y)


if __name__ == '__main__':
    n = 5
    m = 2
    k = 2
    train_file = "train.txt"
    valid_file = "valid.txt"
    model_file = "ffm.npy"
    # 超参数
    eta = 0.05
    lambd = 1e-3
    max_echo = 30
    max_r2 = 0.9

    # 训练模型，并保存模型参数
    sample_generator = Sample(train_file)
    ffm = FFM(m, n, k, eta, lambd)
    ffm.train(sample_generator, max_echo, max_r2)
    ffm.save_model(model_file)

    # 加载模型，并计算在验证集上的拟合效果
    ffm.load_model(model_file)
    valid_generator = Sample(valid_file)
    y_sum = 0.0
    y_square_sum = 0.0
    err_square_sum = 0.0  # 误差平方和
    population = 0  # 样本总数
    for node_list, y in valid_generator:
        y = 0.0 if y == -1 else y  # 真实的y取值为{-1,1}，而预测的y位于(0,1)，计算拟合效果时需要进行统一
        y_hat = ffm.predict(node_list)
        y_sum += y
        y_square_sum += y ** 2
        err_square_sum += (y - y_hat) ** 2
        population += 1
    var_y = y_square_sum - y_sum * y_sum / population  # y的方差
    r2 = 1 - err_square_sum / var_y
    print "r2 on validation set is", r2
