# -*- coding: utf-8 -*-
# @Date    : 3/2/18
# @Author  : zhangchaoyang

class Singleton(type):
    def __init__(cls,   class_name,base_classes, attr_dict):
        cls.__instance = None
        super(Singleton, cls).__init__( class_name,base_classes, attr_dict)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(Singleton, cls).__call__(*args, **kwargs)
            return cls.__instance
        else:
            return cls.__instance
