# -*- coding: utf-8 -*-
# @Time    : 2019/9/18 20:08
# @Author  : Cookie付尧
# @Email   : fuyao@beidasoft.com
# @File    : app_change.py
# @Software: PyCharm

import os
from .base import SettingsInfo
import xml.dom.minidom
import re
import datetime

"""
本程序是将获得的设置信息修改程序，包含
    1. FileEncoding 文件编码修改, 继承自Base的SettingsInfo类（设置文件信息）
        构造函数：初始化了读取csv和写出csv的列表
        get_file_node函数：查找并更新读取csv的列表，写出csv的列表
        node_change函数：接受参数：读取 或 写出，判断编码是否一致，一致则退出，通知用户，不一致则更改编码
        app_change函数：程序入口：1. 更新列表  2. 更改内容
    2. 数据库修改
    3. epf修改
"""


class BaseAppChange(SettingsInfo):
    def __init__(self):
        super().__init__()
        self.csv_read_list, self.csv_write_list = [], []
        self.raw2standard = {"read": [], "write": []}
        self.raw2busin = {"read": [], "write": []}
        self.busin2theme = {"read": [], "write": []}
        self.work_flow_list = ['standard_extract', 'data_extract', 'data_calculate']
        self.raw_database["IP"] = "jdbc:oracle:thin:@" + self.raw_database["IP"]
        self.busin_database["IP"] = "jdbc:oracle:thin:@" + self.busin_database["IP"]

    @staticmethod
    def get_tarXML_from_workflowlist(**kwargs):
        for work_flow in os.listdir(kwargs['workflowlist']):  # 找到每一大类路径下的流程
            work_flow_path = os.path.join(kwargs['workflowlist'], work_flow)
            if os.path.isdir(work_flow_path):  # 如果是流程（而不是文件）
                for ves, tar in zip(kwargs['ves'], kwargs['tar']):
                    ves += [os.path.join(kwargs['workflowlist'], work_flow, node, 'settings.xml') \
                            for node in os.listdir(work_flow_path) if node.startswith(tar)]

    def node_change(self, **kwargs):
        """
        :param kwargs:
            - path：需要修改的settings.xml路径列表
            - pos：需要修改的位置(第几个entry-0开始)（每个settings.xml所有需要修改的位置）
            - value：需要修改的内容列表
        """
        path_list, pos_list, value_list = kwargs['path'], kwargs['pos'], kwargs['value']
        log_path = os.path.join(self.path_base, 'command', 'excute_log')
        os.system('mkdir -p %s' % log_path)
        with open(os.path.join(log_path, 'wrong'), 'a') as f:
            f.write('执行时间:' + str(datetime.datetime.now()) + '\n')
            for xml_path in path_list:
                dom = xml.dom.minidom.parse(xml_path)
                entry = dom.documentElement.getElementsByTagName('entry')
                for pos, value in zip(pos_list, value_list):
                    tar_value_origin = entry[pos]
                    try:
                        if tar_value_origin.getAttribute('value') == value:  # 如果和目标修改相同
                            continue  # 跳过
                        else:
                            print(f"{tar_value_origin.getAttribute('value')} ----> {value} ---changing")
                            tar_value_origin.setAttribute("value", value)
                            with open(xml_path, 'w', encoding='UTF-8') as fh:
                                dom.writexml(fh, indent='', addindent='\t', newl='\n', encoding='UTF-8')
                            print(f"{value}. Has Changed")
                    except:
                        f.write(xml_path + '\n')


class FileEncoding(BaseAppChange):
    def __init__(self):
        super().__init__()
        path_list = [os.path.join(self.path_base, 'workflow', i) for i in self.work_flow_list]  # 找到workflow下的三大类路径（标准抽取，数据抽取，数据计算）
        for workflow_list in path_list:
            self.get_tarXML_from_workflowlist(workflowlist=workflow_list,
                                              ves=[self.csv_read_list, self.csv_write_list],
                                              tar=['CSV Reader', 'CSV Writer'])
        self.node_change(path=self.csv_read_list, pos=[12], value=[self.file_encoding])
        self.node_change(path=self.csv_write_list, pos=[14], value=[self.file_encoding])


class DataBaseChange(BaseAppChange):
    def __init__(self):
        super().__init__()
        for workflowtype, workflowtype_ves in zip(self.work_flow_list, [self.raw2standard, self.raw2busin, self.busin2theme]):
            self.get_tarXML_from_workflowlist(workflowlist=os.path.join(self.path_base, 'workflow', workflowtype),
                                              ves=[workflowtype_ves['read'], workflowtype_ves['write']],
                                              tar=['Database Table Connector', 'Database Connector'])
        """
        标准抽取-读：raw
        数据抽取-读：raw，写：busin
        数据计算-读：busin，写：busin（为了计算同比环比有一个写出到busin的操作）
        """
        # 标准抽取：读raw_database
        self.node_change(path=self.raw2standard['read'],
                         pos=[5, 7, 8],
                         value=[self.raw_database['IP'], self.raw_database['USER'],
                                self.raw_database['PASSWORD_ENCRYPTED']])
        # 数据抽取：读raw_database
        self.node_change(path=self.raw2busin['read'],
                         pos=[5, 7, 8],
                         value=[self.raw_database['IP'], self.raw_database['USER'],
                                self.raw_database['PASSWORD_ENCRYPTED']])
        # 数据抽取：写busin_database
        self.node_change(path=self.raw2busin['write'],
                         pos=[3, 5, 6],
                         value=[self.busin_database['IP'], self.busin_database['USER'],
                                self.busin_database['PASSWORD_ENCRYPTED']])
        # 数据计算：读busin_database
        self.node_change(path=self.busin2theme['read'],
                         pos=[5, 7, 8],
                         value=[self.busin_database['IP'], self.busin_database['USER'],
                                self.busin_database['PASSWORD_ENCRYPTED']])
        # 数据计算：写busin_database
        self.node_change(path=self.busin2theme['write'],
                         pos=[3, 5, 6],
                         value=[self.busin_database['IP'], self.busin_database['USER'],
                                self.busin_database['PASSWORD_ENCRYPTED']])


class EPFChange(SettingsInfo):
    def __init__(self):
        super().__init__()
        with open(self.path_epf, 'r') as f:
            epf_content = f.read()
        epf_content = re.sub('/instance/org.knime.workbench.core/database_drivers=.*?jar',
               '/instance/org.knime.workbench.core/database_drivers=' + self.path_ojdbc, epf_content)
        with open(self.path_epf, 'w') as f:
            f.write(epf_content)

