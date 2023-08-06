"""
因子拥挤度
"""
import pandas as pd
import datetime
import os
import hbshare as hbs
import statsmodels.api as sm
from hbshare.fe.common.util.data_loader import get_trading_day_list
from hbshare.quant.Kevin.asset_allocation.macro_index.util import create_table, delete_duplicate_records, WriteToDB
from sqlalchemy import create_engine
from hbshare.quant.Kevin.rm_associated.config import engine_params, style_names, industry_names


class FactorCrowdCalculator:
    def __init__(self, trade_date, data_path, is_increment=1):
        self.trade_date = trade_date
        self.data_path = data_path
        self.is_increment = is_increment
        self._load_pre_date()

    def _load_pre_date(self):
        trade_dt = datetime.datetime.strptime(self.trade_date, '%Y%m%d')
        pre_date = (trade_dt - datetime.timedelta(days=200)).strftime('%Y%m%d')
        trading_day_list = get_trading_day_list(pre_date, self.trade_date)
        self.pre_date = trading_day_list[-60:][0]
        self.start_date = trading_day_list[-61:][0]

    def _calc_turnover_rate(self):
        # 换手率数据
        path = os.path.join(self.data_path, 'turnover_rate')
        listdir = os.listdir(path)
        listdir = [x for x in listdir if self.pre_date <= x.split('.')[0] <= self.trade_date]
        turnover_date = []
        for filename in listdir:
            date_t_rate = pd.read_json(os.path.join(path, '{}'.format(filename)),
                                       typ='series').to_frame('turnover_rate')
            date_t_rate.index.name = 'ticker'
            date_t_rate = date_t_rate.reset_index()
            date_t_rate['trade_date'] = filename.split('.')[0]

            turnover_date.append(date_t_rate)

        turnover_date = pd.concat(turnover_date, axis=0)
        turnover_date['ticker'] = turnover_date['ticker'].apply(lambda x: str(x).zfill(6))
        turnover_date = turnover_date[turnover_date['ticker'].str[0].isin(('0', '3', '6'))]

        turnover_df = pd.pivot_table(
            turnover_date, index='trade_date', columns='ticker', values='turnover_rate').sort_index()
        count_df = turnover_df.isnull().sum()
        included_list = count_df[count_df <= 20].index.tolist()
        turnover_df = turnover_df[included_list]

        return turnover_df.mean().to_frame('mean_to')

    def _calc_volatility(self):
        # 个股收益数据
        path = os.path.join(self.data_path, 'chg_pct')
        listdir = os.listdir(path)
        listdir = [x for x in listdir if self.pre_date <= x.split('.')[0] <= self.trade_date]
        chg_pct = []
        for filename in listdir:
            date_chg_pct = pd.read_csv(os.path.join(path, '{}'.format(filename)),
                                       dtype={'ticker': str, "tradeDate": str})
            chg_pct.append(date_chg_pct)
        chg_pct = pd.concat(chg_pct, axis=0)
        chg_pct.rename(columns={'dailyReturnReinv': 'chg_pct', 'tradeDate': 'trade_date'}, inplace=True)

        chg_pct.loc[chg_pct['chg_pct'] < -0.2, 'chg_pct'] = -0.2
        chg_pct.loc[chg_pct['chg_pct'] > 0.2, 'chg_pct'] = 0.2

        stock_return = pd.pivot_table(chg_pct, index='trade_date', columns='ticker', values='chg_pct').sort_index()
        count_df = stock_return.isnull().sum()
        included_list = count_df[count_df <= 20].index.tolist()
        stock_return = stock_return[included_list]

        return stock_return.std().to_frame('stock_vol'), stock_return

    def _calc_beta(self, stock_return):
        stock_return = stock_return.dropna(axis=1)
        # 指数收益-Wind全A
        sql_script = "SELECT JYRQ as TRADEDATE, ZQMC as INDEXNAME, SPJG as TCLOSE from funddb.ZSJY WHERE ZQDM = '{}' " \
                     "and JYRQ >= {} and JYRQ <= {}".format('801813', self.start_date, self.trade_date)
        data = pd.DataFrame(hbs.db_data_query('readonly', sql_script)['data'])
        index_return = data.set_index('TRADEDATE')['TCLOSE'].pct_change().dropna().reindex(stock_return.index)

        reg_x = sm.add_constant(index_return)

        beta_series = stock_return.apply(lambda y: sm.OLS(y, reg_x).fit().params[1], axis=0)

        return beta_series.to_frame('beta')

    def daily_calc(self):
        mean_to = self._calc_turnover_rate()
        stock_vol, stock_return = self._calc_volatility()
        beta = self._calc_beta(stock_return)

        result_df = mean_to.merge(stock_vol, left_index=True, right_index=True).merge(
            beta, left_index=True, right_index=True).reset_index()
        result_df['trade_date'] = self.trade_date

        return result_df

    def get_construct_result(self):
        if self.is_increment == 1:
            data = self.daily_calc()
            sql_script = "delete from factor_crowd where trade_date in ({})".format(
                ','.join(data['trade_date'].tolist()))
            # delete first
            delete_duplicate_records(sql_script)
            # add new records
            WriteToDB().write_to_db(data, 'factor_crowd')
        else:
            sql_script = """
                create table factor_crowd(
                id int auto_increment primary key,
                trade_date date not null,
                ticker varchar(20),
                mean_to decimal(6, 4),
                stock_vol decimal(6, 4),
                beta decimal(6,4 )) 
            """
            create_table('factor_crowd', sql_script)
            data = self.daily_calc()
            WriteToDB().write_to_db(data, 'factor_crowd')


def get_style_factor(trade_date, factor_name):
    sql_script = "SELECT * FROM st_ashare.r_st_barra_style_factor where TRADE_DATE = '{}'".format(trade_date)
    res = hbs.db_data_query('alluser', sql_script, page_size=5000)
    style_factor = pd.DataFrame(res['data']).set_index('ticker')[factor_name]

    return style_factor


def get_style_factor_local(trade_date, factor_name):
    factor_path = r'D:\kevin\risk_model_jy\RiskModel\data'
    factor_path = os.path.join(factor_path, r'zzqz_sw\style_factor')
    style_factor = pd.read_csv(
        os.path.join(factor_path, '{0}.csv'.format(trade_date)), dtype={"ticker": str}).set_index('ticker')[factor_name]

    return style_factor


class FactorCrowdTest:
    def __init__(self, trade_date, factor_series):
        self.trade_date = trade_date
        self.factor_series = factor_series

    def run(self):
        sql_script = "SELECT * FROM factor_crowd where trade_date = '{}'".format(self.trade_date)
        engine = create_engine(engine_params)
        data = pd.read_sql(sql_script, engine)
        data['trade_date'] = data['trade_date'].apply(lambda x: datetime.datetime.strftime(x, '%Y%m%d'))
        crowd_df = data.set_index('ticker')[['mean_to', 'stock_vol', 'beta']]
        df = pd.merge(crowd_df, self.factor_series.to_frame('factor'), left_index=True, right_index=True)
        crowd_list = ['mean_to', 'stock_vol', 'beta']

        short_ratio = df[df['factor'] <= df['factor'].quantile(0.1)][crowd_list].mean()
        long_ratio = df[df['factor'] >= df['factor'].quantile(0.9)][crowd_list].mean()
        ratio = long_ratio / short_ratio

        return ratio.to_frame(self.trade_date)


if __name__ == '__main__':
    import time

    start_time = time.time()
    FactorCrowdCalculator('20181019', r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()
    end_time = time.time()
    print('程序用时：%s秒' % (end_time - start_time))

    # start_date = '20181019'
    # end_date = '20220819'
    # from tqdm import tqdm
    # date_list = get_trading_day_list(start_date, end_date, frequency="week")
    # for date in tqdm(date_list):
    #     FactorCrowdCalculator(date, r'D:\kevin\risk_model_jy\RiskModel\data\common_data').get_construct_result()

    # start_date = '20101010'
    # end_date = '20220819'
    # date_list = get_trading_day_list(start_date, end_date, frequency="week")
    # date_list = [x for x in date_list if x != '20150904']
    # from tqdm import tqdm
    # ratio_list = []
    # for date in tqdm(date_list):
    #     factor = get_style_factor_local(date, 'size')
    #     t_ratio = FactorCrowdTest(date, factor).run()
    #     ratio_list.append(t_ratio)
    #
    # ratio_df = pd.concat(ratio_list, axis=1)
    #
    # ratio_df.to_csv('D:\\123.csv')
