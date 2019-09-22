# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 11:11
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : theme2json_enforcepeo.py
# @Software: PyCharm

from base import JsonUpdate
import pandas as pd
import os

ju = JsonUpdate()

aspect_enforcepeo = ["_edu", "_age", "_sex", "_politic", "", "_stafftype", "_jobclass"]
sqfb, hyfb = [], []  # 初始化市区分布，行业分布，
age, edu, sex, stafftype, jobclass, politic = [], [], [], [], [], []  # 年龄分布，学历分布，性别分布，性质分布，职级分布，政治面貌分布
# nlfb, xlfb, xbfb, zfrylx, zjfb, zzmm = [], [], [], [], [], []  # 年龄分布，学历分布，性别分布，性质分布，职级分布，政治面貌分布
# 初始化执法人员数量（页面中间）
zfryCount = []
# 左侧指标：行业总数/领域总数/人员总数
hyTotal, lyTotal, zfryTotal = [], [], []
# 左侧指标层级：机关/主体
leftGzdwzs, leftMainLawExecute = [], []
command_enforcepeo= \
    """
enforcepeo_year%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year%_isga.csv')))  # 读取各年各分类-含公安
enforcepeo_year%_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year%_nonega.csv')))  # 读取各年各分类-无公安
enforcepeo_year_hangye%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year_hangye%_isga.csv')))  # 读取各年各行业各分类-含公安
enforcepeo_year_hangye%_nonega = ju.get_category(enforcepeo_year_hangye%_isga, nonega=True)  # 读取各年各行业各分类-无公安
enforcepeo_year_quyu%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year_quyu%_isga.csv')))  # 读取各年各区划各分类-含公安
enforcepeo_year_quyu%_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year_quyu%_nonega.csv')))  # 读取各年各区划各分类-无公安
enforcepeo_year_hangye_quyu%_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_enforcepeo, 'year_hangye_quyu%_isga.csv')))  # 读取各年各行业各区划各分类-含公安
enforcepeo_year_hangye_quyu%_nonega = ju.get_category(enforcepeo_year_hangye_quyu%_isga, nonega=True)  # 读取各年各行业各区划各分类-无公安
    """

org_year_level_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_org, 'year_level_isga.csv')))
org_year_level_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_org, 'year_level_nonega.csv')))
org_year_hangyenumber_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_org, 'year_hangyenumber_isga.csv')))

sub_year_level_isga = ju.get_category(pd.read_csv(os.path.join(ju.path_source_sub, 'year_level_isga.csv')))
sub_year_level_nonega = ju.get_category(pd.read_csv(os.path.join(ju.path_source_sub, 'year_level_nonega.csv')))

for i in aspect_enforcepeo:
    exec(command_enforcepeo.replace('%', i))


#####################################################################################
# 第一部分：单维度
# 0全体人员部分
command_all = \
    """
# 全行业分区划的人员：sqfb方法
for group_name, group_data in enforcepeo_year_quyu_%.groupby('YEAR'):
    sq_one = []
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_QUYU'):
        sq_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    sqfb.append({"year": int(group_name), "isga": ^, 'dep': "全行业", "data": sq_one})

# 分行业分区划的人员：sqfb方法
for group_name, group_data in enforcepeo_year_hangye_quyu_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        sq_hangqu = []
        for group_name__, group_data__ in group_data_.groupby('PEO_ENFORCE_QUYU'):
            sq_hangqu.append({"name": group_name__, "value": ju.get_value(group_data__, 'SUM(*)')})
        sqfb.append({"year": int(group_name), "isga": ^, 'dep': group_name_, "data": sq_hangqu})

# 全区划分行业的人员：hyfb方法
for group_name, group_data in enforcepeo_year_hangye_%.groupby('YEAR'):
    hy_one = []
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        hy_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    hyfb.append({"year": int(group_name), "isga": ^, 'city': "全市", "data": hy_one})
# 分区划分行业的人员：hyfb方法
for group_name, group_data in enforcepeo_year_hangye_quyu_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_QUYU'):
        hy_hangqu = []
        for group_name__, group_data__ in group_data_.groupby('PEO_ENFORCE_HANGYE'):
            hy_hangqu.append({"name": group_name__, "value": ju.get_value(group_data__, 'SUM(*)')})
        hyfb.append({"year": int(group_name), "isga": ^, 'city': group_name_, "data": hy_hangqu})
    """
#####################################################################################
# 第二部分：分维度-含公安
command_aspect = \
    """
# 全市全行业的分布：
for group_name, group_data in enforcepeo_year_!_%.groupby('YEAR'):
    nl_all_one = []
    for group_name_, group_data_ in group_data.groupby('ENFORCEPEO_@'):
        nl_all_one.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    !.append({"year": int(group_name), "isga": ^, "city": "全市", "dep": "全行业", "data": nl_all_one})
# 各区划全行业的分布：
for group_name, group_data in enforcepeo_year_quyu_!_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_QUYU'):
        quyu_nl_one = []
        for group_name__, group_data__ in group_data_.groupby('ENFORCEPEO_@'):
            quyu_nl_one.append({"name": group_name__, "value": ju.get_value(group_data__, 'SUM(*)')})
        !.append({"year": int(group_name), "isga": ^, "city": group_name_, "dep": "全行业", "data": quyu_nl_one})
# 各行业全市区的分布：
for group_name, group_data in enforcepeo_year_hangye_!_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        hangye_nl_one = []
        for group_name__, group_data__ in group_data_.groupby('ENFORCEPEO_@'):
            hangye_nl_one.append({"name": group_name__, "value": ju.get_value(group_data__, 'SUM(*)')})
        !.append({"year": int(group_name), "isga": ^, "city": '全市', "dep": group_name_, "data": hangye_nl_one})
# 各行业各市区的分布：
for group_name, group_data in enforcepeo_year_hangye_quyu_!_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        for group_name__, group_data__ in group_data_.groupby('PEO_ENFORCE_QUYU'):
            hangyequyu_nl_one = []
            for group_name___, group_data___ in group_data__.groupby('ENFORCEPEO_@'):
                hangyequyu_nl_one.append({"name": group_name___, "value": ju.get_value(group_data___, 'SUM(*)')})
            !.append({"year": int(group_name), "isga": ^, "city": group_name__, "dep": group_name_, "data": hangyequyu_nl_one})
    """
# 第三部分指标
command_side = \
    """
# 全市全行业人员：zfrycount方法（页面中间）/zfryTotal（左侧）方法
for group_name, group_data in enforcepeo_year_%.groupby('YEAR'):
    zfryCount.append({"year": int(group_name), "isga": ^, "city": "全市", "dep": "全行业", "data": ju.get_value(group_data, 'SUM(*)')})
    zfryTotal.append({"year": int(group_name), "isga": ^, "value": ju.get_value(group_data, 'SUM(*)')})
# 各区划全行业的人员：zfrycount方法
for group_name, group_data in enforcepeo_year_quyu_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_QUYU'):
        zfryCount.append({"year": int(group_name), "isga": ^, "city": group_name_, "dep": "全行业", "data": ju.get_value(group_data_, 'SUM(*)')})
# 各行业全市区的人员：zfrycount方法
for group_name, group_data in enforcepeo_year_hangye_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        zfryCount.append({"year": int(group_name), "isga": ^, "city": '全市', "dep": group_name_, "data": ju.get_value(group_data_, 'SUM(*)')})
# 各行业各市区的人员：zfrycount方法
for group_name, group_data in enforcepeo_year_hangye_quyu_%.groupby('YEAR'):
    for group_name_, group_data_ in group_data.groupby('PEO_ENFORCE_HANGYE'):
        for group_name__, group_data__ in group_data_.groupby('PEO_ENFORCE_QUYU'):
            zfryCount.append({"year": int(group_name), "isga": ^, "city": group_name__, "dep": group_name_, "data": ju.get_value(group_data__, 'SUM(*)')})

# 左侧指标：层级
# 机关层级
for group_name, group_data in org_year_level_%.groupby('YEAR'):
    jgcj = []
    for group_name_, group_data_ in group_data.groupby('ORG_LEVEL'):
        jgcj.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    leftGzdwzs.append({"year": int(group_name), "isga": ^, "data": jgcj})
# 主体层级
for group_name, group_data in sub_year_level_%.groupby('YEAR'):
    ztcj = []
    for group_name_, group_data_ in group_data.groupby('SUB_LEVEL'):
        ztcj.append({"name": group_name_, "value": ju.get_value(group_data_, 'SUM(*)')})
    leftMainLawExecute.append({"year": int(group_name), "isga": ^, "data": ztcj})
    """
# 行业总数
for group_name, group_data in org_year_hangyenumber_isga.groupby('YEAR'):
    hyTotal.append({"year": int(group_name), "isga": True, "value": ju.get_value(group_data, 'SUM(*)')})
    hyTotal.append({"year": int(group_name), "isga": False, "value": ju.get_value(group_data, 'SUM(*)') - 1})

# 领域总数：假数据，只能加上
for year_ in ju.order_year:
    lyTotal.append({"year": int(year_), "isga": True, "value": 1})
    lyTotal.append({"year": int(year_), "isga": False, "value": 0})

# 总执行程序
for asp in [i.strip('_') for i in aspect_enforcepeo if i]:
    command_aspect_this = command_aspect.replace("!", asp).replace("@", asp.upper())
    for i, j in ju.ga:
        exec(command_aspect_this.replace('%', i).replace('^', j))

for i, j in ju.ga:
    exec(command_all.replace('%', i).replace('^', j))
    exec(command_side.replace('%', i).replace('^', j))


if __name__ == '__main__':
    content_dict_organization = {
        "sqfb": sqfb,
        "hyfb": hyfb,
        "nlfb": age,
        "xlfb": edu,
        "xbfb": sex,
        "zjfb": jobclass,
        "zzmm": politic,
        "zfrylx": stafftype,
        "zfryCount": zfryCount,
        'zfryTotal': zfryTotal,
        "hyTotal": hyTotal,
        "lyTotal": lyTotal,  # 假数据的方法（现在没有领域）
        "leftGzdwzs": leftGzdwzs,
        "leftMainLawExecute": leftMainLawExecute}
    ju.json_io("organization.json", content_dict_organization)
