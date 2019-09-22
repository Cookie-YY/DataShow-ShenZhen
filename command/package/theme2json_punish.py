# -*- coding: utf-8 -*-
# @Time    : 2019/8/26 22:07
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : theme2json_punish.py
# @Software: PyCharm
"""处罚案件全部，需要区分是否公安"""
from base import JsonUpdate
import pandas as pd
import os

ju = JsonUpdate()

# 只分年
aspect_year = ["_tongbi", "_huanbi",  # 放在一起
               "_punishway", "_type", "_power",  # 很奇怪
               "_dangshirentypebefore", "_dangshirentypeafter", "_source", "_seg",   # 方法统一
               "_month_type", "_quarter_type", "_halfyear_type",  # 放在一起
               "_closestate"]  # 先不做
# 只分行业
aspect_year_hangye = ["_perpeo", "_fine",  # 单搞
                      "_banan", "_bianzhi", "_chizheng",  # 放在一起
                      "_powerbalance", "_power",  # 放在一起
                      "_type",  # 单搞
                      "_cycledays_yanqi", "_cycledays_all"]
# 只分区划和行业区划
aspect_quyu_hangyequyu = ["_perpeo", "_type", "_powerbalance", "_power", "_fine"]
# 分年
command_year = \
    """
punish_year%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year%_isga.csv')))  # 读取各年-含公安
punish_year%_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year%_nonega.csv')))  # 读取各年-无公安
    """
command_year_hangye = \
    """
punish_year_hangye%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye%_isga.csv')))  # 读取各年-含公安
punish_year_hangye%_nonega = ju.get_category(punish_year_hangye%_isga, nonega=True)  # 读取各年-无公安
    """
command_year_quyu_hangyequyu = \
    """
punish_year_hangye_quyu%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye_quyu%_isga.csv')))  # 读取各年-含公安
punish_year_hangye_quyu%_nonega = ju.get_category(punish_year_hangye_quyu%_isga, nonega=True)  # 读取各年-无公安
punish_year_quyu%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu%_isga.csv')))  # 读取各年-含公安
punish_year_quyu%_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu%_nonega.csv')))  # 读取各年-无公安
    """
for asp in aspect_year:
    exec(command_year.replace('%', asp))
for asp in aspect_year_hangye:
    exec(command_year_hangye.replace('%', asp))
for asp in aspect_quyu_hangyequyu:
    exec(command_year_quyu_hangyequyu.replace('%', asp))
punish_way_columns = punish_year_punishway_isga.columns.values  # 处罚全措施的顺序
punish_cycledays_columns = punish_year_hangye_cycledays_all_isga.columns.values  # 处罚周期的顺序
power_year_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_isga.csv')))  # 读取各年职权总数-含公安
power_year_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_power, 'year_nonega.csv')))  # 读取各年职权总数-无公安

# 为了实验（需要各年各行业，各区划的总数，之后前端会修改，计算的总数都分种类了）
punish_year_hangye_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye_isga.csv')))  # 读取各年职权总数-无公安
punish_year_quyu_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu_isga.csv')))  # 读取各年职权总数-无公安
punish_year_hangye_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_hangye_nonega.csv')))  # 读取各年职权总数-无公安
punish_year_quyu_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_punish, 'year_quyu_nonega.csv')))  # 读取各年职权总数-无公安


# 以下，按照大屏顺序：
#####################################################################################
# 行政处罚案件量json
"全行业行政处罚案件量分析（含二级）"
tradePunish, tradePunishErji = [], []
command_tradePunish = \
    """
# 各行业（是否公安）
for group_name, group_data in punish_year_hangye_type_%.groupby('YEAR'):
    hangye_one = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        hangye_one_this = {"name": group_name_}
        for group_name__, group_data__ in group_data_.groupby('PUNISH_TYPE'):
            hangye_one_this[ju.punishtype_mapping['norm'][str(group_name__)]] = ju.get_value(group_data__, 'SUM(*)')
        hangye_one.append(hangye_one_this)
    tradePunish.append({"year": int(group_name), "isga": ^, "data": hangye_one})

# 各行业各区划
for group_name, group_data in punish_year_hangye_quyu_type_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        hangye_quyu_one = []
        for group_name__, group_data__ in group_data_.groupby('PUNISH_QUYU'):
            hangye_quyu_one_this = {"name": group_name__}
            for group_name___, group_data___ in group_data__.groupby('PUNISH_TYPE'):
                hangye_quyu_one_this[ju.punishtype_mapping['norm'][str(group_name___)]] = ju.get_value(group_data___, 'SUM(*)')
            hangye_quyu_one.append(hangye_quyu_one_this)
        tradePunishErji.append({"year": int(group_name), "dep": group_name_, "data": hangye_quyu_one})
"""
"全市区行政处罚案件量分析（含二级）"
cityPunish, cityPunishErji = [], []
command_cityPunish = \
    """
# 各区划（是否公安）
for group_name, group_data in punish_year_quyu_type_%.groupby('YEAR'):
    quyu_one = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        quyu_one_this = {"name": group_name_}
        for group_name__, group_data__ in group_data_.groupby('PUNISH_TYPE'):
            quyu_one_this[ju.punishtype_mapping['norm'][str(group_name__)]] = ju.get_value(group_data__, 'SUM(*)')
        quyu_one.append(quyu_one_this)
    cityPunish.append({"year": int(group_name), "isga": ^, "data": quyu_one})

# 各区划各行业（是否公安）
for group_name, group_data in punish_year_hangye_quyu_type_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        hangye_quyu_one = []
        for group_name__, group_data__ in group_data_.groupby('PUNISH_HANGYE'):
            hangye_quyu_one_this = {"name": group_name__}
            for group_name___, group_data___ in group_data__.groupby('PUNISH_TYPE'):
                hangye_quyu_one_this[ju.punishtype_mapping['norm'][str(group_name___)]] = ju.get_value(group_data___, 'SUM(*)')
            hangye_quyu_one.append(hangye_quyu_one_this)
        cityPunishErji.append({"year": int(group_name), "isga": ^, "dep": group_name_, "data": hangye_quyu_one})
"""
"历年行政处罚案件量分析（含-行业/区划的筛选）"
yearsPunish = {}
years, trade, city = [], [], []
command_yearsPunish = \
"""
# years 部分 是否含公安
years_data = []
for group_name, group_data in punish_year_type_%.groupby('YEAR'):
    years_this = {"name": str(int(group_name))+"年"}
    for group_name_, group_data_ in group_data.groupby('PUNISH_TYPE'):
        years_this[ju.punishtype_mapping['norm'][str(group_name_)]] = ju.get_value(group_data_, 'SUM(*)')
    years_this['total'] = years_this['normalCase'] + years_this['easyCase']
    years_data.append(years_this)
years.append({"isga": ^, "data": years_data})

# trade 部分 是否含公安
trade_data = []
for group_name, group_data in punish_year_hangye_type_%.groupby('PUNISH_HANGYE'):
    trade_this = {"name": group_name}
    for group_name_, group_data_ in group_data.groupby('PUNISH_TYPE'):
        trade_this['type'] = ju.punishtype_mapping['chinesefull'][str(group_name_)]
        for group_name__, group_data__ in group_data_.groupby('YEAR'):
            trade_this[str(int(group_name__))] = ju.get_value(group_data__, 'SUM(*)')
        trade_data.append(trade_this)
# 总案件量
for group_name, group_data in punish_year_hangye_%.groupby('PUNISH_HANGYE'):
    trade_this = {"name": group_name, "type": "总案件量"}
    for group_name_, group_data_ in group_data.groupby('YEAR'):
        trade_this[str(int(group_name_))] = ju.get_value(group_data_, 'SUM(*)')
    trade_data.append(trade_this)
trade.append({"isga": ^, "data": trade_data})

# city 部分 是否含公安
city_data = []
for group_name, group_data in punish_year_quyu_type_%.groupby('PUNISH_QUYU'):
    city_this = {"name": group_name}
    for group_name_, group_data_ in group_data.groupby('PUNISH_TYPE'):
        city_this['type'] = ju.punishtype_mapping['chinesefull'][str(group_name_)]
        for group_name__, group_data__ in group_data_.groupby('YEAR'):
            city_this[str(int(group_name__))] = ju.get_value(group_data__, 'SUM(*)')
        city_data.append(city_this)
# 总案件量——（其实和行业的总案件量一样，再来一遍。。。。）
for group_name, group_data in punish_year_quyu_%.groupby('PUNISH_QUYU'):
    city_this = {"name": group_name, "type": "总案件量"}
    for group_name_, group_data_ in group_data.groupby('YEAR'):
        city_this[str(int(group_name_))] = ju.get_value(group_data_, 'SUM(*)')
    city_data.append(city_this)
city.append({"isga": ^, "data": city_data})
"""
"行政处罚案件量月趋势分析（月，季度，半年，年）"
caseMonthlyTrend = []
# 各月 各季 各半年
command_caseMonthlyTrend = \
    """
# 月/季/半年
for group_name, group_data in punish_year_!_type_%.groupby('YEAR'):
    quarter_one = []
    for group_name_, group_data_ in group_data.groupby('@'):
        quarter_one_this = {"name": ju.time_mapping['!'][0][int(group_name_)-1]}
        for group_name__, group_data__ in group_data_.groupby('PUNISH_TYPE'):
            quarter_one_this[ju.punishtype_mapping['norm'][str(group_name__)]] = ju.get_value(group_data__, 'SUM(*)')
        quarter_one.append(quarter_one_this)
    caseMonthlyTrend.append({"year": int(group_name), "isga": ^, "genre": ju.time_mapping['!'][1], "data": quarter_one})
    """
# 各年（接口混乱）
command_caseMonthlyTrend_ = \
    """
# 历年（json里面什么鬼写法：每一年的字典里面，需要把所有年都写上，如：2015年里面有2015-2019年的数据）
for year_ in ju.order_year:
    year_data = []
    for group_name, group_data in punish_year_type_%.groupby('YEAR'):
        year_data_one = {"name": str(int(group_name))}
        for group_name_, group_data_ in group_data.groupby('PUNISH_TYPE'):
            year_data_one[ju.punishtype_mapping['norm'][str(group_name_)]] = ju.get_value(group_data_, "SUM(*)")
        year_data.append(year_data_one)
    caseMonthlyTrend.append({"year": int(year_), "isga": ^, "genre": "历年", "data": year_data})
    """
"办理环节案件量分析"
handlingOfCases = []
command_handlingOfCases = \
    """
# 案件办理各个环节
for group_name, group_data in punish_year_seg_%.groupby('YEAR'):
    seg_this = []
    lian, diaochaB = 0, 0
    for group_name_, group_data_ in group_data.groupby('PUNISH_SEG'):
        if not group_name_.startswith('调查取证'):
            seg_one={"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")}
            seg_this.append(seg_one)
        else:
            diaochaB = ju.get_value(group_data_, "SUM(*)")
        if group_name_.startswith('立案'):
            lian = ju.get_value(group_data_, "SUM(*)")
    seg_this.append({"name": "立案阶段", "value": lian-diaochaB})
    handlingOfCases.append({"year": int(group_name), "isga": ^, "data": seg_this})
    """
"全措施分析"
allMeasures = []
command_allMeasures = \
    """
# 各行业（是否公安）
for group_name, group_data in punish_year_punishway_%.groupby('YEAR'):
    all_way_this = []
    for col_number in range(len(ju.order_punish_way)):
        all_way_this.append({"name": ju.order_punish_way[col_number], "value": ju.get_value(group_data, punish_way_columns[col_number])})
    allMeasures.append({"year": int(group_name), "isga": ^, "data": all_way_this})
    """
"行政处罚案件来源分析"
punissoanylisLeftPie = []
command_punissoanylisLeftPie = \
    """
for group_name, group_data in punish_year_source_%.groupby('YEAR'):
    source_this = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_SOURCE'):
        source_this.append({"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})
    punissoanylisLeftPie.append({"year": int(group_name), "isga": ^, "data": source_this})
    """
"行政处罚对象类型分析"
objectlawBefore = []
# 各当事人类型-三类
command_objectlawBefore = \
    """
for group_name, group_data in punish_year_dangshirentypebefore_%.groupby('YEAR'):
    dangshiren_one = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_DANGSHIRENTYPE_BEFORE'):
        dangshiren_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    objectlawBefore.append({"year": int(group_name), "isga": ^, "data": dangshiren_one})
    """
# 各当事人类型-四类
objectlawAfter = []
command_objectlawAfter = \
    """
for group_name, group_data in punish_year_dangshirentypeafter_%.groupby('YEAR'):
    dangshiren_one = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_DANGSHIRENTYPE_AFTER'):
        dangshiren_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    objectlawAfter.append({"year": int(group_name), "isga": ^, "data": dangshiren_one})
    """
"案件处罚金额分析！！？？（方法名和内容不对应）"
punishSouce = []
command_punishSouce = \
    """
for group_name, group_data in punish_year_hangye_fine_%.groupby('YEAR'):
    fine_hangye_this = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        fine_hangye_this.append({"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})
    punishSouce.append({"year": int(group_name), "isga": ^, "data": fine_hangye_this})
    """
#####################################################################################
# 行政处罚金额json
"行政处罚金额月趋势分析——暂无"
"全行业行政处罚金额分析——同案件处罚金额分析"
"全市区行政处罚金额分析"
cityPunishMoney = []
command_cityPunishMoney = \
    """
for group_name, group_data in punish_year_quyu_fine_%.groupby('YEAR'):
    fine_quyu_this = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        fine_quyu_this.append({"name": group_name_, "value": ju.get_value(group_data_, "SUM(*)")})
    cityPunishMoney.append({"year": int(group_name), "isga": ^, "data": fine_quyu_this})
    """
#####################################################################################
# 人均处罚量json
"一线执法率（编制，办案，持证，总职权，执法率：办案/编制）"
rateOfFrontLineExecutor = []
command_rateOfFrontLineExecutor = \
    """
# 各行业（是否公安）
for group_data1, group_data2, group_data3, group_data4 in zip(punish_year_hangye_banan_%.groupby('YEAR'), punish_year_hangye_bianzhi_%.groupby('YEAR'), punish_year_hangye_chizheng_%.groupby('YEAR'), punish_year_hangye_power_%.groupby('YEAR')):
    zhifa_this = []
    for group_data1_, group_data2_, group_data3_, group_data4_ in zip(ju.get_df(group_data1).groupby('PUNISH_HANGYE'), ju.get_df(group_data2).groupby('SUB_HANGYE'), ju.get_df(group_data3).groupby('PEO_ENFORCE_HANGYE'), ju.get_df(group_data4).groupby('PUNISH_HANGYE')):
        zhifa_this_one = {"department": group_data1_[0]}
        zhifa_this_one["executor"] = ju.get_value(ju.get_df(group_data1_), 'PEO_PER_PEO', 100)  # 一线执法率
        zhifa_this_one["investigators"] = ju.get_value(ju.get_df(group_data2_), 'SUM(*)')  # 编制
        zhifa_this_one["holder"] = ju.get_value(ju.get_df(group_data1_), 'SUM(*)')  # 办案
        zhifa_this_one["add_holder"] = ju.get_value(ju.get_df(group_data3_), 'SUM(*)')  # 持证
        zhifa_this_one["powersNum"] = ju.get_value(ju.get_df(group_data4_), 'ALL')  # 总职权
        zhifa_this.append(zhifa_this_one)
    rateOfFrontLineExecutor.append({"year": int(group_data1[0]), "isga": ^, "data": zhifa_this})
    """
"全行业人均处罚量分析"
tradePerPunish, tradePerPunishErji = [], []
command_tradePerPunish = \
    """
# 各行业（是否公安）
for group_name, group_data in punish_year_hangye_perpeo_%.groupby('YEAR'):
    perpeo_hangye_one = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        perpeo_hangye_one.append({"name": group_name_, "value":round(ju.get_value(group_data_, 'CASE_PER_PEO'),2)})
    tradePerPunish.append({"year": int(group_name), "isga": ^, "data": perpeo_hangye_one})

# 各行业各区划
for group_name, group_data in punish_year_hangye_quyu_perpeo_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        perpeo_hangyequyu_one = []
        for group_name__, group_data__ in group_data_.groupby('PUNISH_QUYU'):
            perpeo_hangyequyu_one.append({"name": group_name__, "value": round(ju.get_value(group_data__, 'CASE_PER_PEO'),2)})
        tradePerPunishErji.append({"year": int(group_name),  "dep": group_name_, "data": perpeo_hangyequyu_one})
    """
"全市区人均处罚量分析"
cityPerPunish, cityPerPunishErji = [], []
command_cityPerPunish = \
    """
# 各区划（是否公安）
for group_name, group_data in punish_year_quyu_perpeo_%.groupby('YEAR'):
    perpeo_quyu_one =[]
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        perpeo_quyu_one.append({"name": group_name_, "value": round(ju.get_value(group_data_, 'CASE_PER_PEO'),2)})
    cityPerPunish.append({"year": int(group_name), "isga": ^, "data": perpeo_quyu_one})

# 各区划各行业（是否公安）
for group_name, group_data in punish_year_hangye_quyu_perpeo_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PUNISH_QUYU'):
        perpeo_hangyequyu_one = []
        for group_name__, group_data__ in group_data_.groupby('PUNISH_HANGYE'):
            perpeo_hangyequyu_one.append({"name": group_name__, "value": round(ju.get_value(group_data__, 'CASE_PER_PEO'),2)})
        cityPerPunishErji.append({"year": int(group_name), "isga": ^, "dep": group_name_, "data": perpeo_hangyequyu_one})
    """
"历年人均处罚量分析——暂无"
"办案强度分析——暂无"
#####################################################################################
# 职权履行情况json
"全行业职权履行情况分析(均衡率，使用率，总数)(含二级）"
tradePowerPerform, tradePowerPerformErji = [], []
command_tradePowerPerform = \
    """
# 各行业（是否公安）
for group_data1, group_data2 in zip(punish_year_hangye_power_%.groupby('YEAR'), punish_year_hangye_powerbalance_%.groupby('YEAR')):
    power_hangye_info = []
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_HANGYE'), ju.get_df(group_data2).groupby('PUNISH_HANGYE')):
        power_hangye_info_one = {"name": group_data1_[0]}
        power_hangye_info_one['performances'] = ju.get_value(ju.get_df(group_data1_), 'USED')
        power_hangye_info_one['dutyBalancing'] = ju.get_value(ju.get_df(group_data2_), 'RATIO_BALANCE', 100)
        power_hangye_info_one['rateOfPerformance'] = ju.get_value(ju.get_df(group_data1_), 'RATIO', 100)
        power_hangye_info_one['powers'] = ju.get_value(ju.get_df(group_data1_), 'ALL')
        power_hangye_info.append(power_hangye_info_one)
    tradePowerPerform.append({"year": int(group_data1[0]), "isga": ^, "data": power_hangye_info})

# 各行业各区划
for group_data1, group_data2 in zip(punish_year_hangye_quyu_power_%.groupby('YEAR'), punish_year_hangye_quyu_powerbalance_%.groupby('YEAR')):
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_HANGYE'), ju.get_df(group_data2).groupby('PUNISH_HANGYE')):
        power_hangye_quyu_info = []
        for group_data1__, group_data2__ in zip(ju.get_df(group_data1_).groupby('PUNISH_QUYU'), ju.get_df(group_data2_).groupby('PUNISH_QUYU')):
            power_hangye_quyu_info_one = {"name": group_data1__[0]}
            power_hangye_quyu_info_one['performances'] = ju.get_value(ju.get_df(group_data1__), 'USED')
            power_hangye_quyu_info_one['dutyBalancing'] = ju.get_value(ju.get_df(group_data2__), 'RATIO_BALANCE', 100)
            power_hangye_quyu_info_one['rateOfPerformance'] = ju.get_value(ju.get_df(group_data1__), 'RATIO', 100)
            power_hangye_quyu_info_one['powers'] = ju.get_value(ju.get_df(group_data1__), 'ALL')
            power_hangye_quyu_info.append(power_hangye_quyu_info_one)
        tradePowerPerformErji.append({"year": int(group_data1[0]), "dep": group_data1_[0], "data": power_hangye_quyu_info})
    """
"全市区职权履行情况分析(均衡率，使用率，总数)(含二级）"
cityPowerPerform, cityPowerPerformErji = [], []
command_cityPowerPerform = \
    """
# 各区划（是否公安）
for group_data1, group_data2 in zip(punish_year_quyu_power_%.groupby('YEAR'), punish_year_quyu_powerbalance_%.groupby('YEAR')):
    power_quyu_info = []
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_QUYU'), ju.get_df(group_data2).groupby('PUNISH_QUYU')):
        power_quyu_info_one = {"name": group_data1_[0]}
        power_quyu_info_one['performances'] = ju.get_value(ju.get_df(group_data1_), 'USED')
        power_quyu_info_one['dutyBalancing'] = ju.get_value(ju.get_df(group_data2_), 'RATIO_BALANCE', 100)
        power_quyu_info_one['rateOfPerformance'] = ju.get_value(ju.get_df(group_data1_), 'RATIO', 100)
        power_quyu_info_one['powers'] = ju.get_value(ju.get_df(group_data1_), 'ALL')
        power_quyu_info.append(power_quyu_info_one)
    cityPowerPerform.append({"year": int(group_data1[0]), "isga": ^, "data": power_quyu_info})

# 各区划各行业（是否公安）
for group_data1, group_data2 in zip(punish_year_hangye_quyu_power_%.groupby('YEAR'), punish_year_hangye_quyu_powerbalance_%.groupby('YEAR')):
    for group_data1_, group_data2_ in zip(ju.get_df(group_data1).groupby('PUNISH_QUYU'), ju.get_df(group_data2).groupby('PUNISH_QUYU')):
        power_hangye_quyu_info = []
        for group_data1__, group_data2__ in zip(ju.get_df(group_data1_).groupby('PUNISH_HANGYE'), ju.get_df(group_data2_).groupby('PUNISH_HANGYE')):
            power_hangye_quyu_info_one = {"name": group_data1__[0]}
            power_hangye_quyu_info_one['performances'] = ju.get_value(ju.get_df(group_data1__), 'USED')
            power_hangye_quyu_info_one['dutyBalancing'] = ju.get_value(ju.get_df(group_data2__), 'RATIO_BALANCE', 100)
            power_hangye_quyu_info_one['rateOfPerformance'] = ju.get_value(ju.get_df(group_data1__), 'RATIO', 100)
            power_hangye_quyu_info_one['powers'] = ju.get_value(ju.get_df(group_data1__), 'ALL')
            power_hangye_quyu_info.append(power_hangye_quyu_info_one)
        cityPowerPerformErji.append({"year": int(group_data1[0]), "isga": ^, "dep":  group_data1_[0], "data": power_hangye_quyu_info})

    """
"全行业休眠职权（含二级，分类只有处罚）"
tradeDormancy, tradeDormancyErji = [], []
command_tradeDormancy = \
    """
# 各行业
for group_name, group_data in punish_year_hangye_power_isga.groupby('YEAR'):
    sleep_this = []
    for group_name_, group_data_ in group_data.groupby("PUNISH_HANGYE"):
        sleep_this_data = {"name": group_name_, 
                           "total": ju.get_value(group_data_, "ALL"), 
                           "punish": ju.get_value(group_data_, "SLEEP"), 
                           "allowance": 1, "force": 1, "check":1, "else": 1}
        sleep_this.append(sleep_this_data)
    tradeDormancy.append({"year": int(group_name), "data": sleep_this})
# 各行业各区划
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
    """
"全市区休眠职权（含二级，分类只有处罚）"
cityDormancy, cityDormancyErji = [], []
command_cityDormancy = \
    """
# 各区划
for group_name, group_data in punish_year_quyu_power_isga.groupby('YEAR'):
    sleep_this = []
    for group_name_, group_data_ in group_data.groupby("PUNISH_QUYU"):
        sleep_this_data = {"name": group_name_, 
                           "total": ju.get_value(group_data_, "ALL"), 
                           "punish": ju.get_value(group_data_, "SLEEP"), 
                           "allowance": 1, "force": 1, "check":1, "else": 1}
        sleep_this.append(sleep_this_data)
    cityDormancy.append({"year": int(group_name), "data": sleep_this})
# 各区划各行业
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
    """
#####################################################################################
# 案件评查json

#####################################################################################
# 处罚周期json
"处罚周期分析"
punishPeriod = []
command_punishPeriod = \
    """
for group_name, group_data in punish_year_hangye_cycledays_!_%.groupby('YEAR'):
    all_way_this = []
    for group_name_, group_data_ in group_data.groupby('PUNISH_HANGYE'):
        cycledays_data = []
        for col_number in range(len(ju.order_punish_cycledays)):
            cycledays_data.append({"name": ju.order_punish_cycledays[col_number], "value": int(ju.get_value(group_data_, punish_cycledays_columns[col_number]))})
        punishPeriod.append({"year": int(group_name), "isga": ^, "dep": group_name_, "genre": "@", "data": cycledays_data})
     """
#####################################################################################
# 投诉举报分析json
"全行业投诉举报吻合度——未完成"
tradeReportCoincide = []
"投诉举报量——暂无"
"投诉举报重点领域分析——暂无"
#####################################################################################
# 左侧json
"左侧：职权总数"
rateLeftPunishPower = []
command_rateLeftPunishPower = \
    """
for group_name, group_data in power_year_%.groupby('YEAR'):
    rateLeftPunishPower.append({"year": int(group_name), "isga": ^, "sum": ju.get_value(group_data, 'SUM(*)')})
    """
"左侧：职权使用（后台不用算比例，大屏算比例，提供使用数和总数）"
rateLeftCfzqlzl= []
command_rateLeftCfzqlzl = \
    """
for group_name, group_data in punish_year_power_%.groupby('YEAR'):
    rateLeftCfzqlzl.append(
        {"year": int(group_name),
         "isga": ^,
         "value": ju.get_value(group_data, 'USED'),
         "total": ju.get_value(group_data, 'ALL')})
    """
"左侧：同比环比+各年各类案件"
rateLeftPunishCase = []
command_rateLeftPunishCase = \
    """
for group_data1, group_data2, group_data3 in zip(punish_year_tongbi_%.groupby('YEAR'), punish_year_huanbi_%.groupby('YEAR'), punish_year_type_%.groupby('YEAR')):
    zonghe_this = {"year": int(group_data1[0]), "isga": ^}
    for group_name3_, group_data3_ in ju.get_df(group_data3).groupby('PUNISH_TYPE'):
        zonghe_this[ju.punishtype_mapping['abnorm'][str(group_name3_)]] = ju.get_value(group_data3_, "SUM(*)")
    zonghe_this["TB"] = ju.get_value(ju.get_df(group_data1), "TONG", 100)
    zonghe_this["HB"] = ju.get_value(ju.get_df(group_data2), "HUAN", 100)
    rateLeftPunishCase.append(zonghe_this)    
    """


for i, j in ju.ga:
    """处罚案件json"""
    exec(command_tradePunish.replace('%', i).replace('^', j))
    exec(command_cityPunish.replace('%', i).replace('^', j))
    exec(command_yearsPunish.replace('%', i).replace('^', j))
    # 各月/季度/半年 单独写
    exec(command_caseMonthlyTrend_.replace('%', i).replace('^', j))  # 历年案件量
    exec(command_handlingOfCases.replace('%', i).replace('^', j))
    exec(command_allMeasures.replace('%', i).replace('^', j))
    exec(command_punissoanylisLeftPie.replace('%', i).replace('^', j))
    exec(command_objectlawBefore.replace('%', i).replace('^', j))
    exec(command_objectlawAfter.replace('%', i).replace('^', j))
    exec(command_punishSouce.replace('%', i).replace('^', j))
    """处罚金额json"""
    exec(command_cityPunishMoney.replace('%', i).replace('^', j))
    """人均处罚量json"""
    exec(command_rateOfFrontLineExecutor.replace('%', i).replace('^', j))
    exec(command_tradePerPunish.replace('%', i).replace('^', j))
    exec(command_cityPerPunish.replace('%', i).replace('^', j))
    """职权履行情况json"""
    exec(command_tradePowerPerform.replace('%', i).replace('^', j))
    exec(command_cityPowerPerform.replace('%', i).replace('^', j))
    # 全行业/市区休眠没有是否公安，单独写
    """案件评查json为空"""
    """处罚周期json"""
    # 周期单独写
    """投诉举报分析json"""
    # 未完成
    """左侧json"""
    exec(command_rateLeftPunishPower.replace('%', i).replace('^', j))
    exec(command_rateLeftCfzqlzl.replace('%', i).replace('^', j))
    exec(command_rateLeftPunishCase.replace('%', i).replace('^', j))

yearsPunish['years'] = years
yearsPunish['trade'] = trade
yearsPunish['city'] = city

for time_ in ["month", "quarter", "halfyear"]:
    for i, j in ju.ga:
        exec(command_caseMonthlyTrend.replace('!', time_).replace('@', time_.upper()).replace('%', i).replace('^', j))

for cycle, cycle_name in zip(["all", "yanqi"], ["全部案件", "延期案件"]):
    for i, j in ju.ga:
        exec(command_punishPeriod.replace('!', cycle).replace('@', cycle_name).replace('%', i).replace('^', j))

exec(command_tradeDormancy)
exec(command_cityDormancy)

if __name__ == '__main__':
    content_dict_xzcfajl = {  # done
        "tradePunish": tradePunish,
        "tradePunishErji": tradePunishErji,
        "cityPunish": cityPunish,
        "cityPunishErji": cityPunishErji,
        "yearsPunish": yearsPunish,
        "caseMonthlyTrend": caseMonthlyTrend,
        "handlingOfCases": handlingOfCases,
        "allMeasures": allMeasures,
        "punissoanylisLeftPie": punissoanylisLeftPie,
        "objectlawBefore": objectlawBefore,
        "objectlawAfter": objectlawAfter,
        "punishSouce": punishSouce}
    content_dict_xzcfje = {  # 等前端
        "tradePunishMoney": punishSouce,
        "cityPunishMoney": cityPunishMoney}
    content_dict_rjcfl = {  # 等前端
        "rateOfFrontLineExecutor": rateOfFrontLineExecutor,
        "tradePerPunish": tradePerPunish,
        "tradePerPunishErji": tradePerPunishErji,
        "cityPerPunish": cityPerPunish,
        "cityPerPunishErji": cityPerPunishErji}
    content_dict_zqlxgk = {  # 休眠只算了一年
        "tradePowerPerform": tradePowerPerform,
        "tradePowerPerformErji": tradePowerPerformErji,
        "cityPowerPerform": cityPowerPerform,
        "cityPowerPerformErji": cityPowerPerformErji,
        "tradeDormancy": tradeDormancy,
        "tradeDormancyErji": tradeDormancyErji,
        "cityDormancy": cityDormancy,
        "cityDormancyErji": cityDormancyErji}
    content_dict_cfzq = {
        "punishPeriod": punishPeriod}

    content_dict_leftPane = {
        "rateLeftPunishPower": rateLeftPunishPower,
        "rateLeftPunishCase": rateLeftPunishCase,
        "rateLeftCfzqlzl": rateLeftCfzqlzl}

    ju.json_io("xzcfajl.json", content_dict_xzcfajl, iscf=True)
    ju.json_io("xzcfje.json", content_dict_xzcfje, iscf=True)
    ju.json_io("rjcfl.json", content_dict_rjcfl, iscf=True)
    ju.json_io("zqlxgk.json", content_dict_zqlxgk, iscf=True)
    ju.json_io("cfzq.json", content_dict_cfzq, iscf=True)
    ju.json_io("leftPane.json", content_dict_leftPane, iscf=True)
