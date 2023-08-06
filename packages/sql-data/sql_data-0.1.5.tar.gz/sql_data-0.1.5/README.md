# sql-data 

一款用于mysql数据查询存储+时间格式化处理得工具



## 使用方式

1、安装 pip install sql-data==0.1.5

2、

```python
# 用于创建config默认配置并返回文件位置，请按照默认格式进行个人mysql数据库得配置
config_path = sql_data.get_config_path()
```



```.conf
[127.0.0.1]
HOST = 127.0.0.1
PORT = 3306
DB_USER = root
DB_PWD = 12345
```



## 内置函数

```python
from sql_data import exec_sql_mysql, get_data_from_mysql, saved_data_to_mysql

from sql_data import date_fmt
```

```python
sql = "select * from mysql_table"
# 获取数据 -> DataFrom
data_df = sql_data.get_data_from_mysql(sql, "db_name", "127.0.0.1")
# 数据存储
sql_data.saved_data_to_mysql(sql, "db_name", "127.0.0.1")

exec_sql = "delect from mysql_table"
## 数据删除、更改和插入
sql_data.exec_sql_mysql(exec_sql, "db_name", "127.0.0.1")
```

```python
date_value = ["2022年08月08日 19:19",
        "2022年08月08日",
        "2022-08-08 19:40",
        "2022-08-08 10:55:32",
        "08/8/2022",
        "08-08-22",
        "2022.8",
        "20220808"]
date_df = pd.DataFrame(date_value, columns=["time"])
# 对符合以上日期格式得列进行格式化转换 -> Y-M-D
date_fmt_df = date_fmt.column_fmt(date_df)

import datetime as dt
# today = "2022-09-01" or
today = dt.date.today()
# 返回days天之后得日期，days<0则计算之前日期 
fmt_date = date_fmt.day_add(today, days=7)
# 返回weeks周之后得日期，weeks<0则计算之前日期， what_day取值: [1, 7]，设置返回值为星期几得日期
fmt_date = date_fmt.week_add(today, what_day=1, weeks=0)
# 返回months月之后得日期，months<0则计算之前日期，begin=True为月初日期，begin=False为月末日期
fmt_date = date_fmt.month_add(today, months=0, begin=True)
```

