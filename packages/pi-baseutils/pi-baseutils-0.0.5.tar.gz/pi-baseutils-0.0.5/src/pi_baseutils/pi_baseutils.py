# -*- encoding: utf-8 -*-
"""
Date: 2022-03-22 15:12:24
LastEditors: ruohua.li
LastEditTime: 2022-06-07 14:42:21
"""

import os

try:
    from setting import CPROFILE_LOG_PATH, DEBUG, LOG_PATH #type:ignore
except:
    DEBUG = False
    CPROFILE_LOG_PATH = os.getcwd() + "/Logs"
    LOG_PATH = os.getcwd() + "/Logs"  # 根目录下

__a__ = [
    "read_dataframe",
    "save_dataframe",
    "two_int_date_subtract",
    "add_month_to_date",
    "SingletonLogger",
    "make_logger",
    "func_cprofile",
    "DataCheck",
    "DbInfo",
]

################################################################################
### 读写数据
################################################################################


def read_dataframe(
    source, DEBUG_source=None, query=None, columns=None, Logger=None
):
    """从数据库（Mongo、SQL）、文件（Excel）读入数据,根据source自动判断
    Args：
       source：数据源，数据库信息类或者excel文件地址
       DEBUG_source：如果是DEBUG状态，则数据源选用DEBUG_source
       query：如果源是MYSQL则是查询语句，mongo则是筛选条件
       columns：想要提取的列名；如果源是MYSQL则和query二选一；
       Logger：默认打印数据源、列名和shape，如果传入logger则会输出到日志
    """
    # 输出
    # 如果指定logger，则写入日志
    if Logger:
        printer = Logger.info
    else:
        printer = print

    # 如果有指定DEBUG状态的数据源，则DEBUG=True时使用DEBUG_source
    if DEBUG:
        if DEBUG_source:
            source = DEBUG_source
        else:
            printer("当前为DEBUG模式，但DEBUG_source未指定,按source读数据！！！！！！！！！")
    # 读数据
    if isinstance(source, str):
        df = _read_file(source, columns=columns)
    elif source.INSTANCE == "MYSQL":
        df = _read_mysql_to_df(source, query, columns)
    else:
        df = _find_mongo_to_df(source, query, columns)

    if isinstance(source, str):
        printer(f"数据读入：{source}")
    else:
        if source.INSTANCE == "MYSQL" and query:
            table = "by query"
        else:
            table = source.TABLE
        printer(f"数据读入：{source.NAME} -> {source.DB} -> {table}")
    printer(f"数据列：{df.columns.tolist()}")
    printer(f"数据量：{df.shape}")

    return df


def _find_mongo_to_df(config, query=None, columns=None):
    """从mongo数据库读入数据
       pymongo 4.0 之后有些改动，但是目前我们的 MongoDB 版本低于3.6 没法测试
    Args：
       config：数据库信息类
       query：查询语句
       columns：指定提取的列名；
    """
    import pandas as pd
    import pymongo
    from urllib.parse import quote_plus

    # 有些密码带 @ 字符的特殊处理
    PASSWORD = quote_plus(config.PASSWORD)

    mongo_url = f"mongodb://{config.USER}:{PASSWORD}@{config.HOST}:{config.PORT}/?authSource={config.AUTHENTICATION}&authMechanism=SCRAM-SHA-1"
    myclient =  pymongo.MongoClient(mongo_url)

    mydb = myclient[config.DB]
    mycol = mydb[config.TABLE]

    if not query:
        query = {}
    if columns:
        cols_dict = {}
        for col in columns:
            cols_dict[col] = 1
        data = mycol.find(query, cols_dict)
    else:
        data = mycol.find(query)
    df = pd.DataFrame(data)  # type: ignore
    return df


def _read_mysql_to_df(config, query=None, columns=None):
    """从SQL数据库读入数据
    Args：
       config：数据库信息类
       query：查询语句
       columns：指定提取的列名；和query二选一；
       如果query和columns都没指定，怎会读全表
    """
    import pandas as pd

    engine = engine_to_mysql(config)

    if query:
        pass
    elif columns:
        columns = [f'`{x}`' for x in columns]
        cols = ",".join(columns)
        query = f"select {cols} from {config.TABLE}"
    else:
        query = f"select * from {config.TABLE}"
    connection = engine.raw_connection()
    df = pd.read_sql_query(query, connection)
    return df


def save_dataframe(Db, df, DEBUG_Db=None, if_exists="append", Logger=None):
    """保存DataFrame到数据库（Mongo、SQL）、文件（Excel）,根据Db自动判断
    Args：
       Db：保存地址信息，数据库信息类或者excel文件地址
       df:待保存的数据
       DEBUG_Db：如果是DEBUG状态，则保存数据地址选用DEBUG_Db
       if_exists：如果表存在保存到数据库的方式，默认为'append',传入'replace'即全表替换；
                  也可以指定一个列名（通常是用于版本控制的列，比如日期、版本号，默认待写入数据仅有一个非重复的值），
                  根据该列名将待写入数据进行覆盖写入（场景是同一个批次的数据多次计算，历史记录表需要覆盖写入）
       Logger：默认打印写入前后的数据库数据量信息，如果传入logger则会输出到日志
    """
    # 输出
    # 如果指定logger，则写入日志
    if Logger:
        printer = Logger.info
    else:
        printer = print
    # import pandas as pd
    if DEBUG:
        if DEBUG_Db:
            Db = DEBUG_Db
        else:
            printer("当前为DEBUG模式，但DEBUG_Db未指定,数据未写入！！！！！！！！！")
            return
    # 如果指定列名，则根据df的唯一值删除数据库的重复值
    if if_exists not in ["append", "replace"]:
        # 如果不存在df.columns，则会报错
        uni_col = df[if_exists].unique().tolist()
        if len(uni_col) > 1:
            raise KeyError(if_exists, "不唯一！")
        else:
            version = uni_col[0]

    # 保存数据
    if isinstance(Db, str):
        _save_file(Db, df)
    elif Db.INSTANCE == "MYSQL":
        engine = engine_to_mysql(Db)
        start_len = engine.execute(f"select count(*) from {Db.TABLE}").scalar()
        if if_exists not in ["append", "replace"]:  # 如果指定列名
            if df[if_exists].dtypes == "object":  # 字符串特殊处理
                version = "'" + version + "'"  # type: ignore
            effect_len = engine.execute(
                f"select count(*) from \
                {Db.TABLE} where {if_exists}={version}"  # type: ignore
            ).scalar()
            engine.execute(
                f"delete from {Db.TABLE} where {if_exists}={version}"  # type: ignore
            )
            _write_df_to_mysql(Db, df, engine=engine)
        else:
            # 下面函数实现'append'和'replace'
            _write_df_to_mysql(Db, df, if_exists=if_exists, engine=engine)
        end_len = engine.execute(f"select count(*) from {Db.TABLE}").scalar()
    else:  # mongo
        con = connection_to_mongo(Db)
        start_len = con.count_documents({})
        if if_exists not in ["append", "replace"]:  # 如果指定列名
            effect_len = con.count_documents({if_exists: version})  # type: ignore
            con.delete_many({if_exists: version})  # type: ignore
            _write_df_to_mongo(Db, df, if_exists="append", con=con)
        else:
            # 下面函数实现'append'和'replace'
            _write_df_to_mongo(Db, df, if_exists=if_exists, con=con)
        end_len = con.count_documents({})
        # df = find_mongo_to_df(source,query,columns)

    printer(f"DataFrame数据量：{df.shape}")
    if not isinstance(Db, str):
        printer(f"数据写入：{Db.NAME} -> {Db.DB} -> {Db.TABLE}")
        printer(f"写入前数据量：{start_len}")  # type: ignore
        printer(f"写入后数据量：{end_len}")  # type: ignore
        if if_exists not in ["append", "replace"]:
            printer(f"指定列{if_exists}的当前版本为{version}")  # type: ignore
            printer(f"根据当前版本{version}，删除的数据量：{effect_len}")  # type: ignore


def _read_file(file_path, columns=None):
    import pandas as pd

    _type = file_path.split(".")[-1]
    if _type == "xlsx":
        df = pd.read_excel(file_path)
    elif _type == "csv":
        df = pd.read_csv(file_path)
    elif _type == "pkl":
        df = pd.read_pickle(file_path)
    else:
        raise KeyError("文件暂时不支持！")
    if columns:
        df = df[[columns]]
    return df


def _save_file(file_path, df):
    _type = file_path.split(".")[-1]
    if _type == "xlsx":
        df.to_excel(file_path, index=None)
    elif _type == "csv":
        df.to_csv(file_path, index=None)
    elif _type == "pkl":
        df.to_pickle(file_path)
    else:
        raise KeyError("文件暂时不支持！")


def engine_to_mysql(config):
    from sqlalchemy import create_engine
    from urllib.parse import quote_plus

    # 有些密码带 @ 字符的特殊处理
    PASSWORD = quote_plus(config.PASSWORD)

    engine = create_engine(
        f"mysql+pymysql://{config.USER}:{PASSWORD}@\
{config.HOST}:{config.PORT}/{config.DB}?charset=utf8"
    )
    return engine


def _write_df_to_mysql(config, df, if_exists="append", engine=None):
    """保存DataFrame到数据库SQL
    Args：
       config：数据库信息类
       df:待保存的数据
       if_exists：如果表存在保存到数据库的方式，默认为'append',传入'replace'即全表替换；
    """
    if not engine:
        engine = engine_to_mysql(config)
    df.to_sql(config.TABLE, engine, if_exists=if_exists, index=False)


def connection_to_mongo(config):
    import pymongo

    client = pymongo.MongoClient(config.HOST, config.PORT)
    mydb = client[config.AUTHENTICATION]
    mydb.authenticate(config.USER, config.PASSWORD)
    insert_db = client[config.DB]
    mytable = insert_db.get_collection(config.TABLE)
    return mytable


def _write_df_to_mongo(config, df, if_exists="append", con=None):
    """保存DataFrame到数据库mongo
    Args：
       config：数据库信息类
       df:待保存的数据
       if_exists：如果表存在保存到数据库的方式，默认为'append',传入'replace'即全表替换；
    """
    if not con:
        con = connection_to_mongo(config)
    if if_exists == "replace":
        con.delete_many({})
    data = df.to_dict(orient="records")
    con.insert_many(data)


################################################################################
### 工具函数
################################################################################


def two_int_date_subtract(start, end):
    """用于计算int类型的月份差,end-start；
    date格式支持6位或8位（202202或20220201）,但不会做合规检查
    Args：
       end：结束日期，int格式支持6位或8位
       start:开始日期，int格式支持6位或8位
    """
    if end > 1000000:
        start = int(str(start)[:6])
        end = int(str(end)[:6])

    start_y = start // 100
    start_m = start % 100
    end_y = end // 100
    end_m = end % 100

    y_diff = (end_y - start_y) * 12
    m_diff = end_m - start_m
    months = y_diff + m_diff
    return months


def add_month_to_date(date, monthnum):
    """用于计算int类型的年月加上月份，也可以传负值，例如202105-10=202007
    Args：
       date：日期，格式支持6位或8位（202202或20220201）,但不会做合规检查
       monthnum:月数，int格式支持6位或8位
    """
    days = False
    if date > 1000000:
        days = date % 100
        date = int(str(date)[:6])

    # 这是月份（位置）list
    month_list = list(range(1, 13))
    # 初始化
    year = date // 100
    month = date % 100
    # 月份处理
    # 实际是循环队列的方法
    month_index = month - 1  # 减1是位置list的下标，下标从0开始
    month_index = month_index + monthnum
    month = month_list[month_index % 12]
    # 年度处理
    year = year + month_index // 12
    result = year * 100 + month
    # 加上原来的日(days)
    if days:
        if month == 2 and days > 28:
            result = result * 100 + 28
        elif month in [4, 6, 9, 11] and days > 30:
            result = result * 100 + 30
        else:
            result = result * 100 + days
    return result


################################################################################
### 日志
################################################################################


# 单例模式，限制下面SingletonLogger、data_check只能存在单个实例
def Singleton(cls):
    _instance = {}

    def _singleton(*args, **kargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kargs)
        return _instance[cls]

    return _singleton


@Singleton
class SingletonLogger:
    """统一调用日志类，日志同时输出到终端，可根据Setting指定日志文件夹；"""

    def __init__(self):
        import os
        import time
        import logging

        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)  # Log等级总开关
        # 第二步，创建一个handler，用于写入日志文件
        rq = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        logfile = f"{LOG_PATH}/{rq}.log"
        fh = logging.FileHandler(logfile, mode="w")
        sh = logging.StreamHandler()
        fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关
        # 第三步，定义handler的输出格式
        formatter = logging.Formatter(
            "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
        )
        fh.setFormatter(formatter)
        sh.setFormatter(formatter)
        # 第四步，将logger添加到handler里面
        self.logger.addHandler(fh)
        self.logger.addHandler(sh)



import json
import datetime
import logging
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):    # 日期和时间
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):    # 日期
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, datetime.time):    # 时间
            return obj.strftime('%H:%M:%S')
        else:
            return json.JSONEncoder.default(self, obj)

class JSONFormatter(logging.Formatter):
    REMOVE_ATTR = ["exc_text", "stack_info", "created", "msecs", "relativeCreated", "exc_info",
                   "msg", "args", "levelno", "pathname", "lineno", "funcName", "thread",
                   "threadName", "processName", "process"]
    @classmethod
    def build_record(cls, record):
        return {attr_name: record.__dict__[attr_name] for attr_name in record.__dict__ if attr_name not in cls.REMOVE_ATTR}

    @classmethod
    def set_format_time(cls, msg_dict):
        now = datetime.datetime.now()
        format_time = now.strftime("%Y-%m-%d %H:%M:%S")
        msg_dict['datetime'] = format_time
        return format_time

    def format(self, record):
        msg_dict = self.build_record(record)
        self.set_format_time(msg_dict)  # set time
        if isinstance(record.msg, dict):
            msg_dict['msg'] = record.msg  # set message
        else:
            if record.args:
                msg_dict['msg'] = "'" + record.msg + "'," + str(record.args).strip('()')
            else:
                msg_dict['msg'] = record.msg
        if record.exc_info:
            msg_dict['exc_info'] = self.formatException(record.exc_info)
        return json.dumps(msg_dict, ensure_ascii=False, cls=ComplexEncoder)



def make_json_logger(name='root'):
    """统一正式服务调用日志类，json格式，一般仅保留报错信息（存活监测5秒一次，并且接口信息java已经有日志）"""

    logger = logging.getLogger(name)

    logger.setLevel(logging.INFO)  # type:ignore # Log等级总开关
    # 第二步，创建一个handler，用于写入日志文件
    rq = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    if not os.path.exists(LOG_PATH):
        os.makedirs(LOG_PATH)
    logfile = f"{LOG_PATH}/{rq}_{name}.log"
    fh = logging.FileHandler(logfile, mode="w")
    sh = logging.StreamHandler()
    fh.setLevel(logging.INFO)  # 输出到file的log等级的开关
    # 第三步，定义handler的输出格式
    formatter = logging.Formatter(
        "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
    )
    fh.setFormatter(JSONFormatter())
    sh.setFormatter(JSONFormatter())
    # 第四步，将logger添加到handler里面
    logger.addHandler(fh)  # type:ignore
    logger.addHandler(sh)  # type:ignore
    return logger  # type:ignore


################################################################################
### 装饰器
################################################################################


def func_cprofile(f):
    import os
    from functools import wraps
    from datetime import datetime as dt

    """
   将函数中耗时最多的前200项保存到指定日志；默认DEBUG=True启用；可根据Setting指定日志文件夹；
    """
    if DEBUG:
        import cProfile, pstats, io

        @wraps(f)
        def wrapper(*args, **kwargs):
            profile = cProfile.Profile()
            name = f.__name__
            try:
                profile.enable()
                result = f(*args, **kwargs)
                profile.disable()
                return result
            finally:
                s = io.StringIO()
                ps = (
                    pstats.Stats(profile, stream=s)
                    .sort_stats("cumulative")
                    .print_stats(200)
                )
                if not os.path.exists(CPROFILE_LOG_PATH):
                    os.makedirs(CPROFILE_LOG_PATH)
                with open(
                    f'{CPROFILE_LOG_PATH}/{dt.now().strftime("%Y%m%d_%H%M%S")}_{name}_cProfile.log',
                    "w",
                ) as fp:
                    fp.write(s.getvalue())

        return wrapper

    else:

        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper


def run_time(f):
    """输出函数用时；如果传入Logger类自动写日志；"""
    from functools import wraps
    from datetime import datetime as dt
    import logging

    name = f.__name__

    @wraps(f)
    def wrapper(*args, **kwargs):
        printer = print
        for i in args:
            if isinstance(i, logging.RootLogger):
                printer = i.info
                break
        start = dt.now()
        printer("函数 {} 参数: {} 开始运行".format(name, args))
        result = f(*args, **kwargs)
        end = dt.now()
        printer("函数 {} 用时:{}(s)".format(name, (end - start).total_seconds()))
        return result

    return wrapper


################################################################################
### 类
################################################################################


class DbInfo:
    """数据库信息的父类，属性必须在 NAME_LIST 范围
    属性必须大写，一旦赋值不能删除、不能修改
    """

    class DbInfoError(TypeError):
        pass

    class DbInfoCaseError(DbInfoError):
        pass

    NAME_LIST = (
        "NAME",
        "INSTANCE",
        "HOST",
        "PORT",
        "USER",
        "PASSWORD",
        "AUTHENTICATION",
        "DB",
        "TABLE",
    )

    def __setattr__(self, name: str, value) -> None:
        if name in self.__dict__:
            raise self.DbInfoError(f"已经包含{name}，不能再次赋值")
        # if not name.isupper():
        #     raise self.DbInfoCaseError(f"常量 {name} 不是全大写")
        if name in DbInfo.NAME_LIST:
            self.__dict__[name] = value
        else:
            raise self.DbInfoError(f"NAME_LIST不包含{name} 属性，不能增加")

    def __delattr__(self, name):
        if name in self.__dict__:
            raise self.DbInfoError(f"不能删除 {name} 属性")


@Singleton
class DataCheck:
    """用于对项目主要数据的变化做跟踪检查，因此设定只能存在一个实例
    Args:
      df:主要数据，可通过 compare_lastest 函数和最后版本（对比后会被加入记录，即最后版本）
      target：主键，主要关注的列，默认是TrimId
    result:
        cols_add:增加的列
        cols_reduce：减少的列
        target_reduce：主键非重复数量减少情况
        len_reduce：总行数减少量（负数即增加了）
    """

    def __init__(self, df, target="TrimId"):
        self.__data = []
        self.__count = -1
        self.__target = target
        self.__add_df(df)  # 初始化目标df（加入第一个df）

    # 和最后版本数据做对比，并把要对比的数据加入记录（只有这里能增加df记录）
    def compare_lastest(self, df):
        self.__add_df(df)
        result = self.__compare(self.__count - 1)
        return result

    # 最后版本数据和最开始（第一次）的数据做对比
    def compare_origin(self):
        result = self.__compare(0)
        return result

    # 返回全部的列变化
    def get_all_columns(self):
        result = [x["columns"] for x in self.__data]
        return result

    # 返回全部目标（主键）非重复数量（unique）变化
    def get_all_target_len(self):
        result = [x["target_len"] for x in self.__data]
        return result

    # 返回全部行数变化
    def get_all_len(self):
        result = [x["len"] for x in self.__data]
        return result

    # 核心对比函数
    def __compare(self, index_):
        if self.__count < 1:
            return "只有一条数据早着呢！"
        else:
            r_dict = {}
            last = self.__data[self.__count]
            compare = self.__data[index_]
            r_dict["cols_add"] = [
                x for x in last["columns"] if x not in compare["columns"]
            ]
            r_dict["cols_reduce"] = [
                x for x in compare["columns"] if x not in last["columns"]
            ]
            r_dict["target_reduce"] = last["target_len"] - compare["target_len"]
            r_dict["len_reduce"] = last["len"] - compare["len"]

            return r_dict

    # 将新的df加入到记录历史
    def __add_df(self, df):
        tmp = {}
        tmp["columns"] = df.columns.tolist()
        tmp["target_len"] = len(df[self.__target].unique())
        tmp["len"] = len(df)
        self.__data.append(tmp)
        self.__count += 1
