# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 14:03
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : main.py
# @Software: PyCharm

import package.app_change
import package.base
import time
import getopt
import sys


def help_text():
    help_text = """
    -h, --help          check the help text
    -s, --skip          the step you want you skip, eg. -skip=23
                          1: data_extract
                          2: data_calculate
                          3: json_update
    -i, --include        the step you want to run, eg.--include=012
                          0: standard_extract:  default not to run
    -a, --apply          change the program according to settings.json
    """
    return help_text


def get_opt(argv):
    apply, step0, step1, step2, step3 = False, False, True, True, True
    try:
        options, args = getopt.getopt(argv, "hs:i:a", ["help", "skip=", "include=", "apply"])
    except getopt.GetoptError:
        sys.exit()
    for option, value in options:
        if option in ("-h", "--help"):
            print(help_text())
        if option in ("-s", "--skip"):
            step1 = False if "1" in value else True
            step2 = False if "2" in value else True
            step3 = False if "3" in value else True
        if option in ("-i", "--include"):
            step0 = True if "0" in value else False
            step1 = True if "1" in value else False
            step2 = True if "2" in value else False
            step3 = True if "3" in value else False
        if option in ("-a", "--apply"):
            apply = True

    print("error args: {0}".format(args))
    return apply, step0, step1, step2, step3


if __name__ == '__main__':
    apply, step0, step1, step2, step3 = get_opt(sys.argv[1:])
    ws = package.base.WorkflowStart()
    t0 = time.time()
    # apply：编码修改，数据库连接修改，epf中oracle的路径修改
    if apply:
        package.app_change.FileEncoding()
        package.app_change.DataBaseChange()
        package.app_change.EPFChange()
    # 第零步：标准抽取
    if step0:
        dir_list = [ws.path_standard]
        ws.create_path(dir_list)
        ws.start_workflow('standard_extract')  # 在order中找顺序，并启动
    # 第一步：抽取数据
    if step1:
        ws.start_workflow('data_extract')  # 在order中找顺序，并启动
    # 第二步：数据计算
    if step2:
        dir_list = [ws.path_source_punish,
                    ws.path_source_power,
                    ws.path_source_enforcepeo,
                    ws.path_source_org,
                    ws.path_source_sub,
                    ws.path_source_law]
        ws.create_path(dir_list)
        ws.start_workflow('data_calculate')
    # 第三步：数据更新
    if step3:
        package.base.PyStart()
    print('All-Done')
    print(f'----{time.time()-t0} seconds----')
