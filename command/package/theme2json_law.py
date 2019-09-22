# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 11:11
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : theme2json_enforcepeo.py
# @Software: PyCharm

"""所有内容不分是否公安！！！！！！！！！！！！！！！！！！！"""
from base import JsonUpdate
import pandas as pd
import os

ju = JsonUpdate()

# 读取高低频
law_year_highlow_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_highlow_isga.csv')))
law_year_type_highlow_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_type_highlow_isga.csv')))
# 读取新增
law_year_new_type_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_new_type_isga.csv')))
# 读取分类
law_year_type_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_type_isga.csv')))
# 读取各行业（各区划）使用法律数//各行业（各区划）法律数
law_year_hangye_use_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_hangye_use_isga.csv')))
law_year_hangye_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_hangye_lawnumber_isga.csv')))
law_year_hangye_quyu_use_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_law, 'year_hangye_quyu_use_isga.csv')))
law_year_hangye_quyu_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_hangye_quyu_lawnumber_isga.csv')))

leftLawTotal = []  # 初始化左侧
saflfgfx = []  # 初始化高低频
lawsRatio = []  # 法律分类分析
increaseLaw = []  # 初始化新增
tradeLawsImplement, tradeLawsImplementErji = [], []


# 涉案法律规范分析（高低频）
for group_name, group_data in law_year_type_highlow_isga.groupby('YEAR'):
    content_type = {"year": int(group_name)}
    data_type = []
    for group_name_, group_data_ in group_data.groupby('LAW_TYPE'):
        data_one = {
            "order": ju.order_law_typerank[group_name_],
            "name": group_name_,
            "gp": ju.get_value(group_data_, "HIGH", 100),
            "dp": ju.get_value(group_data_, "LOW", 100),
            "wsa": ju.get_value(group_data_, "NO_USE", 100)}
        data_type.append(data_one)
    content_type["data"] = data_type
    saflfgfx.append(content_type)

# 法律分类占比统计
for group_name, group_data in law_year_type_isga.groupby('YEAR'):
    law_type_data = []
    for group_name_, group_data_ in group_data.groupby('LAW_TYPE'):
        law_type_data.append({"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})
    lawsRatio.append({"year": int(group_name), "data": law_type_data})


# 新增：
for group_name, group_data in law_year_new_type_isga.groupby('YEAR'):
    increase = {"name": str(int(group_name)) + '年'}
    for group_name_, group_data_ in group_data.groupby('LAW_TYPE'):
        increase[ju.lawtype_mapping[group_name_]] = ju.get_value(group_data_, "SUM(*)")
    increaseLaw.append(increase)

# 法律规范履行率（各行业）
for group_data1, group_data2 in zip(law_year_hangye_use_isga.groupby('YEAR'), law_year_hangye_isga.groupby('YEAR')):
    law_use_data = []
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_HANGYE'), ju.get_df(group_data2).groupby('POWER_HANGYE')):
        law_use_data.append({"name": group_data1_[0],
                             "total": ju.get_value(ju.get_df(group_data2_), "SUM(*)"),
                             "value": ju.get_value(ju.get_df(group_data1_), "SUM(*)")})
    tradeLawsImplement.append({"year": int(group_data1[0]), "data": law_use_data})
# 法律规范履行率（各行业各区划）
for group_data1, group_data2 in zip(law_year_hangye_quyu_use_isga.groupby('YEAR'), law_year_hangye_quyu_isga.groupby('YEAR')):
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_HANGYE'), ju.get_df(group_data2).groupby('POWER_HANGYE')):
        law_use_data = []
        for group_data1__, group_data2__ in zip(ju.get_df(group_data1_).groupby('PUNISH_QUYU'), ju.get_df(group_data2_).groupby('POWER_QUYU')):
            law_use_data.append({"name": group_data1__[0],
                                 "total": ju.get_value(ju.get_df(group_data2__), "SUM(*)"),
                                 "value": ju.get_value(ju.get_df(group_data1__), "SUM(*)")})
        tradeLawsImplement.append({"year": int(group_data1[0]), "dep": group_data1_[0], "data": law_use_data})
# 左侧
for group_name, group_data in law_year_highlow_isga.groupby('YEAR'):
    content = {"year": int(group_name)}
    content["data"] = [
        {"name": "职权关联法律总数", "value": ju.get_value(group_data, "SUM(*)")},
        {"name": "涉案法律总数", "value": ju.get_value(group_data, "USE")},
        {"name": "未涉案法律总数", "value": ju.get_value(group_data, "NO_USE")},
        {"name": "高频触发法律总数", "value": ju.get_value(group_data, "HIGH")},
        {"name": "低频触发法律总数", "value": ju.get_value(group_data, "LOW")}]
    leftLawTotal.append(content)


if __name__ == '__main__':
    content_dict_law = {
        "leftLawTotal": leftLawTotal,
        "saflfgfx": saflfgfx,
        "lawsRatio": lawsRatio,
        "increaseLaw": increaseLaw,
        "tradeLawsImplement": tradeLawsImplement,
        "tradeLawsImplementErji": tradeLawsImplementErji}
    ju.json_io("law.json", content_dict_law)

