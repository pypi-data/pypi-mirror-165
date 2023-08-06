import  numpy as np
import pandas as pd
from hbshare.fe.XZ import  functionality
from hbshare.fe.XZ import db_engine as dbeng
import datetime

util=functionality.Untils()
hbdb=dbeng.HBDB()
localdb=dbeng.PrvFunDB().engine

def get_jjnav_bydate(jjdm_list,date_list):

    sql="select jjdm,jzrq,fqdwjz from st_fund.t_st_gm_rhb where jzrq in ({0}) and jjdm in ({1})"\
        .format(util.list_sql_condition(date_list),
                util.list_sql_condition(jjdm_list))

    jj_nav=hbdb.db2df(sql,db='funduser')

    return  jj_nav

def create_stock_shift_ratio():

    hsl=pd.read_excel(r"E:\GitFolder\hbshare\fe\factor_analysis\换手率.xlsx")
    date_col=hsl.columns.tolist()
    date_col.remove('证券简称')
    date_col.remove('证券代码')
    new_date_col=[]
    date_map=dict()
    hsl['jjdm'] = hsl['证券代码'].str[0:6]
    for i in range(len(date_col)):
        new_date_col.append(date_col[i].replace('H1','0630').replace(' ','').replace('H2', '1231'))

    date_map = dict(zip(date_col,new_date_col))

    outputdf=pd.DataFrame()
    tempdf=pd.DataFrame()
    tempdf['jjdm']=util.get_mutual_stock_funds('20211231')
    tempdf=pd.merge(tempdf,hsl,how='left',on='jjdm')

    for date in date_col:
        tempdf2=tempdf[['jjdm',date]]
        tempdf2['date']=date_map[date]
        tempdf2.rename(columns={date:'hsl'},inplace=True)
        outputdf=pd.concat([outputdf,tempdf2],axis=0)

    outputdf=outputdf[outputdf['hsl'].notnull()]

    outputdf.to_sql('factor_hsl',con=localdb,index=False,if_exists='append')

def read_factors(table_name):

    sql="select * from {}".format(table_name)
    df=pd.read_sql(sql,con=localdb)

    return  df

def bhar(arr):
    return 100 * (np.power(np.cumprod((arr + 100) / 100).tolist()[-1], 1 / len(arr)) - 1)

def get_quarter_ret(arr):

    return  np.cumprod(arr/100+1).tolist()[-1]-1

def hsl_rank2db(dir):

    #get the hsl raw data first
    # sql="select * from factor_hsl  "
    # df=pd.read_sql(sql,con=localdb)
    df=pd.read_csv(dir)
    df['hsl_rank']=df.groupby('date').rank(method='min')
    count=df.groupby('date', as_index=False).count()[['date', 'jjdm']]
    count.rename(columns={'jjdm':'count'},inplace=True)
    df=pd.merge(df,count,how='left',on='date')
    df['hsl_rank']=df['hsl_rank']/df['count']
    df.to_sql('factor_hsl',con=localdb,index=False,if_exists='append')

def save_fund_return_factor2db():

    jjdm_list=util.get_mutual_stock_funds('20211231')

    #get year end date

    sql_script = "SELECT JYRQ, SFJJ, SFYM,SFZM FROM funddb.JYRL WHERE JYRQ >= {0} and JYRQ <= {1} and SFJJ=0 ".format(
        '20141231', datetime.datetime.today().strftime('%Y%m%d'))
    trade_calander = hbdb.db2df(sql_script, db='readonly').drop('ROW_ID',axis=1).sort_values('JYRQ')
    month_end_list=trade_calander[trade_calander['SFYM']=='1']['JYRQ'].tolist()
    #
    # trade_calander['year'] = trade_calander['JYRQ'].astype(str).str[0:4]
    # year_end_list=trade_calander.groupby('year')['JYRQ'].max().tolist()

    #get month end jj fqnav

    jj_nav=get_jjnav_bydate(jjdm_list,month_end_list)
    jj_nav['month'] = jj_nav['jzrq'].astype(str).str[4:6]
    jj_nav['date']=jj_nav['jzrq']
    jj_nav.set_index('jzrq',inplace=True)
    #get jj year return for each month end date


    jj_nav['year_logret']=np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(12)+1)
    jj_nav['2year_logret'] = np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(24) + 1)
    jj_nav['3year_logret'] = np.log(jj_nav.groupby('jjdm')['fqdwjz'].pct_change(36) + 1)

    jj_nav['year_end_flag']=0
    jj_nav['quarter_end_flag'] = 0
    jj_nav.loc[jj_nav['month']=='12','year_end_flag']=1
    jj_nav.loc[jj_nav['month'].isin(['03','06','09','12'])
    , 'quarter_end_flag'] = 1
    jj_nav['date']=jj_nav['date'].astype(str)

    #localdb.execute('delete from factor_year_ret')
    jj_nav[jj_nav.notnull()].rename(columns={'jzrq':'date'})[['jjdm'
        , 'year_logret','2year_logret','3year_logret', 'date','year_end_flag', 'quarter_end_flag']].to_sql('factor_year_ret'
                                                                       ,con=localdb
                                                                       ,index='False'
                                                                       ,if_exists='append')


def save_fund_rank_factor2db():

    #get the quarter end date
    sql= "SELECT JYRQ, SFYM FROM funddb.JYRL WHERE JYRQ >= {0} and JYRQ<={1} and SFJJ=0 and SFYM=1".format(
        '20160101',datetime.datetime.today().strftime('%Y%m%d'))
    calander = hbdb.db2df(sql, db='readonly').drop('ROW_ID',axis=1)
    calander['month']=calander['JYRQ'].astype(str).str[4:6]
    calander=calander.loc[calander['month'].isin(['03','06','09','12'])]['JYRQ'].tolist()
    calander.sort()

    result=[[],[],[]]

    for date in calander:
        fund_pool=util.get_mutual_stock_funds(date,2)
        sql = "select jjdm,tjyf,rqzh,hb1y from st_fund.t_st_gm_yhb where jjdm in ({0}) and rq1y!=99999 {1} {2} " \
            .format(util.list_sql_condition(fund_pool)
                    , "and rqzh>='{}'".format( str(int(date[0:4])-5)+date[4:6]+'01')
                    , "and rqzh<='{}'".format(date))
        montly_ret = hbdb.db2df(sql, db='funduser')

        #get quarter,half_yearly,yearly return
        montly_ret['hb1q']=montly_ret.groupby('jjdm')['hb1y'].rolling(3).apply(get_quarter_ret).values
        montly_ret['hb1hy']=montly_ret.groupby('jjdm')['hb1y'].rolling(6).apply(get_quarter_ret).values
        montly_ret['hb1y']=montly_ret.groupby('jjdm')['hb1y'].rolling(12).apply(get_quarter_ret).values
        montly_ret['month']=montly_ret['rqzh'].astype(str).str[4:6]
        first_month=montly_ret['tjyf'].min()

        montly_ret=montly_ret.loc[(montly_ret['month'].isin(['03','06','09','12']))&(montly_ret['tjyf']!=first_month)]
        montly_ret['ret_q_rank_per_quarter']=montly_ret.groupby('tjyf').rank(method='min')['hb1q']
        montly_ret['ret_hy_rank_per_quarter']=montly_ret.groupby('tjyf').rank(method='min')['hb1hy']
        montly_ret['ret_y_rank_per_quarter']=montly_ret.groupby('tjyf').rank(method='min')['hb1y']

        montly_ret=pd.merge(montly_ret
                            ,montly_ret.groupby('tjyf').count()['jjdm'].to_frame('count')
                            ,how='left',on='tjyf')

        i=0
        for col in ['ret_q_rank_per_quarter','ret_hy_rank_per_quarter','ret_y_rank_per_quarter']:
            montly_ret[col]=montly_ret[col]/montly_ret['count']
            tempdf=montly_ret.groupby('jjdm')[col].describe()
            tempdf['date']=date
            result[i].append(tempdf.reset_index())
            i+=1

    name_list = ['quarter', 'half_year', 'year']

    for i in range(3):

        sql="delete from factor_{}_rank_quantile".format(name_list[i])
        localdb.execute(sql,con=localdb)
        pd.concat(result[i],axis=0).to_sql('factor_{}_rank_quantile'.format(name_list[i])
                                           ,con=localdb,index=False,if_exists='append')





if __name__ == '__main__':


    #save_fund_rank_factor2db()

    save_fund_return_factor2db()

    # df=read_factors('factor_hsl')
    # df=df.groupby('jjdm').min()
    # df=df[df['hsl'] >= 350]
    #
    # jjdm_list=df.index.tolist()
    # jjdm_con=util.list_sql_condition(jjdm_list)
    #
    # sql="""select jjdm,hb1n,rqzh from st_fund.t_st_gm_nhb
    # where hb1n!=99999 and jjdm in ({0}) and tjnf in ('2015','2016','2017','2018','2019','2020','2021')"""\
    #     .format(jjdm_con)
    # ret=hbdb.db2df(sql,db='funduser')
    # ret=ret.groupby('jjdm')['hb1n'].apply(bhar)
    # ret.to_csv('hlsret.csv',encoding='gbk')
    # print('')