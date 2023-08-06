"""
Date data formatting
"""

import pandas as pd
import datetime as dt


class DateFMT:
    """
    Some ways to format date
    """
    __slots__ = 'today', 'df_columns'

    def __new__(cls, date=None, date_df=None):
        self = object.__new__(cls)
        if date is not None:
            self.today = dt.datetime.strptime(str(date), "%Y-%m-%d")
        if date_df is not None:
            self.df_columns = date_df.columns
        return self

    @staticmethod
    def _fmt_ymd(date):
        return dt.datetime.strftime(date, "%Y-%m-%d")

    @classmethod
    def day_add(cls, date, days=0):
        """
        The increase or decrease of days
        :param date:
        :param days:
        :return:
        """
        return cls._fmt_ymd(cls(date).today + dt.timedelta(days=days))

    @classmethod
    def week_add(cls, date, what_day=0, weeks=0):
        """
        Choose a fixed day of the week
        :param date:
        :param what_day:
        :param weeks:
        :return:
        """
        return cls._fmt_ymd(
            cls(date).today - dt.timedelta(days=(dt.date.isoweekday(cls(date).today) - what_day - weeks * 7)))

    @classmethod
    def month_add(cls, date, months=0, begin=True):
        """
        Choose the beginning or end of a month
        :param date:
        :param months:
        :param begin:
        :return:
        """
        today = str(cls(date).today).split("-")
        if begin:
            date = dt.date(int(today[0]), int(today[1]) + months, 1)
        else:
            date = dt.date(int(today[0]), int(today[1]) + months + 1, 1) - dt.timedelta(days=1)
        return cls._fmt_ymd(date)

    @classmethod
    def column_fmt(cls, data_df: pd.DataFrame) -> pd.DataFrame:
        """
        Date data formatting -> Y-M-D
        The following formats are supported
        "2022年08月08日 19:19"
        "2022年08月08日"
        "2022-08-08 19:40"
        "2022-08-08 10:55:32"
        "08/8/2022"
        "08-08-22"
        "2022.8"
        "20220808"

        :param data_df:
        :return: df
        """
        import warnings
        for n in cls(date_df=data_df).df_columns:
            try:
                data_df[n] = [
                    str(pd.to_datetime(str(i).replace("年", "-").replace("月", "-").replace("日", "-"))).split(" ")[0] for
                    i in data_df.loc[:, n]]
            except Exception:
                warnings.warn(f"This data format is not currently supported: {n}", Warning, stacklevel=2, )

        return data_df
