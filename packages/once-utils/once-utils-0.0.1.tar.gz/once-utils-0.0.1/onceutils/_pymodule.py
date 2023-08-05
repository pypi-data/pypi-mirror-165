# -*- coding: utf-8 -*-
# @Date:2022/08/27 0:35
# @Author: Lu
# @Description py module util
import os
import sys


def append_module(work_dir):
    """
    For import a xxx pylib, but it not in the same project or the work path, you should add the lib's path to sys environment
    :param work_dir: a path
    :return: None
    """
    curr_dir_path = os.path.abspath(os.path.dirname(__file__))
    end = curr_dir_path.find(work_dir)
    if end == -1:
        return
    end += work_dir + len(work_dir)
    work_path = curr_dir_path[:end]
    if work_dir not in sys.path:
        sys.path.append(work_path)
