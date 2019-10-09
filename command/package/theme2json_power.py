# -*- coding: utf-8 -*-
# @Time    : 2019/8/28 11:30
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : theme2json_power.py
# @Software: PyCharm

"""所有内容不分是否公安！！！！！！！！！！！！！！！！！！！"""
from base import JsonUpdate
import pandas as pd
import os

ju = JsonUpdate()

aspect_power = ["_hangye_type", "_quyu_type", "_hangye_quyu_type", "_type", "", "_lawnumber", "_lawitemnumber", "_lawtype"]
command_power = "power_year%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year%_isga.csv')))  # 读取各年"
for asp in aspect_power:
    exec(command_power.replace("%", asp))
punish_year_power_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_power_isga.csv')))
punish_year_hangye_power_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye_power_isga.csv')))
punish_year_quyu_power_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu_power_isga.csv')))
punish_year_hangye_quyu_power_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye_quyu_power_isga.csv')))

#####################################################################################
# 初始化：类别总数/左侧总数（总，法，依）/各区划各类别，各行业各类别
powerGenre, leftPowerTotal = [], [],
cityPower, tradePower = [], []
tradePowerErji, cityPowerErji = [], []
tradeDormancy, cityDormancy = [], []
tradeDormancyErji, cityDormancyErji = [], []
powerSource = []
leftPunishRateOfPower = []

# 全行业职权分析：tradePower方法 分的行业在data里面？？？？？？？？？？？？？？？？？？？？
for group_name, group_data in power_year_hangye_type_isga.groupby('YEAR'):
    trade_one = []
    for group_name_, group_data_ in group_data.groupby('POWER_HANGYE'):
        trade_hangye_one = {"department": group_name_}
        for group_name__, group_data__ in group_data_.groupby('POWER_TYPE'):
            trade_hangye_one[ju.powertype_mapping[group_name__]] = ju.get_value(group_data__, 'SUM(*)', jduge_sum=True)
        trade_one.append(trade_hangye_one)
    tradePower.append({"year": int(group_name), "data": trade_one})
# 全行业职权分析(二级）tradePowerErji方法：
for group_name, group_data in power_year_hangye_quyu_type_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('POWER_HANGYE'):
        hangyequyu = []
        for group_name__, group_data__ in group_data.groupby('POWER_QUYU'):
            hangyequyu_data = {"department": group_name__}
            for group_name___, group_data___ in group_data__.groupby('POWER_TYPE'):
                hangyequyu_data[ju.powertype_mapping[group_name___]] = ju.get_value(group_data___, 'SUM(*)', jduge_sum=True)
            hangyequyu.append(hangyequyu_data)
        tradePowerErji.append({"year": int(group_name), "dep": group_name_, "data": hangyequyu})
# 全市区职权分析：cityPower方法 分的区划在date里面？？？？？？？？？？？？？？？？？？？？
for group_name, group_data in power_year_quyu_type_isga.groupby('YEAR'):
    city_one = []
    for group_name_, group_data_ in group_data.groupby('POWER_QUYU'):
        city_quyu_one = {"department": group_name_}
        for group_name__, group_data__ in group_data_.groupby('POWER_TYPE'):
            city_quyu_one[ju.powertype_mapping[group_name__]] = ju.get_value(group_data__, 'SUM(*)', jduge_sum=True)
        city_one.append(city_quyu_one)
    cityPower.append({"year": int(group_name), "data": city_one})
# 全市区职权分析(二级）cityPowerErji方法：
for group_name, group_data in power_year_hangye_quyu_type_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('POWER_QUYU'):
        hangyequyu = []
        for group_name__, group_data__ in group_data.groupby('POWER_HANGYE'):
            hangyequyu_data = {"department": group_name__}
            for group_name___, group_data___ in group_data__.groupby('POWER_TYPE'):
                hangyequyu_data[ju.powertype_mapping[group_name___]] = ju.get_value(group_data___, 'SUM(*)', jduge_sum=True)
            hangyequyu.append(hangyequyu_data)
        cityPowerErji.append({"year": int(group_name), "dep": group_name_, "data": hangyequyu})
# 全行业休眠职权（含二级，分类只有处罚）tradeDormancy方法
for group_name, group_data in punish_year_hangye_power_isga.groupby('YEAR'):
    sleep_this = []
    for group_name_, group_data_ in group_data.groupby("PUNISH_HANGYE"):
        sleep_this_data = {"name": group_name_, 
                           "total": ju.get_value(group_data_, "ALL"), 
                           "punish": ju.get_value(group_data_, "SLEEP"), 
                           "allowance": 1, "force": 1, "check":1, "else": 1}
        sleep_this.append(sleep_this_data)
    tradeDormancy.append({"year": int(group_name), "data": sleep_this})
# 全行业休眠职权（二级）
for group_name, group_data in punish_year_hangye_quyu_power_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby("PUNISH_HANGYE"):
        sleep_this = []
        for group_name__, group_data__ in group_data_.groupby("PUNISH_QUYU"):
            sleep_this_data = {"name": group_name__, 
                               "total": ju.get_value(group_data__, "ALL"), 
                               "punish": ju.get_value(group_data__, "SLEEP"), 
                               "allowance": 1, "force": 1, "check":1, "else": 1}
            sleep_this.append(sleep_this_data)
        tradeDormancyErji.append({"year": int(group_name), "dep": group_name_, "data": sleep_this})

# 全市区休眠职权（含二级，分类只有处罚）cityDormancy方法
for group_name, group_data in punish_year_quyu_power_isga.groupby('YEAR'):
    sleep_this = []
    for group_name_, group_data_ in group_data.groupby("PUNISH_QUYU"):
        sleep_this_data = {"name": group_name_, 
                           "total": ju.get_value(group_data_, "ALL"), 
                           "punish": ju.get_value(group_data_, "SLEEP"), 
                           "allowance": 1, "force": 1, "check":1, "else": 1}
        sleep_this.append(sleep_this_data)
    cityDormancy.append({"year": int(group_name), "data": sleep_this})
# 全市区休眠职权（二级）
for group_name, group_data in punish_year_hangye_quyu_power_isga.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby("PUNISH_QUYU"):
        sleep_this = []
        for group_name__, group_data__ in group_data_.groupby("PUNISH_HANGYE"):
            sleep_this_data = {"name": group_name__, 
                               "total": ju.get_value(group_data__, "ALL"), 
                               "punish": ju.get_value(group_data__, "SLEEP"), 
                               "allowance": 1, "force": 1, "check":1, "else": 1}
            sleep_this.append(sleep_this_data)
        cityDormancyErji.append({"year": int(group_name), "dep": group_name_, "data": sleep_this})

# 职权类型分析powerGenre方法
for group_name, group_data in power_year_type_isga.groupby('YEAR'):
    type_all_one = []
    for group_name_, group_data_ in group_data.groupby('POWER_TYPE'):
        type_all_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    powerGenre.append({"year": int(group_name), "data": type_all_one})
# 职权来源分析
for group_name, group_data in power_year_lawtype_isga.groupby('YEAR'):
    lawtype_data = []
    for group_name_, group_data_ in group_data.groupby('POWER_LAWTYPE'):
        lawtype_data.append({"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})
    powerSource.append({"year": int(group_name), "data": lawtype_data})


# 左侧：leftPowerTotal方法
for group_data1, group_data2, group_data3 in zip(power_year_isga.groupby('YEAR'), power_year_lawnumber_isga.groupby('YEAR'), power_year_lawitemnumber_isga.groupby('YEAR')):
    leftPowerTotal.append({"year": int(group_data1[0]),
                           "data": [
                               {"name": "职权总数", "value": ju.get_value(ju.get_df(group_data1), 'SUM(*)')},
                               {"name": "关联法律规范数", "value": ju.get_value(ju.get_df(group_data2), 'SUM(*)')},
                               {"name": "关联依据数", "value": ju.get_value(ju.get_df(group_data3), 'SUM(*)')}]})

# 左侧：处罚职权履行率
for group_name, group_data in punish_year_power_isga.groupby('YEAR'):
    leftPunishRateOfPower.append(
        {"year": int(group_name),
         "value": ju.get_value(group_data, 'USED'),
         "total": ju.get_value(group_data, 'ALL')})


if __name__ == '__main__':
    content_dict_list = {
        "tradePower": tradePower,
        "tradePowerErji": tradePowerErji,
        "cityPower": cityPower,
        "cityPowerErji": cityPowerErji,
        "tradeDormancy": tradeDormancy,  # 休眠只算了一年
        "tradeDormancyErji": tradeDormancyErji,  # 休眠只算了一年
        "cityDormancy": cityDormancy,  # 休眠只算了一年
        "cityDormancyErji": cityDormancyErji,  # 休眠只算了一年
        "powerGenre": powerGenre,
        "powerSource": powerSource,
        # 左侧
        "leftPowerTotal": leftPowerTotal,
        "leftPunishRateOfPower": leftPunishRateOfPower}
    ju.json_io("list.json", content_dict_list)

