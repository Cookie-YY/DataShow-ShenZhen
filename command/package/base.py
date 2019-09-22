# -*- coding: utf-8 -*-
# @Time    : 2019/8/23 11:11
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : base.py
# @Software: PyCharm

import pandas as pd
import datetime
import os
import time
import json

"""
本程序是深圳后台执行以下脚本的基类方法文件
    - 流程驱动脚本：raw2busin_extract.py
                   busin2standard_extract.py
                   busin2theme_calculate.py
    - 更新json脚本
                   theme2json_home.py
                   theme2json_punish.py
                   theme2json_law_peo_enforce.py
                   theme2json_law.py
                   theme2json_power.py
基类1：SourcePath：得到所有来源路径（result/standard，result/theme)
基类2：SettingsInfo：得到设置文件中的信息和目的路径（supervision）
基类3：BaseJsonUpdate：继承基类1，基类2，并初始化了：1. isga的字典 2. 地图数据 3. 各个分类标准 4.映射 

驱动流程部分（WorkflowStart类，继承自基类1）包含：
    create_path方法：新建所需文件夹
    start_workflow方法：按顺序驱动指定流程
更新json脚本部分（JsonUpdate类，继承子基类3）包含：
    change_category方法：get_category方法的基础
    get_category方法：将所有的文件更新类别变量
    get_value方法：指定数据表和列，获取数据（空值以0填充）
    get_df方法：转换表格：（使用zip连接多个表格，并使用循环时，需要转换成表格）
    json_io方法：读入json，接受参数，写出json（大屏实现动态）
驱动python脚本部分（PyStart类）
"""


class SourcePath:  # 获得 1.标准库的路径 2.主题库的路径（用于创建文件夹和寻找计算结果）
    def __init__(self):
        self.path_base = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # 找到根目录datashow的路径
        self.path_standard = os.path.join(self.path_base, 'result', 'standard')
        self.path_source_punish = os.path.join(self.path_base, 'result', 'theme', 'punish')
        self.path_source_power = os.path.join(self.path_base, 'result', 'theme', 'power')
        self.path_source_enforcepeo = os.path.join(self.path_base, 'result', 'theme', 'enforcepeo')
        self.path_source_org = os.path.join(self.path_base, 'result', 'theme', 'organization')
        self.path_source_sub = os.path.join(self.path_base, 'result', 'theme', 'subject')
        self.path_source_law = os.path.join(self.path_base, 'result', 'theme', 'law')


class SettingsInfo:  # 获得 1. settings.json中的内容  2. 得到目标路径
    def __init__(self):
        self.path_base = os.path.dirname(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))  # 找到根目录datashow的路径
        # 获得settings.json数据
        with open(os.path.join(self.path_base, 'command', 'settings.json'), 'r', encoding='utf-8') as json_read:
            load_json = json.load(json_read)
        self.sig_dig = load_json['SIGNIFICANT_DIGITS']
        self.file_encoding = load_json['FILE_ENCODING']
        self.state = load_json['STATE']
        self.path_tar = load_json['PATH']['PATH_DEV']['PATH_DAPING_DATA'] if self.state == 'DEV' else \
        load_json['PATH']['PATH_PRO']['PATH_DAPING_DATA']
        self.raw_database = load_json['DATABASE']['DATABASE_DEV']['RAW_DATABASE'] if self.state == 'DEV' else load_json['DATABASE'][
            'DATABASE_PRO']['RAW_DATABASE']
        self.busin_database = load_json['DATABASE']['DATABASE_DEV']['BUSIN_DATABASE'] if self.state == 'DEV' else load_json['DATABASE'][
            'DATABASE_PRO']['BUSIN_DATABASE']
        self.path_python = load_json['PATH']['PATH_DEV']['PATH_PYTHON'] if self.state == 'DEV' else \
        load_json['PATH']['PATH_PRO']['PATH_PYTHON']
        self.path_core = load_json['PATH']['PATH_DEV']['PATH_CORE'] if self.state == 'DEV' else \
        load_json['PATH']['PATH_PRO']['PATH_CORE']
        self.path_epf = load_json['PATH']['PATH_DEV']['PATH_EPF'] if self.state == 'DEV' else \
        load_json['PATH']['PATH_PRO']['PATH_EPF']
        self.path_ojdbc = load_json['PATH']['PATH_DEV']['PATH_OJDBC'].replace("\\", "\\\\\\") if self.state == 'DEV' else \
        load_json['PATH']['PATH_PRO']['PATH_OJDBC'].replace("\\", "\\\\\\")
        # 获得目标json的文件夹
        self.path_tar_punish = os.path.join(self.path_tar, 'punish')  # 处罚案件是一个文件夹


class WorkflowStart(SourcePath, SettingsInfo):
    def __init__(self):
        SourcePath.__init__(self)
        SettingsInfo.__init__(self)
        self.command = \
            f'{self.path_core} ' \
            f'-consoleLog -application org.knime.product.KNIME_BATCH_APPLICATION -reset ' \
            f'-workflowDir="%s" ' \
            f'-preferences="{self.path_epf}" ' \
            f'-nosplash'


    @staticmethod
    def create_path(dir_list):
        for dir_ in dir_list:
            os.system('mkdir -p %s' % dir_)

    def start_workflow(self, filename):
        path_order = os.path.join(self.path_base, 'command', 'excute_order')
        with open(os.path.join(path_order, filename+'_order'), 'r', encoding='utf-8') as ord:
            workflow_list = [os.path.join(self.path_base, 'workflow', filename, i.strip()) for i in ord.readlines()]
        with open(os.path.join(self.path_base, 'command', 'excute_log', filename), 'a', encoding='utf-8') as f:
            f.write(str(datetime.datetime.now()))
            t0 = time.time()
            for workflow in workflow_list:
                t = time.time()
                os.system(self.command % workflow)
                t_ = time.time()
                f.write(workflow + '-----------'+str(int(t_-t)) + '\n')
            f.write('-----------' + str(int(time.time()-t0)) + '-----------')
            f.write(str(datetime.datetime.now()))
            f.write('----------------------')
            f.write('----------------------')


class BaseJsonUpdate(SourcePath, SettingsInfo):
    def __init__(self):
        SourcePath.__init__(self)
        SettingsInfo.__init__(self)
        self.ga = [("isga", "True"), ("nonega", "False")]
        self.home_map = {  # 地图数据，用于加载首页地图
            "福田区": 6496, "罗湖区": 4343, "盐田区": 2804, "南山区": 4315, "宝安区": 4245, "龙岗区": 2668, "光明区": 3484, "坪山区": 3620,
            "龙华区": 1484, "大鹏新区": 1620, "深汕特别合作区": 1620}
        # 获取标准序列
        # 标准-基础
        self.order_quyu = self.get_order('standard_base_quyu.csv')
        self.order_hangye = self.get_order('standard_base_hangye.csv')
        self.order_org_level = self.get_order('standard_base_level.csv')
        self.order_sub_level = self.get_order('standard_base_level.csv')
        self.order_month = [i for i in range(1, 13)]
        self.order_quarter = [i for i in range(1, 5)]
        self.order_halfyear = [i for i in range(1, 3)]
        self.order_year = [float(datetime.datetime.now().year) - i for i in range(5)][::-1]
        self.order_hangye_nonega = [i for i in self.order_hangye if i != "公安"]
        # 标准-人员
        self.order_enforcepeo_edu = self.get_order('standard_staff_edu.csv')[::-1]  # 学历顺序是反的
        self.order_enforcepeo_jobclass = self.get_order('standard_staff_jobclass.csv')
        self.order_enforcepeo_stafftype = self.get_order('standard_staff_type.csv')
        self.order_enforcepeo_politic = self.get_order('standard_staff_politic.csv')
        self.order_enforcepeo_sex = self.get_order('standard_staff_sex.csv')
        self.order_enforcepeo_age = self.get_order('standard_staff_age.csv')
        # 标准-处罚案件
        self.order_punish_way = ["罚款", '行政拘留', '吊销许可证执照', '暂扣',
                                 '责令停产停业', '没收非法所得/没收非法财物',
                                 '警告', '其他']  # 这个指标的分类是按列展开的，如IS_FINE等（顺序需固定，修改需要同步修改计算逻辑）
        self.order_punish_cycledays = ["立案阶段", "调查取证阶段", "审查决定阶段", "处罚执行阶段", "结案阶段"]
        self.order_punish_source = self.get_order('standard_punish_source.csv')
        self.order_punish_dangshirentype_before = self.get_order('standard_punish_dangshirentype.csv')[:-2]
        self.order_punish_dangshirentype_after = self.get_order('standard_punish_dangshirentype.csv')[:-2]
        self.order_punish_dangshirentype_after[0] = "自然人"
        self.order_punish_dangshirentype_after.insert(0, "个体工商户")
        self.order_punish_seg = self.get_order('standard_punish_seg.csv')
        self.order_punish_type = [1, 2]
        # 标准-职权
        self.order_power_type = self.get_order('standard_power_type.csv')
        # 标准-法律
        self.order_law_type = self.get_order('standard_law_type.csv')
        self.order_law_typerank = {"法律": 1, "行政法规": 2, "特区法规": 3, "地方性法规": 4, "部门规章": 5, "政府规章": 6, "其他": 7}
        ######################################################################################################
        # 映射
        self.time_mapping = {
            "month": ([str(i) + '月' for i in range(1, 13)], "当年"),
            "quarter": (['第一季度', '第二季度', '第三季度', '第四季度'], "季度"),
            "halfyear": (['上半年', '下半年'], "半年")}
        self.punishtype_mapping = {
            "norm": {"1": "normalCase", "2": "easyCase"},
            "abnorm": {"1": "generalLaw", "2": "easyLaw"},
            "chinese": {"1": "一般", "2": "简易"},
            "chinesefull": {"1": "一般案件", "2": "简易案件"}}
        self.powertype_mapping = {i: "qt" for i in self.order_power_type}
        self.powertype_mapping["行政处罚"] = "cf"
        self.powertype_mapping["行政许可"] = "xk"
        self.powertype_mapping["行政强制"] = "qz"
        self.powertype_mapping["行政检查"] = "jcs"
        self.lawtype_mapping = {"法律": "flValue", "行政法规": "xzfgValue", "特区法规": "tqfgValue", "部门规章": "bmgzValue", "地方性法规": "dfxfgValue", "政府规章": "zfgzValue", "其他": "qtValue"}

    def get_order(self, order_name):
        list_ = pd.read_csv(os.path.join(self.path_standard, order_name)).iloc[:, 2].dropna().values
        li = []
        for i in list_:
            if i not in li:
                li.append(i)
        return li


class JsonUpdate(BaseJsonUpdate):
    def __init__(self):
        super().__init__()

    @staticmethod
    def change_category(df, item, order):
        if item:
            df[item[0]] = pd.Categorical(df[item[0]], categories=order, ordered=True)

    def get_category(self, df, nonega=False):
        """
        :param df: 需要改变的表格数据
        :param nonega: 调控是否含公安
        :return: 修改后的表格
        """
        # 基础分类
        year_name = [i for i in list(df.columns) if 'YEAR' in i]
        hangye_name = [i for i in list(df.columns) if 'HANGYE' in i]
        quyu_name = [i for i in list(df.columns) if 'QUYU' in i]
        self.change_category(df, year_name, self.order_year)
        self.change_category(df, quyu_name, self.order_quyu)
        if not nonega:
            self.change_category(df, hangye_name, self.order_hangye)
        else:
            self.change_category(df, hangye_name, self.order_hangye_nonega)

        # 其他分类
        cat_list = ["ENFORCEPEO_EDU", "ENFORCEPEO_JOBCLASS", "ENFORCEPEO_STAFFTYPE",
                    "ENFORCEPEO_POLITIC", "ENFORCEPEO_SEX", "ENFORCEPEO_AGE",
                    "POWER_TYPE",
                    "ORG_LEVEL",
                    "SUB_LEVEL",
                    "LAW_TYPE",
                    "MONTH", "QUARTER", "HALFYEAR",
                    "PUNISH_SOURCE", "PUNISH_DANGSHIRENTYPE_BEFORE", "PUNISH_DANGSHIRENTYPE_AFTER" ,
                    "PUNISH_TYPE", "PUNISH_SEG"

                    ]
        command_find = """%s_name = [i for i in list(df.columns) if i == "%s"]"""
        command_change = """self.change_category(df, %s_name, self.order_%s)"""
        for cat in cat_list:
            exec(command_find % (cat.lower(), cat))
            exec(command_change % (cat.lower(), cat.lower()))
        return df

    def get_value(self, df, col, multi=1, jduge_sum=False):
        """
        :param df:
        :param col:
        :param jduge_sum: 最后分组之后是否求和
        :param jduge_float: 最后分组之后是否是浮点数（保留小数位数，默认整数）
        :return: 空值以0填充
        """
        df[col].fillna(0, inplace=True)
        if not jduge_sum:
            try:
                return round(float(df[col]) * multi, self.sig_dig) if any(df[col]) else 0
            except:
                print('ATTENTION!!!, USING SUM() AFTER GROUPBY')
                return round(float(sum(df[col])) * multi, self.sig_dig) if any(df[col]) else 0
        else:
            return round(float(sum(df[col])) * multi, self.sig_dig) if any(df[col]) else 0

    @staticmethod
    def get_df(df):
        return pd.DataFrame(df[1])

    def json_io(self, json_name, content_dict, iscf=False):
        """
        :param json_name: 目标json的名称（只有文件名）
        :param content_dict: {方法名称: 对应方法}
        :return: 无
        """
        parent_path = self.path_tar_punish if iscf else self.path_tar
        with open(os.path.join(parent_path, json_name), 'r', encoding='utf-8') as json_read:
            load_json = json.load(json_read)
        for name, content in content_dict.items():
            load_json[name] = content
        with open(os.path.join(parent_path, json_name), 'w', encoding='utf-8') as dump_f:
            json.dump(load_json, dump_f, ensure_ascii=False, indent=4)


class PyStart(SettingsInfo):
    def __init__(self):
        super().__init__()
        python_list = ["theme2json_home.py", "theme2json_law.py", "theme2json_power.py", "theme2json_punish.py",
                       "theme2json_enforcepeo.py"]
        self.path_python_list = [os.path.join(self.path_base, 'command', 'command_json_update', i) for i in python_list]
        t0 = time.time()
        log_path = os.path.join(self.path_base, 'command', 'excute_log')
        with open(os.path.join(log_path, 'json_update'), 'a', encoding='utf-8') as f:
            for py in python_list:
                t = time.time()
                os.system(self.path_python + ' ' + os.path.join(self.path_base, 'command', 'package', py))
                t_ = time.time()
                f.write(py + '-----------' + str(int(t_ - t)) + '\n')
            f.write('-----------' + str(int(time.time() - t0)) + '-----------')
            f.write('----------------------')
            f.write('----------------------')

