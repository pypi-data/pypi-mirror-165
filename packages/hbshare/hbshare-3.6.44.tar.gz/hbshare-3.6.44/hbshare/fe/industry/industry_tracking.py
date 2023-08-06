# -*- coding: utf-8 -*-

from hbshare.fe.xwq.analysis.orm.hbdb import HBDB
from hbshare.fe.xwq.analysis.utils.const_var import TimeDateFormat
from hbshare.fe.xwq.analysis.utils.timedelta_utils import TimeDateUtil
import os
import numpy as np
import pandas as pd

from WindPy import w
w.start()  # 默认命令超时时间为120秒，如需设置超时时间可以加入waitTime参数，例如waitTime=60,即设置命令超时时间为60秒
w.isconnected()  # 判断WindPy是否已经登录成功

from matplotlib.ticker import FuncFormatter
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style('white', {'font.sans-serif': ['simhei', 'Arial']})
line_color_list = ['#F04950', '#6268A2', '#959595', '#333335', '#EE703F', '#7E4A9B', '#8A662C',
                   '#44488E', '#BA67E9', '#3FAEEE']
bar_color_list = ['#C94649', '#EEB2B4', '#E1777A', '#D57C56', '#E39A79', '#DB8A66', '#E5B88C',
                  '#8588B7', '#B4B6D1', '#55598D', '#628497', '#A9C6CB', '#866EA9', '#B79BC7',
                  '#7D7D7E', '#CACACA', '#A7A7A8', '#606063', '#C4C4C4', '#99999B', '#B7B7B7']


def from_rgb_to_color16(rgb):
    color = '#'
    for i in rgb:
        num = int(i)
        color += str(hex(num))[-2:].replace('x', '0').upper()
    return color


def to_100percent(temp, position):
    return '%0.01f'%(temp * 100) + '%'


def to_percent(temp, position):
    return '%0.01f'%(temp) + '%'


def filter_extreme_mad(ser, n=3):
    median = ser.quantile(0.5)
    new_median = ((ser - median).abs()).quantile(0.5)
    max_range = median + n * new_median
    min_range = median - n * new_median
    ser = np.clip(ser, min_range, max_range)
    return ser


def get_date(start_date, end_date):
    calendar_df = HBDB().read_cal(start_date, end_date)
    calendar_df = calendar_df.rename(columns={'JYRQ': 'CALENDAR_DATE', 'SFJJ': 'IS_OPEN', 'SFZM': 'IS_WEEK_END', 'SFYM': 'IS_MONTH_END'})
    calendar_df['CALENDAR_DATE'] = calendar_df['CALENDAR_DATE'].astype(str)
    calendar_df = calendar_df.sort_values('CALENDAR_DATE')
    calendar_df['IS_OPEN'] = calendar_df['IS_OPEN'].astype(int).replace({0: 1, 1: 0})
    calendar_df['YEAR'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:4])
    calendar_df['YEAR_MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[:6])
    calendar_df['MONTH'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:6])
    calendar_df['MONTH_DAY'] = calendar_df['CALENDAR_DATE'].apply(lambda x: x[4:])
    calendar_df = calendar_df[(calendar_df['CALENDAR_DATE'] >= start_date) & (calendar_df['CALENDAR_DATE'] <= end_date)]
    trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    trade_df = trade_df[(trade_df['TRADE_DATE'] >= start_date) & (trade_df['TRADE_DATE'] <= end_date)]
    report_df = calendar_df.drop_duplicates('YEAR_MONTH', keep='last').rename(columns={'CALENDAR_DATE': 'REPORT_DATE'})
    report_df = report_df[report_df['MONTH_DAY'].isin(['0331', '0630', '0930', '1231'])]
    report_df = report_df[(report_df['REPORT_DATE'] >= start_date) & (report_df['REPORT_DATE'] <= end_date)]
    report_trade_df = calendar_df[calendar_df['IS_OPEN'] == 1].rename(columns={'CALENDAR_DATE': 'TRADE_DATE'})
    report_trade_df = report_trade_df.sort_values('TRADE_DATE').drop_duplicates('YEAR_MONTH', keep='last')
    report_trade_df = report_trade_df[report_trade_df['MONTH'].isin(['03', '06', '09', '12'])]
    report_trade_df = report_trade_df[(report_trade_df['TRADE_DATE'] >= start_date) & (report_trade_df['TRADE_DATE'] <= end_date)]
    calendar_trade_df = calendar_df[['CALENDAR_DATE']].merge(trade_df[['TRADE_DATE']], left_on=['CALENDAR_DATE'], right_on=['TRADE_DATE'], how='left')
    calendar_trade_df['TRADE_DATE'] = calendar_trade_df['TRADE_DATE'].fillna(method='ffill')
    calendar_trade_df = calendar_trade_df[(calendar_trade_df['TRADE_DATE'] >= start_date) & (calendar_trade_df['TRADE_DATE'] <= end_date)]
    return calendar_df, report_df, trade_df, report_trade_df, calendar_trade_df


class PeTracking:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = TimeDateUtil.convert_format(self.start_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.end_date_hyphen = TimeDateUtil.convert_format(self.end_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.data_path = data_path
        self.stocks = pd.read_excel('{0}stocks.xlsx'.format(self.data_path))
        self.stocks['TICKER_SYMBOL'] = self.stocks['代码'].apply(lambda x: str(x).split('.')[0])
        self.indexs = pd.read_excel('{0}indexs.xlsx'.format(self.data_path))
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        if os.path.isfile('{0}stock_valuation.hdf'.format(self.data_path)):
            existed_stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), self.start_date)
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = self.start_date
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_valuation_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            stock_valuation_date = stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            star_stock_valuation_date = star_stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(star_stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            stock_valuation_list.append(stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat([existed_stock_valuation] + stock_valuation_list, ignore_index=True)
        self.stock_valuation = self.stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_valuation = self.stock_valuation.reset_index().drop('index', axis=1)
        self.stock_valuation.to_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')

        if os.path.isfile('{0}index_valuation.hdf'.format(self.data_path)):
            existed_index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_index_valuation['TRADE_DATE'])
            start_date_hyphen = max(str(max_date), self.start_date_hyphen)
        else:
            existed_index_valuation = pd.DataFrame()
            start_date_hyphen = self.start_date_hyphen
        index_valuation_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_valuation_index = w.wsd(index, "pe_ttm", start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_valuation_index.columns = ['TRADE_DATE', 'PE_TTM']
            index_valuation_index['INDEX_SYMBOL'] = index
            index_valuation_list.append(index_valuation_index)
            print(index)
        self.index_valuation = pd.concat([existed_index_valuation] + index_valuation_list, ignore_index=True)
        self.index_valuation = self.index_valuation.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_valuation = self.index_valuation.reset_index().drop('index', axis=1)
        self.index_valuation.to_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')
        return

    def get_stocks_forwardpehr(self):
        latest_stock_valuation = self.stock_valuation[self.stock_valuation['TRADE_DATE'] == self.end_date]
        stocks_forwardpehr = self.stocks.merge(latest_stock_valuation[['TICKER_SYMBOL', 'FORWARD_PEHR']], on=['TICKER_SYMBOL'], how='left')
        stocks_forwardpehr = stocks_forwardpehr.drop('TICKER_SYMBOL', axis=1)
        stocks_forwardpehr.to_excel('{0}stocks_forwardpehr_{1}.xlsx'.format(self.data_path, self.end_date))
        return

    def get_stocks_pe_quantile(self):
        stock_valuation = self.stock_valuation[self.stock_valuation['TICKER_SYMBOL'].isin(self.stocks['TICKER_SYMBOL'].unique().tolist())]
        stock_valuation = stock_valuation.pivot(index='TRADE_DATE', columns='TICKER_SYMBOL', values='PE_TTM')
        stock_valuation = stock_valuation.sort_index()
        stocks_pe_quantile = pd.DataFrame(stock_valuation.apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0))
        stocks_pe_quantile = stocks_pe_quantile.reset_index()
        stocks_pe_quantile.columns = ['TICKER_SYMBOL', 'PE_QUANTILE']
        stocks_pe_quantile = self.stocks.merge(stocks_pe_quantile, on=['TICKER_SYMBOL'], how='left')
        stocks_pe_quantile = stocks_pe_quantile.drop('TICKER_SYMBOL', axis=1)
        stocks_pe_quantile.to_excel('{0}stocks_pe_quantile_{1}.xlsx'.format(self.data_path, self.end_date))
        return

    def get_indexs_pe_quantile(self):
        index_valuation = self.index_valuation[self.index_valuation['INDEX_SYMBOL'].isin(self.indexs['代码'].unique().tolist())]
        index_valuation = index_valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE_TTM')
        index_valuation = index_valuation.sort_index()
        indexs_pe_quantile = pd.DataFrame(index_valuation.apply(lambda x: (1.0 - np.count_nonzero(x.iloc[-1] <= x) / x.size) * 100.0))
        indexs_pe_quantile = indexs_pe_quantile.reset_index()
        indexs_pe_quantile.columns = ['代码', 'PE_QUANTILE']
        indexs_pe_quantile = self.indexs.merge(indexs_pe_quantile, on=['代码'], how='left')
        indexs_pe_quantile.to_excel('{0}indexs_pe_quantile_{1}.xlsx'.format(self.data_path, self.end_date))

        for sector in self.indexs['板块'].unique().tolist():
            sector_indexs = self.indexs[self.indexs['板块'] == sector]['代码'].unique().tolist()
            index_name_list = self.indexs[self.indexs['板块'] == sector]['名称'].unique().tolist()
            index_pe_list = [filter_extreme_mad(index_valuation[index].dropna()) for index in sector_indexs]
            ind_pe_latest = index_valuation[sector_indexs].iloc[-1]
            plt.figure(figsize=(12, 6))
            plt.boxplot(index_pe_list, labels=index_name_list, vert=True, widths=0.25, flierprops={'marker': 'o', 'markersize': 1}, meanline=True, showmeans=True, showfliers=False)
            plt.scatter(range(1, len(ind_pe_latest) + 1), ind_pe_latest.values, marker='o')
            plt.xticks(rotation=45)
            plt.title(sector)
            plt.tight_layout()
            plt.savefig('{0}indexs_pe_quantile_{1}_{2}.png'.format(self.data_path, sector, self.end_date))
        return

    def get_amt_results(self):
        self.get_stocks_forwardpehr()
        self.get_stocks_pe_quantile()
        self.get_indexs_pe_quantile()


class IndustryTracking:
    def __init__(self, start_date, end_date, data_path):
        self.start_date = start_date
        self.end_date = end_date
        self.start_date_hyphen = TimeDateUtil.convert_format(self.start_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.end_date_hyphen = TimeDateUtil.convert_format(self.end_date, TimeDateFormat.YMD.value, TimeDateFormat.YMDHYPHEN.value)
        self.data_path = data_path
        self.stocks = pd.read_excel('{0}stocks.xlsx'.format(self.data_path))
        self.stocks['TICKER_SYMBOL'] = self.stocks['代码'].apply(lambda x: str(x).split('.')[0])
        self.indexs = pd.read_excel('{0}indexs_factor_ori.xlsx'.format(self.data_path))
        self.indexs = self.indexs[self.indexs['是否展示'] == 1]
        self.load()

    def load(self):
        self.calendar_df, self.report_df, self.trade_df, self.report_trade_df, self.calendar_trade_df = get_date(self.start_date, self.end_date)

        if os.path.isfile('{0}stock_valuation.hdf'.format(self.data_path)):
            existed_stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_stock_valuation['TRADE_DATE'])
            start_date = max(str(max_date), self.start_date)
        else:
            existed_stock_valuation = pd.DataFrame()
            start_date = self.start_date
        trade_df = self.trade_df[(self.trade_df['TRADE_DATE'] > start_date) & (self.trade_df['TRADE_DATE'] <= self.end_date)]
        stock_valuation_list = []
        for date in trade_df['TRADE_DATE'].unique().tolist():
            stock_valuation_date = HBDB().read_stock_valuation_given_date(date)
            stock_valuation_date = stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            star_stock_valuation_date = HBDB().read_star_stock_valuation_given_date(date)
            star_stock_valuation_date = star_stock_valuation_date[['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR']] if len(star_stock_valuation_date) > 0 else pd.DataFrame(columns=['TRADE_DATE', 'TICKER_SYMBOL', 'SEC_SHORT_NAME', 'MARKET_VALUE', 'PE_TTM', 'PB_LF', 'PEG', 'DIVIDEND_RATIO_TTM', 'FORWARD_PEHR'])
            stock_valuation_date = pd.concat([stock_valuation_date, star_stock_valuation_date])
            stock_valuation_list.append(stock_valuation_date)
            print(date)
        self.stock_valuation = pd.concat([existed_stock_valuation] + stock_valuation_list, ignore_index=True)
        self.stock_valuation = self.stock_valuation.sort_values(['TRADE_DATE', 'TICKER_SYMBOL'])
        self.stock_valuation = self.stock_valuation.reset_index().drop('index', axis=1)
        self.stock_valuation.to_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.stock_valuation = pd.read_hdf('{0}stock_valuation.hdf'.format(self.data_path), key='table')

        if os.path.isfile('{0}index_valuation.hdf'.format(self.data_path)):
            existed_index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')
            max_date = max(existed_index_valuation['TRADE_DATE'])
            start_date_hyphen = max(str(max_date), self.start_date_hyphen)
        else:
            existed_index_valuation = pd.DataFrame()
            start_date_hyphen = self.start_date_hyphen
        index_valuation_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_valuation_index = w.wsd(index, "pe_ttm", start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_valuation_index.columns = ['TRADE_DATE', 'PE_TTM']
            index_valuation_index['INDEX_SYMBOL'] = index
            index_valuation_list.append(index_valuation_index)
            print(index)
        self.index_valuation = pd.concat([existed_index_valuation] + index_valuation_list, ignore_index=True)
        self.index_valuation = self.index_valuation.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_valuation = self.index_valuation.reset_index().drop('index', axis=1)
        self.index_valuation.to_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table', mode='w')
        self.index_valuation = pd.read_hdf('{0}index_valuation.hdf'.format(self.data_path), key='table')

        if os.path.isfile('{0}index_daily_k.hdf'.format(self.data_path)):
            existed_index_daily_K = pd.read_hdf('{0}index_daily_k.hdf'.format(self.data_path), key='table')
            max_date = max(existed_index_daily_K['TRADE_DATE'])
            start_date_hyphen = max(str(max_date), self.start_date_hyphen)
        else:
            existed_index_daily_K = pd.DataFrame()
            start_date_hyphen = self.start_date_hyphen
        index_daily_k_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_daily_k_index = w.wsd(index, "close", start_date_hyphen, self.end_date_hyphen, "Fill=Previous;PriceAdj=F", usedf=True)[1].reset_index()
            index_daily_k_index.columns = ['TRADE_DATE', 'CLOSE_INDEX']
            index_daily_k_index['INDEX_SYMBOL'] = index
            index_daily_k_list.append(index_daily_k_index)
            print(index)
        self.index_daily_k = pd.concat([existed_index_daily_K] + index_daily_k_list, ignore_index=True)
        self.index_daily_k = self.index_daily_k.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        self.index_daily_k = self.index_daily_k.reset_index().drop('index', axis=1)
        self.index_daily_k.to_hdf('{0}index_daily_k.hdf'.format(self.data_path), key='table', mode='w')
        self.index_daily_k = pd.read_hdf('{0}index_daily_k.hdf'.format(self.data_path), key='table')

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_finance_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_finance_index = w.wsd(index, "oper_rev,or_ttm2,yoy_or,qfa_yoysales,qfa_cgrsales,np_belongto_parcomsh,profit_ttm2,yoynetprofit,qfa_yoynetprofit,qfa_cgrnetprofit,roe_avg,qfa_roe,yoyroe,roa,qfa_roa,grossprofitmargin,qfa_grossprofitmargin,netprofitmargin,qfa_netprofitmargin,eps_basic,bps", start_date_hyphen, self.end_date_hyphen, "unit=1;rptType=1;Period=Q;Days=Alldays", usedf=True)[1].reset_index()
            index_finance_index.columns = ['REPORT_DATE', 'MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']
            index_finance_index['INDEX_SYMBOL'] = index
            index_finance_list.append(index_finance_index)
            print(index)
        self.index_finance = pd.concat(index_finance_list, ignore_index=True)
        self.index_finance = self.index_finance.sort_values(['REPORT_DATE', 'INDEX_SYMBOL']).drop_duplicates(['REPORT_DATE', 'INDEX_SYMBOL'])
        self.index_finance = self.index_finance.reset_index().drop('index', axis=1)
        self.index_finance.to_hdf('{0}index_finance.hdf'.format(self.data_path), key='table', mode='w')
        self.index_finance = pd.read_hdf('{0}index_finance.hdf'.format(self.data_path), key='table')

        start_date_hyphen = str(int(self.start_date_hyphen[:4]) - 1) + self.start_date_hyphen[4:]
        index_consensus_list = []
        for index in self.indexs['代码'].unique().tolist():
            index_consensus_index = w.wsd(index, "west_sales_FY1,west_sales_YOY,west_sales_CAGR,west_netprofit_FY1,west_netprofit_YOY,west_netprofit_CAGR,west_nproc_1w,west_nproc_4w,west_nproc_13w,west_nproc_26w,west_avgroe_FY1,west_avgroe_YOY,west_eps_FY1,west_avgbps_FY1", start_date_hyphen, self.end_date_hyphen, "unit=1;year=2022;Period=Q;Days=Alldays", usedf=True)[1].reset_index()
            index_consensus_index.columns = ['REPORT_DATE', 'CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
            index_consensus_index['INDEX_SYMBOL'] = index
            index_consensus_list.append(index_consensus_index)
            print(index)
        self.index_consensus = pd.concat(index_consensus_list, ignore_index=True)
        self.index_consensus = self.index_consensus.sort_values(['REPORT_DATE', 'INDEX_SYMBOL']).drop_duplicates(['REPORT_DATE', 'INDEX_SYMBOL'])
        self.index_consensus = self.index_consensus.reset_index().drop('index', axis=1)
        self.index_consensus.to_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table', mode='w')
        self.index_consensus = pd.read_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table')

        # if os.path.isfile('{0}index_consensus.hdf'.format(self.data_path)):
        #     existed_index_consensus = pd.read_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table')
        #     max_date = max(existed_index_consensus['TRADE_DATE'])
        #     start_date_hyphen = max(str(max_date), self.start_date_hyphen)
        # else:
        #     existed_index_consensus = pd.DataFrame()
        #     start_date_hyphen = self.start_date_hyphen
        # index_consensus_list = []
        # for index in self.indexs['代码'].unique().tolist()[:3]:
        #     index_consensus_index = w.wsd(index, "west_sales_FY1,west_sales_YOY,west_sales_CAGR,west_netprofit_FY1,west_netprofit_YOY,west_netprofit_CAGR,west_nproc_1w,west_nproc_4w,west_nproc_13w,west_nproc_26w,west_avgroe_FY1,west_avgroe_YOY,west_eps_FY1,west_avgbps_FY1", start_date_hyphen, self.end_date_hyphen, "unit=1;year=2022;Days=Alldays;Fill=Previous", usedf=True)[1].reset_index()
        #     index_consensus_index.columns = ['TRADE_DATE', 'CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
        #     index_consensus_index['INDEX_SYMBOL'] = index
        #     index_consensus_list.append(index_consensus_index)
        #     print(index)
        # self.index_consensus = pd.concat([existed_index_consensus] + index_consensus_list, ignore_index=True)
        # self.index_consensus = self.index_consensus.sort_values(['TRADE_DATE', 'INDEX_SYMBOL']).drop_duplicates(['TRADE_DATE', 'INDEX_SYMBOL'])
        # self.index_consensus = self.index_consensus.reset_index().drop('index', axis=1)
        # self.index_consensus.to_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table', mode='w')
        # self.index_consensus = pd.read_hdf('{0}index_consensus.hdf'.format(self.data_path), key='table')
        return

    def get_amt_ret(self):
        index_daily_k = self.index_daily_k.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='CLOSE_INDEX')
        index_daily_k.index = map(lambda x: str(x).replace('-', ''), index_daily_k.index)
        index_daily_k = index_daily_k.sort_index()

        # 周收益情况
        last_date = self.trade_df[(self.trade_df['IS_WEEK_END'] == '1') & (self.trade_df['TRADE_DATE'] <= self.end_date)]['TRADE_DATE'].iloc[-2]
        index_daily_k_w = index_daily_k[(index_daily_k.index >= last_date) & (index_daily_k.index <= self.end_date)]
        index_daily_k_wret = index_daily_k_w.iloc[-1] / index_daily_k_w.iloc[0] - 1
        index_daily_k_wret = index_daily_k_wret.reset_index()
        index_daily_k_wret.columns = ['代码', '周收益']
        indexs_wret = self.indexs.merge(index_daily_k_wret, on=['代码'], how='left')
        sector_list = self.indexs['板块'].unique().tolist()
        sector_color_list = ([bar_color_list[0], bar_color_list[7]] * len(sector_list))[:len(sector_list)]
        sector_color_dict = {sector: sector_color_list[i] for i, sector in enumerate(sector_list)}
        indexs_wret['颜色'] = indexs_wret['板块'].apply(lambda x: sector_color_dict[x])
        indexs_wret['索引'] = range(len(indexs_wret))
        # 周收益柱状图
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.barplot(x='索引', y='周收益', data=indexs_wret, palette=indexs_wret['颜色'].tolist())
        ax.set_xticklabels(labels=indexs_wret['展示名称'].tolist(), rotation=90)
        ax.yaxis.set_major_formatter(FuncFormatter(to_100percent))
        plt.xlabel('')
        plt.ylabel('周收益')
        plt.tight_layout()
        plt.savefig('{0}wret_{1}.png'.format(self.data_path, self.end_date))

        # 先进制造情况
        amt_indexs_names_dic = self.indexs[self.indexs['板块'] == '先进制造'].set_index('代码')['展示名称'].to_dict()
        amt_indexs = self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()
        amt_index_daily_k = index_daily_k[amt_indexs]
        amt_index_daily_k = amt_index_daily_k / amt_index_daily_k.iloc[0]
        amt_index_daily_k.columns = [amt_indexs_names_dic[col] for col in list(amt_index_daily_k.columns)]
        amt_index_daily_k = amt_index_daily_k.reset_index().rename(columns={'index': 'TRADE_DATE'})
        amt_index_daily_k['TRADE_DATE'] = amt_index_daily_k['TRADE_DATE'].apply(lambda x: TimeDateUtil.convert_str_to_date(x, '%Y%m%d'))
        # 指数走势线型图
        plt.figure(figsize=(12, 6))
        for i, index_name in enumerate(list(amt_index_daily_k.columns)[1:]):
            sns.lineplot(x='TRADE_DATE', y=index_name, data=amt_index_daily_k, label=index_name, color=line_color_list[i])
        plt.xlabel('')
        plt.ylabel('')
        plt.legend(loc=2)
        plt.tight_layout()
        plt.savefig('{0}close_{1}.png'.format(self.data_path, self.end_date))
        return

    def get_amt_valuation(self):
        index_valuation = self.index_valuation.pivot(index='TRADE_DATE', columns='INDEX_SYMBOL', values='PE_TTM')
        index_valuation.index = map(lambda x: str(x).replace('-', ''), index_valuation.index)
        index_valuation = index_valuation.sort_index()

        # 估值分布情况
        indexs_info = self.indexs.copy(deep=True)
        index_id_list = indexs_info['代码'].tolist()[::-1]
        index_name_list = indexs_info['展示名称'].tolist()[::-1]
        index_valuation_list = [filter_extreme_mad(index_valuation[index].dropna()) for index in index_id_list]
        index_valuation_latest = index_valuation[index_id_list].iloc[-1]
        sector_list = indexs_info['板块'].unique().tolist()
        sector_color_list = ([bar_color_list[0], bar_color_list[7]] * len(sector_list))[:len(sector_list)]
        sector_color_dict = {sector: sector_color_list[i] for i, sector in enumerate(sector_list)}
        indexs_info['颜色'] = indexs_info['板块'].apply(lambda x: sector_color_dict[x])
        # 估值分布箱型图
        plt.figure(figsize=(12, 18))
        f = plt.boxplot(index_valuation_list, labels=index_name_list, vert=False, meanline=True, showmeans=True, showfliers=False, patch_artist=True, zorder=1)
        for box, c in zip(f['boxes'], indexs_info['颜色'].tolist()[::-1]):
            box.set(color=c)
        plt.scatter(index_valuation_latest.values, range(1, len(index_valuation_latest) + 1), marker='o', zorder=2)
        plt.xlabel('PE_TTM')
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig('{0}valuation_{1}.png'.format(self.data_path, self.end_date))
        return

    def get_amt_prosperity(self):
        indexs = self.indexs.copy(deep=True)
        indexs_names_dic = indexs.set_index('代码')['展示名称'].to_dict()
        index_finance = self.index_finance.copy(deep=True)
        index_finance['REPORT_DATE'] = index_finance['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_finance = index_finance[index_finance['REPORT_DATE'] >= '20190101']
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))

        # 测试指标有效性
        factor_list = ['MAIN_INCOME', 'MAIN_INCOME_TTM', 'MAIN_INCOME_YOY', 'MAIN_INCOME_Q_YOY', 'MAIN_INCOME_Q_MOM', 'NET_PROFIT', 'PROFIT_TTM', 'NET_PROFIT_YOY', 'NET_PROFIT_Q_YOY', 'NET_PROFIT_Q_MOM', 'ROE', 'ROE_Q', 'ROE_YOY', 'ROA', 'ROA_Q', 'GROSS_PROFIT_MARGIN', 'GROSS_PROFIT_MARGIN_Q', 'NET_PROFIT_MARGIN', 'NET_PROFIT_MARGIN_Q', 'EPS_BASIC', 'BPS']
        factor_name_list = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS']
        factor_name_dict = {factor_list[i]: factor_name_list[i] for i in range(len(factor_list))}
        corr_df = pd.DataFrame(index=self.indexs['代码'].unique().tolist(), columns=factor_list)
        for factor in factor_list:
            for index in self.indexs['代码'].unique().tolist():
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
                index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
                max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
                index_finance_index = index_finance_index[index_finance_index['REPORT_DATE'] <= max_report_date]
                index_finance_index = index_finance_index[['REPORT_DATE', 'INDEX_SYMBOL', factor]]
                index_finance_index = index_finance_index.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                index_finance_index = index_finance_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
                # index_finance_index['CLOSE_INDEX'] = index_finance_index['CLOSE_INDEX'].pct_change().shift(-1)
                index_finance_index = index_finance_index.dropna().drop('TRADE_DATE', axis=1).sort_values('REPORT_DATE')
                if len(index_finance_index) == 0:
                    continue
                corr = round(np.corrcoef(index_finance_index[factor], index_finance_index['CLOSE_INDEX'])[0, 1], 2)
                corr_df.loc[index, factor] = corr

                # fig, ax1 = plt.subplots(figsize=(6, 3))
                # ax2 = ax1.twinx()
                # sns.lineplot(ax=ax1, x='REPORT_DATE', y=factor, data=index_finance_index, color=line_color_list[0])
                # sns.lineplot(ax=ax2, x='REPORT_DATE', y='CLOSE_INDEX', data=index_finance_index, color=line_color_list[1])
                # ax1.set_xlabel('')
                # ax2.set_xlabel('')
                # ax1.set_ylabel(factor_name_dict[factor])
                # ax2.set_ylabel(indexs_names_dic[index])
                # ax1.set_xticklabels(labels=index_finance_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # ax2.set_xticklabels(labels=index_finance_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # plt.title('两者相关系数为{2}%'.format(factor_name_dict[factor], indexs_names_dic[index], corr))
                # plt.tight_layout()
                # plt.savefig('{0}corr/{1}_{2}_{3}.png'.format(self.data_path, factor_name_dict[factor], indexs_names_dic[index], self.end_date))

        corr_df = corr_df.reset_index()
        corr_df.columns = ['代码'] + [factor_name_dict[col] for col in list(corr_df.columns)[1:]]
        indexs_corr = self.indexs.merge(corr_df, on=['代码'], how='left')
        indexs_corr.to_excel('{0}factor_close_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        # indexs_corr.to_excel('{0}factor_ret_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        # indexs_corr.to_excel('{0}factor_forward_ret_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        return

    def get_amt_con_prosperity(self):
        indexs = self.indexs.copy(deep=True)
        indexs_names_dic = indexs.set_index('代码')['展示名称'].to_dict()
        index_consensus = self.index_consensus.copy(deep=True)
        index_consensus['REPORT_DATE'] = index_consensus['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_consensus = index_consensus[index_consensus['REPORT_DATE'] >= '20190101']
        index_finance = self.index_finance.copy(deep=True)
        index_finance['REPORT_DATE'] = index_finance['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_finance = index_finance[index_finance['REPORT_DATE'] >= '20190101']
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))

        # 测试指标有效性
        factor_list = ['CON_MAIN_INCOME_FY1', 'CON_MAIN_INCOME_YOY', 'CON_MAIN_INCOME_CAGR', 'CON_NET_PROFIT_FY1', 'CON_NET_PROFIT_YOY', 'CON_NET_PROFIT_CAGR', 'CON_NET_PROFIT_1W', 'CON_NET_PROFIT_4W', 'CON_NET_PROFIT_13W', 'CON_NET_PROFIT_26W', 'CON_ROE_FY1', 'CON_ROE_YOY', 'CON_EPS_FY1', 'CON_BPS_FY1']
        factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
        factor_name_dict = {factor_list[i]: factor_name_list[i] for i in range(len(factor_list))}
        corr_df = pd.DataFrame(index=self.indexs['代码'].unique().tolist(), columns=factor_list)
        for factor in factor_list:
            for index in self.indexs['代码'].unique().tolist():
                index_daily_k_index = index_daily_k[index_daily_k['INDEX_SYMBOL'] == index]
                index_consensus_index = index_consensus[index_consensus['INDEX_SYMBOL'] == index]
                index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
                max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
                index_consensus_index = index_consensus_index[index_consensus_index['REPORT_DATE'] <= max_report_date]
                index_consensus_index = index_consensus_index[['REPORT_DATE', 'INDEX_SYMBOL', factor]]
                index_consensus_index = index_consensus_index.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
                index_consensus_index = index_consensus_index.merge(index_daily_k_index, on=['INDEX_SYMBOL', 'TRADE_DATE'], how='left')
                # index_consensus_index['CLOSE_INDEX'] = index_consensus_index['CLOSE_INDEX'].pct_change().shift(-1)
                index_consensus_index = index_consensus_index.dropna().drop('TRADE_DATE', axis=1).sort_values('REPORT_DATE')
                if len(index_consensus_index) == 0:
                    continue
                corr = round(np.corrcoef(index_consensus_index[factor], index_consensus_index['CLOSE_INDEX'])[0, 1], 2)
                corr_df.loc[index, factor] = corr

                # fig, ax1 = plt.subplots(figsize=(6, 3))
                # ax2 = ax1.twinx()
                # sns.lineplot(ax=ax1, x='REPORT_DATE', y=factor, data=index_consensus_index, color=line_color_list[0])
                # sns.lineplot(ax=ax2, x='REPORT_DATE', y='CLOSE_INDEX', data=index_consensus_index, color=line_color_list[1])
                # ax1.set_xlabel('')
                # ax2.set_xlabel('')
                # ax1.set_ylabel(factor_name_dict[factor])
                # ax2.set_ylabel(indexs_names_dic[index])
                # ax1.set_xticklabels(labels=index_consensus_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # ax2.set_xticklabels(labels=index_consensus_index['REPORT_DATE'].unique().tolist(), rotation=90)
                # plt.title('两者相关系数为{2}%'.format(factor_name_dict[factor], indexs_names_dic[index], corr))
                # plt.tight_layout()
                # plt.savefig('{0}con_corr/{1}_{2}_{3}.png'.format(self.data_path, factor_name_dict[factor], indexs_names_dic[index], self.end_date))

        corr_df = corr_df.reset_index()
        corr_df.columns = ['代码'] + [factor_name_dict[col] for col in list(corr_df.columns)[1:]]
        indexs_corr = self.indexs.merge(corr_df, on=['代码'], how='left')
        indexs_corr.to_excel('{0}con_factor_close_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        # indexs_corr.to_excel('{0}con_factor_ret_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        # indexs_corr.to_excel('{0}con_factor_forward_ret_corr_{1}.xlsx'.format(self.data_path, self.end_date))
        return

    def get_amt_prosperity_factor(self):
        factor_list = []
        for file_name in ['factor_close_corr', 'factor_ret_corr', 'con_factor_close_corr', 'con_factor_ret_corr']:
            if file_name in ['factor_close_corr', 'factor_ret_corr']:
                factor_name_list = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS']
            else:
                factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
            indexs_corr_factor = pd.read_excel('{0}{1}_{2}.xlsx'.format(self.data_path, file_name, self.end_date))
            indexs_corr_factor = indexs_corr_factor[['代码'] + factor_name_list].set_index('代码')
            indexs_corr_factor = indexs_corr_factor.fillna(-99999.0)
            indexs_corr_factor = indexs_corr_factor > 0.5
            indexs_corr_factor = indexs_corr_factor.unstack().reset_index()
            indexs_corr_factor.columns = ['景气度指标', '代码', '是否有效']
            indexs_corr_factor = indexs_corr_factor[indexs_corr_factor['是否有效'] == True]
            factor_list.append(indexs_corr_factor)
        factor = pd.concat(factor_list).drop_duplicates()
        factor = factor.groupby('代码').apply(lambda x: '，'.join(x['景气度指标'])).reset_index().rename(columns={0: '景气度指标'})

        con_factor_list = []
        for file_name in ['factor_forward_ret_corr', 'con_factor_forward_ret_corr']:
            if file_name in ['factor_forward_ret_corr']:
                factor_name_list = ['营业收入（元）', '营业收入TTM（元）', '营业收入同比增长率（%）', '单季度营业收入同比增长率（%）', '单季度营业收入环比增长率（%）', '归母净利润（元）', '净利润TTM（元）', '归母净利润同比增长率（%）', '单季度归母净利润同比增长率（%）', '单季度归母净利润环比增长率（%）', 'ROE', '单季度ROE', 'ROE同比增长率（%）', 'ROA', '单季度ROA', '销售毛利率（%）', '单季度销售毛利率（%）', '销售净利率（%）', '单季度销售净利率（%）', 'EPS（基本）', 'BPS']
            else:
                factor_name_list = ['一致预测营业收入（元）', '一致预测营业收入同比增长率（%）', '一致预测营业收入2年复合增长率（%）', '一致预测净利润（元）', '一致预测净利润同比增长率（%）', '一致预测净利润2年复合增长率（%）', '一致预测净利润1周变化率（%）', '一致预测净利润4周变化率（%）', '一致预测净利润13周变化率（%）', '一致预测净利润26周变化率（%）', '一致预测ROE（%）', '一致预测ROE同比增长率（%）', '一致预测EPS', '一致预测BPS']
            indexs_corr_con_factor = pd.read_excel('{0}{1}_{2}.xlsx'.format(self.data_path, file_name, self.end_date))
            indexs_corr_con_factor = indexs_corr_con_factor[['代码'] + factor_name_list].set_index('代码')
            indexs_corr_con_factor = indexs_corr_con_factor.fillna(-99999.0)
            indexs_corr_con_factor = indexs_corr_con_factor > 0.5
            indexs_corr_con_factor = indexs_corr_con_factor.unstack().reset_index()
            indexs_corr_con_factor.columns = ['未来景气度指标', '代码', '是否有效']
            indexs_corr_con_factor = indexs_corr_con_factor[indexs_corr_con_factor['是否有效'] == True]
            con_factor_list.append(indexs_corr_con_factor)
        con_factor = pd.concat(con_factor_list).drop_duplicates()
        con_factor = con_factor.groupby('代码').apply(lambda x: '，'.join(x['未来景气度指标'])).reset_index().rename(columns={0: '未来景气度指标'})

        indexs_factor = pd.read_excel('{0}indexs_factor_ori.xlsx'.format(self.data_path))
        indexs_factor = indexs_factor.merge(factor, on=['代码'], how='left').merge(con_factor, on=['代码'], how='left')
        indexs_factor.to_excel('{0}indexs_factor.xlsx'.format(self.data_path))
        return

    def get_amt_pb_roe(self):
        indexs = self.indexs.copy(deep=True)
        indexs_names_dic = indexs.set_index('代码')['展示名称'].to_dict()
        index_daily_k = self.index_daily_k.copy(deep=True)
        index_daily_k['TRADE_DATE'] = index_daily_k['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_daily_k = index_daily_k[index_daily_k['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index_daily_k = index_daily_k[(index_daily_k['TRADE_DATE'] >= self.start_date) & (index_daily_k['TRADE_DATE'] <= self.end_date)]
        index_finance = self.index_finance.copy(deep=True)
        index_finance['REPORT_DATE'] = index_finance['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_finance = index_finance[index_finance['REPORT_DATE'] >= self.start_date]
        index_consensus = self.index_consensus.copy(deep=True)
        index_consensus['REPORT_DATE'] = index_consensus['REPORT_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_consensus = index_consensus[index_consensus['REPORT_DATE'] >= self.start_date]
        index_con_roe = pd.read_excel('{0}index_con_roe.xlsx'.format(data_path))
        index_con_roe = index_con_roe.set_index('DateTime').unstack().reset_index()
        index_con_roe.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'CON_ROE_FY1']
        index_con_roe['TRADE_DATE'] = index_con_roe['TRADE_DATE'].apply(lambda x: str(x).replace('-', '')[:8])
        index_con_roe = index_con_roe[index_con_roe['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index_con_roe = index_con_roe[(index_con_roe['TRADE_DATE'] >= self.start_date) & (index_con_roe['TRADE_DATE'] <= self.end_date)]
        index_con_roe_yoy = pd.read_excel('{0}index_con_roe_yoy.xlsx'.format(data_path))
        index_con_roe_yoy = index_con_roe_yoy.set_index('DateTime').unstack().reset_index()
        index_con_roe_yoy.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'CON_ROE_YOY']
        index_con_roe_yoy['TRADE_DATE'] = index_con_roe_yoy['TRADE_DATE'].apply(lambda x: str(x).replace('-', '')[:8])
        index_con_roe_yoy = index_con_roe_yoy[index_con_roe_yoy['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index_con_roe_yoy = index_con_roe_yoy[(index_con_roe_yoy['TRADE_DATE'] >= self.start_date) & (index_con_roe_yoy['TRADE_DATE'] <= self.end_date)]
        index_pb_lf = pd.read_excel('{0}index_pb_lf.xlsx'.format(data_path))
        index_pb_lf = index_pb_lf.set_index('DateTime').unstack().reset_index()
        index_pb_lf.columns = ['INDEX_SYMBOL', 'TRADE_DATE', 'PB_LF']
        index_pb_lf['TRADE_DATE'] = index_pb_lf['TRADE_DATE'].apply(lambda x: str(x).replace('-', '')[:8])
        index_pb_lf = index_pb_lf[index_pb_lf['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index_pb_lf = index_pb_lf[(index_pb_lf['TRADE_DATE'] >= self.start_date) & (index_pb_lf['TRADE_DATE'] <= self.end_date)]
        index_pe_ttm = self.index_valuation.copy(deep=True)
        index_pe_ttm['TRADE_DATE'] = index_pe_ttm['TRADE_DATE'].apply(lambda x: str(x).replace('-', ''))
        index_pe_ttm = index_pe_ttm[index_pe_ttm['TRADE_DATE'].isin(self.trade_df['TRADE_DATE'].unique().tolist())]
        index_pe_ttm = index_pe_ttm[(index_pe_ttm['TRADE_DATE'] >= self.start_date) & (index_pe_ttm['TRADE_DATE'] <= self.end_date)]

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pb_lf_index = index_pb_lf[index_pb_lf['INDEX_SYMBOL'] == index]
            index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
            max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
            index_finance_index = index_finance_index[index_finance_index['REPORT_DATE'] <= max_report_date]
            index_finance_index = index_finance_index.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
            index_pb_lf_index = index_pb_lf_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
            index_finance_index = index_finance_index[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE']]
            index_pb_roe = index_finance_index.merge(index_pb_lf_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            sns.lmplot(x='ROE', y='PB_LF', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['ROE'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['ROE'].iloc[i], index_pb_roe['PB_LF'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（历史ROE）', fontsize=10)
            plt.ylabel('ln(PB)', fontsize=10)
            plt.title(indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/roe_{1}_{2}'.format(self.data_path, indexs_names_dic[index], self.end_date))

        max_report_date = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='MAIN_INCOME').dropna().index.max()
        index_finance_latest = index_finance[index_finance['REPORT_DATE'] == max_report_date]
        index_finance_latest = index_finance_latest[index_finance_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_finance_latest = index_finance_latest.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
        index_finance_latest = index_finance_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE']]
        index_pb_lf_latest = index_pb_lf[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
        index_pb_roe = index_finance_latest.merge(index_pb_lf_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
        plt.figure(figsize=(6, 6))
        sns.lmplot(x='ROE', y='PB_LF', data=index_pb_roe, scatter=True, scatter_kws={'color': 'm'}, line_kws={'color': 'm'})
        for i in range(len(index_pb_roe)):
            plt.annotate(indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['ROE'][i], index_pb_roe['PB_LF'][i]), xytext=(index_pb_roe['ROE'][i], index_pb_roe['PB_LF'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（历史ROE）')
        plt.ylabel('ln(PB)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/roe_{1}'.format(self.data_path, self.end_date))

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pb_lf_index = index_pb_lf[index_pb_lf['INDEX_SYMBOL'] == index]
            index_finance_index = index_finance[index_finance['INDEX_SYMBOL'] == index]
            max_report_date = index_finance_index.dropna(subset=['MAIN_INCOME'])['REPORT_DATE'].max()
            index_finance_index = index_finance_index[index_finance_index['REPORT_DATE'] <= max_report_date]
            index_finance_index = index_finance_index.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
            index_pb_lf_index = index_pb_lf_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
            index_finance_index = index_finance_index[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE_Q']]
            index_pb_roe = index_finance_index.merge(index_pb_lf_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            sns.lmplot(x='ROE_Q', y='PB_LF', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            plt.plot(index_pb_roe['ROE_Q'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe))
            for i in range(len(index_pb_roe)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe['ROE_Q'].iloc[i], index_pb_roe['PB_LF'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（单季度ROE）', fontsize=10)
            plt.ylabel('ln(PB)', fontsize=10)
            plt.title(indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/roe_q_{1}_{2}'.format(self.data_path, indexs_names_dic[index], self.end_date))

        max_report_date = index_finance.pivot(index='REPORT_DATE', columns='INDEX_SYMBOL', values='MAIN_INCOME').dropna().index.max()
        index_finance_latest = index_finance[index_finance['REPORT_DATE'] == max_report_date]
        index_finance_latest = index_finance_latest[index_finance_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_finance_latest = index_finance_latest.merge(self.calendar_trade_df.rename(columns={'CALENDAR_DATE': 'REPORT_DATE'}), on=['REPORT_DATE'], how='left')
        index_finance_latest = index_finance_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'ROE_Q']]
        index_pb_lf_latest = index_pb_lf[['TRADE_DATE', 'INDEX_SYMBOL', 'PB_LF']]
        index_pb_roe = index_finance_latest.merge(index_pb_lf_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        index_pb_roe['PB_LF'] = np.log(index_pb_roe['PB_LF'])
        plt.figure(figsize=(6, 6))
        sns.lmplot(x='ROE_Q', y='PB_LF', data=index_pb_roe, scatter=True, scatter_kws={'color': 'm'}, line_kws={'color': 'm'})
        for i in range(len(index_pb_roe)):
            plt.annotate(indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['ROE_Q'][i], index_pb_roe['PB_LF'][i]), xytext=(index_pb_roe['ROE_Q'][i], index_pb_roe['PB_LF'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（单季度ROE）')
        plt.ylabel('ln(PB)')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/roe_q_{1}'.format(self.data_path, self.end_date))

        for i, index in enumerate(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist()):
            index_pe_ttm_index = index_pe_ttm[index_pe_ttm['INDEX_SYMBOL'] == index]
            index_con_roe_index = index_con_roe[index_con_roe['INDEX_SYMBOL'] == index]
            index_pe_ttm_index = index_pe_ttm_index[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
            index_con_roe_index = index_con_roe_index[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1']]
            index_pb_roe = index_pe_ttm_index.merge(index_con_roe_index, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
            index_pb_roe = index_pb_roe.fillna(method='ffill')
            index_pb_roe = index_pb_roe.merge(self.trade_df, on=['TRADE_DATE'], how='left')
            index_pb_roe = index_pb_roe.sort_values('TRADE_DATE', ascending=True).reset_index().drop('index', axis=1)
            index_pb_roe_weekly = index_pb_roe[index_pb_roe['IS_WEEK_END'] == '1']
            index_pb_roe_weekly = index_pb_roe_weekly.sort_values('TRADE_DATE', ascending=False).reset_index().drop('index', axis=1)
            plt.figure(figsize=(6, 6))
            # sns.lmplot(x='CON_ROE_FY1', y='PE_TTM', data=index_pb_roe, scatter=False, line_kws={'color': 'm'})
            # plt.plot(index_pb_roe['CON_ROE_FY1'].values, index_pb_roe['PB_LF'].values, linestyle='dotted', color=line_color_list[2])
            norm = matplotlib.colors.Normalize(vmin=0, vmax=len(index_pb_roe_weekly))
            for i in range(len(index_pb_roe_weekly)):
                c_rgb = matplotlib.cm.Purples_r(norm(i), bytes=True)
                c = from_rgb_to_color16(list(c_rgb)[:3])
                plt.plot(index_pb_roe_weekly['CON_ROE_FY1'].iloc[i], index_pb_roe_weekly['PE_TTM'].iloc[i], '*', color=c)
            plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
            plt.xlabel('预期ROE（一致预测ROE）', fontsize=10)
            plt.ylabel('PE_TTM', fontsize=10)
            plt.title(indexs_names_dic[index], fontsize=10)
            plt.tight_layout()
            plt.savefig('{0}pb_roe/con_roe_{1}_{2}'.format(self.data_path, indexs_names_dic[index], self.end_date))

        index_con_roe_latest = index_con_roe[index_con_roe['TRADE_DATE'] == self.end_date]
        index_con_roe_latest = index_con_roe_latest[index_con_roe_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_con_roe_latest = index_con_roe_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'CON_ROE_FY1']]
        index_pe_ttm_latest = index_pe_ttm[index_pe_ttm['TRADE_DATE'] == self.end_date]
        index_pe_ttm_latest = index_pe_ttm_latest[index_pe_ttm_latest['INDEX_SYMBOL'].isin(self.indexs[self.indexs['板块'] == '先进制造']['代码'].unique().tolist())]
        index_pe_ttm_latest = index_pe_ttm_latest[['TRADE_DATE', 'INDEX_SYMBOL', 'PE_TTM']]
        index_pb_roe = index_con_roe_latest.merge(index_pe_ttm_latest, on=['TRADE_DATE', 'INDEX_SYMBOL'], how='left')
        plt.figure(figsize=(6, 6))
        plt.scatter(index_pb_roe['CON_ROE_FY1'].values, index_pb_roe['PE_TTM'].values, color='m')
        for i in range(len(index_pb_roe)):
            plt.annotate(indexs_names_dic[index_pb_roe['INDEX_SYMBOL'][i]], xy=(index_pb_roe['CON_ROE_FY1'][i], index_pb_roe['PE_TTM'][i]), xytext=(index_pb_roe['CON_ROE_FY1'][i], index_pb_roe['PE_TTM'][i]))  # 这里xy是需要标记的坐标，xytext是对应的标签坐标
        plt.xlabel('预期ROE（一致预测ROE）')
        plt.ylabel('PE_TTM')
        plt.gca().xaxis.set_major_formatter(FuncFormatter(to_percent))
        plt.tight_layout()
        plt.savefig('{0}pb_roe/con_roe_{1}'.format(self.data_path, self.end_date))
        return

    def get_amt_results(self):
        self.get_amt_ret()
        self.get_amt_valuation()
        self.get_amt_prosperity()
        self.get_amt_con_prosperity()
        self.get_amt_prosperity_factor()
        self.get_amt_pb_roe()


if __name__ == '__main__':
    start_date = '20190101'
    end_date = '20220805'
    data_path = 'D:/Git/hbshare/hbshare/fe/xwq/data/industry_tracking/'
    PeTracking(start_date, end_date, data_path).get_amt_results()
    IndustryTracking(start_date, end_date, data_path).get_amt_results()




