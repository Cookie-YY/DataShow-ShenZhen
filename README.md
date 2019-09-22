## 深圳大屏后台计算逻辑——调用方法
***

### 程序简介：
本程序是深圳项目大数据可视化的后台程序（不涉及以来环境包，和主程序目录[无法独立启动]）总共分为四个步骤：应用用户设置，标准抽取，数据抽取，数据计算，数据更新：
- 应用用户设置(apply)：将用户设置（settings.json）应用到程序上
- 标准抽取(0)：在数据库中抽取分类标准，并形成文件（允许用户在文件上自定义）
- 数据抽取(1)：将数据库的数据按照一定形式抽取出来，是数据分析的起点
- 数据计算(2)：程序的核心，计算出指定指标，到指定位置
- 数据更新(3)：将计算的结果，按照指定形式刷新到指定位置的文件（大屏读取的数据文件）

### 启动程序：
- `cd command`
- `python commanmain.py [options]`：默认不启动标准抽取
    - `-h --help`: 查看帮助
    - `-a --apply`：执行主程序前应用用户设置（setting.json）
    - `-i --include`：接受参数0，1，2，3（可多选，无连接）
        - 如`python main.py -i 0123`：启动标准抽取(0)，数据收取(1)，数据计算(2)，数据更新(3)
    - `-s --skip`：接受参数1,2,3
        - 如`python main.py -s 23`：只启动数据抽取（默认启动1，2，3）

### 文件目录说明datashow
- datashow（所有文件的根目录-数据展示）
    - command：命令文件夹（用于存放所有命令脚本）
        - excute_log：用于存放执行日志（每部分的执行时间）
            - data_calculate：数据计算部分各流程的时间
            - data_exract：数据抽取部分各流程的时间
            - json_update：json更新部分个部分的时间
            - wrong：记录错误信息
        - excute_order：用于存放各部分流程的执行顺序（可指定流程执行）
            - data_calculate_order：用于存放数据计算各指标的执行顺序
            - data_extract_order：用于存放数据抽取得到业务库的顺序
            - standard_extract_order：用于存放标准抽取得到标准库的顺序
        - package：用于存放依赖脚本
            - __init__.py：包文件头
            - app_change.py：根据用户设置更改程序主体脚本
            - base.py：所有脚本的基类（一些公共方法）
            - theme2json_*.py：修改大屏页面脚本
        - **settings.json**：全局设置文件
        - **main.py**：主程序入口，用法`./root/anaconda/bin/python3 main.py [options]`
        - **app_change.py**：用于根据settings.json中的配置修改程序的脚本
    - result：结果文件夹（用于存放标准库和计算结果）
        - standard：用于存放所有分类标准（分类代码，分类名称，大屏映射）
        - theme：用于存放所有计算结果（主题库）
    - workflow：流程文件夹（用于存放所有计算流程）
        - data_extract：用于存放数据抽取部分的所有流程
        - standard_extract：用于存放标准抽取部分的所有流程
        - data_calculate：用于存放数据计算部分的所有流程
    - README.md
    - version：版本记录
- core：用于存放主要启动程序（用于存放启动环境）
    - knime_4.0.0：用于存放数据计算的工具
    - knime.epf：knime的配置文件
    - ojdbc8.jar：oracle数据库驱动
- dependence：用于存放所有环境依赖
    - gcc
    - Anaconda3-5.3.1-Linux-x86_64.sh
    - bzip22-1.0.6.tar.gz
    - nginx-1.17.0.tar.gz
    - zlib-1.2.7.3.tar.gz
    - README：环境配置信息
    
### 配置文件说明settings.json：
- SIGNIFICANT_DIGITS：涉及除法时保留的有效数字
- FILE_ENCODING：文件编码：UTF-8/GBK:主要涉及标准库的标准分类和指标库的计算结果
- STATE：现在状态：DEV/PRO
    - DEV: 开发状态，将影响以下两个地方（PRO类似）
        - 数据库：将通过DATABASE_DEV中的信息连接（IP/USER/PASSWORD）
        - 路径：写出json的路径，将通过PATH_DEV中的路径寻找目标
        - 路径：python解释器的路径（已添加环境变量可以直接用python）
        - 路径：核心程序knime路径（默认：core/knime_4.0.0/knime）
        - 路径：核心程序knime配置文件路径（默认：core/knime.epf）
        - 路径：oracle驱动路径（默认：core/ojdbc8.jar）

> 注：数据库配置信息中的密码是经过工具加密的
> 注：theme文件夹可删，每次执行会自动创建result/theme
> 注：excute_log文件夹可删，每次执行会自动创建command/excute_log
> 注：windows下路径需要以两个反斜线分隔
