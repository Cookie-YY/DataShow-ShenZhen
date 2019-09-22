# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 13:11
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : theme2json_home.py
# @Software: PyCharm

"""所有内容不分是否公安！！！！！！！！！！！！！！！！！！！"""
from base import JsonUpdate
import pandas as pd
import os

ju = JsonUpdate()

aspect_home = ["punish", "org", "enforcepeo", "power"]  # 处罚案件/机关/人员/职权  分成各年和各年各区
aspect_home_ = ["", "_quyu"]
command_home = "!_year~_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_!, 'year~_isga.csv')))  # 读取各年"
for asp in aspect_home:
    for asp_ in aspect_home_:
        exec(command_home.replace("!", asp).replace("~", asp_))  # 罚案件/机关/人员/职权 的 各年和各年各区
punish_year_type_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_type_isga.csv')))  # 处罚案件分类的各年
punish_year_quyu_type_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu_type_isga.csv'))) # 处罚案件分类的各年各区
power_year_quyu_lawnumber_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_quyu_lawnumber_isga.csv')))  # 职权关联法律的各年
power_year_lawnumber_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_lawnumber_isga.csv')))  # 职权关联法律的各年各区
org_year_hangyenumber_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_org, 'year_hangyenumber_isga.csv')))  # 行业数
# 初始化方法
totalOfPunish, lawExecutor, annualPunish, powerNum = [], [], [], []
# 许可和检查现在没有数，但是需要填上假的
annualAllowance, annualInspection = [], []
# 地图？
mapData = []

#####################################################################################
# 1处罚案件量（各年 各年各区）totalOfPunish方法
# 处罚案件（各年）：
for group_name, group_data in punish_year_isga.groupby('YEAR'):
    totalOfPunish.append({"dep": "全区", "year": int(group_name), "value": ju.get_value(group_data, "SUM(*)")})
# 处罚案件（各年各区划）
for group_name, group_data in punish_year_quyu_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        totalOfPunish.append({"dep": group_name_, "year": int(group_name), "value": ju.get_value(group_data_, "SUM(*)")})

# 2 行业，领域，机关，人员，法律，lawExecutor方法
# 2.1 行业（各年）
for group_name, group_data in org_year_hangyenumber_isga.groupby('YEAR'):
    lawExecutor.append({"dep": "全区", "year": int(group_name), "name": "行业总数", "value": ju.get_value(group_data, "SUM(*)")})
# 2.2 行业（各年各区划）
for ind, year_ in enumerate(ju.order_year):
    for quyu_ in ju.order_quyu:
        lawExecutor.append({"dep": quyu_, "year": int(year_), "name": "行业总数", "value": lawExecutor[ind]['value']})
# 2.3 领域（如果不报错，就这样吧）需要填充内容，必须按顺序填，什么鬼
# 2.3.1 领域（各年）
for year_ in ju.order_year:
    lawExecutor.append({"dep": "全区", "year": int(year_), "name": "领域总数", "value": 1})
# 2.3.2 领域（各年各区划）
for year_ in ju.order_year:
    for quyu_ in ju.order_quyu:
        lawExecutor.append({"dep": quyu_, "year": int(year_), "name": "领域总数", "value": 1})
# 2.4 机关数（各年）
for group_name, group_data in org_year_isga.groupby('YEAR'):
    lawExecutor.append({"dep": "全区", "year": int(group_name), "name": "单位总数", "value": ju.get_value(group_data, "SUM(*)")})
# 2.4 机关数（各年各区划）
for group_name, group_data in org_year_quyu_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('ORG_QUYU'):
        lawExecutor.append({"dep": group_name_, "year": int(group_name), "name": "单位总数", "value": ju.get_value(group_data_, "SUM(*)")})
# 2.4 人员数（各年）
for group_name, group_data in enforcepeo_year_isga.groupby('YEAR'):
    lawExecutor.append({"dep": "全区", "year": int(group_name), "name": "人员总数", "value": ju.get_value(group_data, "SUM(*)")})
# 2.4 人员数（各年各区划）
for group_name, group_data in enforcepeo_year_quyu_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_QUYU'):
        lawExecutor.append({"dep": group_name_, "year": int(group_name), "name": "人员总数", "value": ju.get_value(group_data_, "SUM(*)")})
# 2.4 法律规范数（各年）
for group_name, group_data in power_year_lawnumber_isga.groupby('YEAR'):
    lawExecutor.append({"dep": "全区", "year": int(group_name), "name": "法律规范", "value": ju.get_value(group_data, "SUM(*)")})
# 2.4 法律规范数（各年各区划）
for group_name, group_data in power_year_quyu_lawnumber_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('POWER_QUYU'):
        lawExecutor.append({"dep": group_name_, "year": int(group_name), "name": "法律规范", "value": ju.get_value(group_data_, "SUM(*)")})
# 2.5 差职权 职权为啥不写在这里，非得单独的方法！！！！！！！！！

# 3 一般简易处罚案件量annualPunish方法：
# 一般简易处罚案件量（总）
for group_name, group_data in punish_year_type_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_TYPE'):
        group_name_ = ju.punishtype_mapping["chinese"][str(group_name_)]
        annualPunish.append({"dep": "全区", "year": int(group_name), "name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})

# 一般简易处罚案件量（分区划）
for group_name, group_data in punish_year_quyu_type_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        for group_name__, group_data__ in group_data_.groupby('PUNISH_TYPE'):
            group_name__ = ju.punishtype_mapping["chinese"][str(group_name__)]
            annualPunish.append({"dep": group_name_, "year": int(group_name), "name": group_name__, "value": ju.get_value(group_data__, "SUM(*)")})

# 4 职权数量powerNum方法
# 职权数量（各年）
for group_name, group_data in power_year_isga.groupby('YEAR'):
    powerNum.append({"dep": "全区", "year": int(group_name), "name": "职权总数", "value": ju.get_value(group_data, "SUM(*)")})
# 职权数量（各年各区划）
for group_name, group_data in power_year_quyu_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('POWER_QUYU'):
        powerNum.append({"dep": group_name_, "year": int(group_name), "name": "职权总数", "value": ju.get_value(group_data_, "SUM(*)")})

# 最后统一将没用的东西，填上
# 领域只能放到前面，有顺序限制
# 许可（各年）
for year_ in ju.order_year:
    for name_ in ["不予许可", "准予许可"]:
        annualAllowance.append({"dep": "全区", "year": int(year_), "name": name_, "value": 1})
# 许可（各年各区）
for year_ in ju.order_year:
    for quyu_ in ju.order_quyu:
        for name_ in ["不予许可", "准予许可"]:
            annualAllowance.append({"dep": quyu_, "year": int(year_), "name": name_, "value": 1})
# 检查（各年）
for year_ in ju.order_year:
    for name_ in ["双随机", "日常", "其他", "勘验", "专项"]:
        annualInspection.append({"dep": "全区", "year": int(year_), "name": name_, "value": 1})
# 检查（各年各区）
for year_ in ju.order_year:
    for quyu_ in ju.order_quyu:
        for name_ in ["双随机", "日常", "其他", "勘验", "专项"]:
            annualInspection.append({"dep": quyu_, "year": int(year_), "name": name_, "value": 1})

for year_ in ju.order_year:
    for quyu_ in [i for i in ju.order_quyu if i not in ['市级']]+["深汕特别合作区"]:
        mapData.append({"year": int(year_), "name": quyu_, "value": ju.home_map[quyu_]})
if __name__ == '__main__':
    content_dict_home = {
        "totalOfPunish": totalOfPunish,
        "lawExecutor": lawExecutor,
        "annualPunish": annualPunish,
        "powerNum": powerNum,
        # 补充的两个方法（目前没用的）
        "annualAllowance": annualAllowance,  # 年度许可
        "annualInspection": annualInspection,  # 年度检查
        "mapData": mapData}
    ju.json_io("home.json", content_dict_home)
