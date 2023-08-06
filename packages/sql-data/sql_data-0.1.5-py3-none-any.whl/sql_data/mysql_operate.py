"""
Mysql database operation methods
"""
import pymysql
import pandas as pd
import pymysql.cursors
from sqlalchemy import create_engine
import os
import configparser

_config = configparser.ConfigParser()
_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mysql_config.conf")
_conf_path = str(_config_path)
_config.read(_config_path, encoding="utf-8")


class Mysql:
    """
    Read the configuration through mysql_config.conf
    """

    def __init__(self, db_ip, db_name):
        self.host = _config.get(db_ip, "host")
        self.port = int(_config.get(db_ip, "port"))
        self.db_user = _config.get(db_ip, "db_user")
        self.db_pwd = _config.get(db_ip, "db_pwd")
        self.db_name = db_name
        self._conn = None
        self._connect()

    def _connect(self):
        if not self._conn:
            self._conn = pymysql.connect(host=self.host, port=self.port, user=self.db_user, passwd=self.db_pwd,
                                         db=self.db_name, charset='utf8', cursorclass=pymysql.cursors.DictCursor)

    def _con_close(self):
        if self._conn:
            self._conn.close()
            self._conn = None

    @staticmethod
    def _del_cursor(cur):
        if cur:
            cur.close()

    def _new_cursor(self):
        cur = self._conn.cursor()
        if cur:
            return cur
        else:
            raise 'Error: Get New Cursor Failed'

    def exec(self, sql):
        """
        对数据库执行增、删、改操作，传入需要执行的SQL语句
        :param sql:
        """
        cur = self._new_cursor()
        try:
            cur.execute(sql)
            self._conn.commit()
        except Exception as e:
            if str(e).find("Duplicate entry") == -1:
                cur.rollback()
                raise f'Exec Sql Failed: {e}'
        finally:
            self._del_cursor(cur)
            self._con_close()

    def get_data_from_mysql(self, sql):
        """
        从数据库中获取DataFrame数据
        :param sql:
        :return: DataFrom
        """
        db_url = (
            '{driver}://{user}:{pwd}@{host}:{port}/{name}?charset=utf8'.format(driver='mysql+pymysql',
                                                                               user=self.db_user,
                                                                               port=self.port, pwd=self.db_pwd,
                                                                               host=self.host, name=self.db_name))
        try:
            engine = create_engine(db_url)
            df = pd.read_sql_query(sql, engine)
            return df
        except Exception as e:
            raise f'Data acquisition failure: {e}'
        finally:
            self._con_close()

    def saved_data_to_mysql(self, df, tabel_name, if_exists='append', index=False):
        """
        将DataFrame存储到mysql数据库的mysql_tabel中
        :param df:
        :param tabel_name:
        :param if_exists:
        :param index:
        """
        db_url = (
            '{driver}://{user}:{pwd}@{host}:{port}/{name}?charset=utf8'.format(driver='mysql+pymysql',
                                                                               user=self.db_user,
                                                                               port=self.port, pwd=self.db_pwd,
                                                                               host=self.host, name=self.db_name))
        try:
            engine = create_engine(db_url)
            df.to_sql(name=tabel_name, con=engine, if_exists=if_exists, index=index)
        except Exception as e:
            raise f'Data storage failure: {e}'
        finally:
            self._con_close()


def get_config_path():
    """
    按照以下格式进行mysql_config.conf文件的配置
    :return: mysql_config.conf 文件位置
    """
    w_b = '''
[127.0.0.1]
HOST = 127.0.0.1
PORT = 3306
DB_USER = root
DB_PWD = 12345
    '''
    if not os.path.isfile(_conf_path):
        with open(_conf_path, 'w') as f:
            f.write(w_b)
    return _conf_path


def exec_sql_mysql(sql, db_name="algorithm", db_ip="127.0.0.1"):
    """
    对mysql数据库中的db_name数据库执行sql语句
    :param sql: SQL语句
    :param db_name: 数据库名称
    :param db_ip: 数据库label
    """
    pym = Mysql(db_ip=db_ip, db_name=db_name)
    try:
        pym.exec(sql)
    except Exception as err:
        print(err)


def get_data_from_mysql(sql, db_name="algorithm", db_ip="127.0.0.1"):
    """

    :param sql: SQL语句
    :param db_name: 数据库名称
    :param db_ip: 数据库label
    :return: 查询结果
    """
    pym = Mysql(db_ip=db_ip, db_name=db_name)
    df = pym.get_data_from_mysql(sql)
    return df


def saved_data_to_mysql(df, mysql_table, if_exists="append", index=False, db_name="algorithm",
                        db_ip="127.0.0.1"):
    """
    将DataFrame数据保存到mysql数据库中
    :param df: 需要保存的DataFrame
    :param mysql_table: 数据库表名
    :param if_exists: 采取的保存数据的方式
    :param index: 是否保存DataFrame的索引
    :param db_name: 数据库名称
    :param db_ip: 数据库label
    """
    pym = Mysql(db_ip=db_ip, db_name=db_name)
    pym.saved_data_to_mysql(df, mysql_table, if_exists=if_exists, index=index)
