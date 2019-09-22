## 深圳大屏后台计算逻辑——调用方法
***
### 文件目录说明datashow
- datashow（所有文件的根目录-数据展示）
    - command：命令文件夹（用于存放所有命令脚本）
        - command_json_update：用于存放更新大屏json的脚本
            - theme2json_enforcepeo.py：更新执法人员页数据的脚本
            - theme2json_home.py：更新主页数据的脚本
            - theme2json_law.py：更新法律页数据的脚本
            - theme2json_power.py：更新职权页数据的脚本
            - theme2json_punish.py：更新行政处罚页数据的脚本
        - excute_log：用于存放执行日志（每部分的执行时间）
            - data_calculate：数据计算部分各流程的时间
            - data_exract：数据抽取部分各流程的时间
            - json_update：json更新部分个部分的时间
        - excute_order：用于存放各部分流程的执行顺序（可指定流程执行）
            - data_calculate_order：用于存放数据计算各指标的执行顺序
            - data_extract_order：用于存放数据抽取得到业务库的顺序
            - standard_extract_order：用于存放标准抽取得到标准库的顺序
        - **settings.json**：全局设置文件
        - **main.py**：主程序入口，用法`./root/anaconda/bin/python3 main.py`
        - **raw2standard_extract.py**：标准提取流程启动命令（当数据库中的表sys_code中的分类字段有更新时，需要启动这一命令，重新得到标准库中的文件，并手动增加大屏映射字段）
        - **app_change.py**：用于根据settings.json中的配置修改程序的脚本
    - env：环境文件夹（用于存放所有依赖环境）
        - knime：用于存放数据计算的工具
    - result：结果文件夹（用于存放标准库和计算结果）
        - standard：用于存放所有分类标准（分类代码，分类名称，大屏映射）
        - theme：用于存放所有计算结果（主题库）
    - workflow：流程文件夹（用于存放所有计算流程）
        - data_extract：用于存放数据抽取部分的所有流程
        - standard_extract：用于存放标准抽取部分的所有流程
        - data_calculate：用于存放数据计算部分的所有流程

### 配置文件说明settings.json：
- SIGNIFICANT_DIGITS：涉及除法时保留的有效数字
- FILE_ENCODING：文件编码：主要涉及标准库的标准分类和指标库的计算结果
- STATE：现在状态：DEV/PRO
    - DEV: 开发状态，将影响以下两个地方（PRO类似）
        - 数据库的连接，将通过DATABASE_DEV中的信息连接
        - 写出json的路径，将通过PATH_DEV中的路径寻找目标
- !: 出现在FILE_ENCODING（文件编码）和STATE（状态）的内容后面
    - FILE_ENCODING（文件编码）后：
        - "UTF-8!" 表示：目前是UTF-8编码（不对程序中的编码进行修改）
        - "UTF-8" 表示：将现有的文件编码改成"UTF-8"（对现有编码进行修改）
    - STATE（状态）后：
        - "DEV!"表示：
            - 通过PATH_DEV中的路径寻找目标json
            - 目前是连接开发环境中的数据库（不改当前的连接数据库的来源）
        - "DEV"表示：
            - 通过PATH_DEV中的路径寻找目标json
            - 将现在连接数据库的方式改成开发环境中的数据库（修改当前的连接数据库的来源）
> 注：数据库配置信息中的密码是经过工具加密的
> 注：result文件夹可删，每次执行会自动创建result/standard和result/theme

### 详细说明
