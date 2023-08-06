from typing import Tuple

from datetime import date, timedelta
from pandas import DataFrame, Series

from BukePypiProjectVersion2.parameter import Universe, UnitPeriod


class Evaluator:

    @staticmethod
    def get_pnl(balance: Series) -> Series:
        """
        일별 잔고의 손익 계산
        :param balance: 일별 잔고
        :return: PNL (Profit and Loss)
        """
        pnl = balance.diff().fillna(0).apply(int)
        return pnl

    @staticmethod
    def get_return(balance: Series) -> Series:
        """
        일별 수익률 계산
        :param balance: 일별 잔고
        :return: Return (일별 수익률)
        """
        daily_return = balance.pct_change(periods=1).fillna(0)
        return daily_return

    def _get_index_day_price(self, universe: Universe, start_date, end_date):
        """
        비교 지수의 일봉 구하는 함수
        :param universe: 비교 지수
        :param start_date: 시작 날짜
        :param end_date: 끝 날짜
        :return: 비교 지수의 일봉
        """
        index_day_price = self.generator.get_index_day_price_data(universe, start_date, end_date)
        return index_day_price

    @staticmethod
    def get_winning_rate(daily_balance: DataFrame) -> Tuple[int, float]:
        """
        거래일과 승률을 구하는 함수
        :param daily_balance:
        :return:
        """
        winning = daily_balance.query("pnl > 0")
        losing = daily_balance.query("pnl < 0")

        winning_days = winning.pnl.count()
        losing_days = losing.pnl.count()

        trading_days = winning_days + losing_days
        winning_rate = winning_days / (winning_days + losing_days)
        return trading_days, winning_rate

    @staticmethod
    def get_profit_loss_rate(daily_balance: DataFrame) -> float:
        """
        손익비를 구하는 함수
        :param daily_balance:
        :return:
        """
        winning = daily_balance.query("pnl > 0")
        losing = daily_balance.query("pnl < 0")

        profit_loss_rate = winning.daily_return.mean() / losing.daily_return.abs().mean()
        return profit_loss_rate

    @staticmethod
    def get_cagr(previous_balance: Series, balance: Series) -> float:
        """
        누적 수익률을 구하는 함수
        :param previous_balance:
        :param balance:
        :return:
        """
        if len(previous_balance) > 0:
            cagr = (balance.iloc[-1] - previous_balance.iloc[-1]) / previous_balance.iloc[-1]
        else:
            cagr = (balance.iloc[-1] - balance.iloc[0]) / balance.iloc[0]
        return cagr

    @staticmethod
    def get_mdd(balance: Series) -> float:
        """
        MDD(Max Draw Down)을 구하는 함수
        :param balance:
        :return:
        """
        ath = balance.rolling(len(balance), min_periods=1).max()
        dd = balance - ath
        mdd = dd.rolling(len(dd), min_periods=1).min() / ath

        return mdd.min()

    def get_stat_of_unit_period(
        self, daily_balance: DataFrame, start_date, end_date
    ) -> dict:
        """
        단위 기간 동안의 통계를 구하는 함수
        :param daily_balance:
        :param index_day_price:
        :param start_date:
        :param end_date:
        :return:
        """
        query = "(date >= @start_date) and (date < @end_date)"
        sub_daily_balance = daily_balance.query(query)

        query = "date < @start_date"
        previous_sub_daily_balance = daily_balance.query(query)

        trading_days, winning_rate = self.get_winning_rate(sub_daily_balance)
        profit_loss_rate = self.get_profit_loss_rate(sub_daily_balance)
        cagr = self.get_cagr(previous_sub_daily_balance.balance, sub_daily_balance.balance)
        mdd = self.get_mdd(sub_daily_balance.balance)

        period_dict = {
            "trading_days": trading_days,
            "winning_rate": winning_rate,
            "profit_loss_rate": profit_loss_rate,
            "cagr": cagr,
            "mdd": mdd,
        }
        return period_dict

    def get_stat(
        self, daily_balance: DataFrame, unit_period: UnitPeriod = UnitPeriod.year
    ) -> DataFrame:
        """
        통계 결과를 반환하는 함수
        :param daily_balance:
        :param compared_index:
        :param unit_period:
        :return:
        """
        daily_balance["pnl"] = self.get_pnl(daily_balance.balance)
        daily_balance["daily_return"] = self.get_return(daily_balance.balance)

        start_date = daily_balance.date.iloc[0]
        end_date = daily_balance.date.iloc[-1]

        result = {}
        for year in range(start_date.year, end_date.year + 1):

            if unit_period == UnitPeriod.year:
                if year == start_date.year:
                    sub_start_date = start_date
                else:
                    sub_start_date = date(year, 1, 1)
                if year == end_date.year:
                    sub_end_date = end_date + timedelta(days=1)
                else:
                    sub_end_date = date(year + 1, 1, 1)

                year_dict = self.get_stat_of_unit_period(daily_balance, sub_start_date, sub_end_date)
                result[year] = year_dict

            else:
                start_month = 1
                last_month = 12
                if year == start_date.year:
                    start_month = start_date.month
                if year == end_date.year:
                    last_month = end_date.month

                for month in range(start_month, last_month + 1):

                    sub_start_date = date(year, month, 1)
                    if month == 12:
                        sub_end_date = date(year + 1, 1, 1)
                    else:
                        sub_end_date = date(year, month + 1, 1)

                    month_dict = self.get_stat_of_unit_period(
                        daily_balance, sub_start_date, sub_end_date
                    )
                    month = "%02d" % month
                    result[f"{year}-{month}"] = month_dict

        total_dict = self.get_stat_of_unit_period(
            daily_balance, start_date, end_date + timedelta(days=1)
        )
        result["total"] = total_dict

        result = DataFrame.from_dict(result, orient="index")
        result = result.round(decimals=4)

        return result
