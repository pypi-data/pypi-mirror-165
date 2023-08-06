import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=dbeng.HBDB()
localdb = dbeng.PrvFunDB().engine

def save_mutual_core_pool2locabdb(asofdate):

    data=pd.read_excel(r"C:\Users\xuhuai.zhe\Desktop\核心池列表-20220629_风格.xlsx")

    data=data[['基金代码','基金名称']]
    data['基金经理']=''
    data['asofdate']=asofdate

    data['基金代码']=data['基金代码'].astype(str).str[0:6]

    data.to_sql('core_pool_history',
                con=localdb,index=False,if_exists='append')

def save_wenjian_pool2locabdb(asofdate,factor_name):

    pool_size = 10

    raw_df=pd.read_sql("select * from factor_year_rank_quantile",
                       con=localdb)


    localdb.execute("delete from conservative_pool_{1}_history where asofdate='{0}'".format(asofdate,factor_name.split('%')[0]))

    raw_df=raw_df[(raw_df['date']==asofdate)&(raw_df['count']==17)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('conservative_pool_{0}_history'.format(factor_name.split('%')[0]),con=localdb,index=False,if_exists='append')

def save_wenjian_pool2locabdb(asofdate,factor_name):

    pool_size = 10

    raw_df=pd.read_sql("select * from factor_year_rank_quantile",
                       con=localdb)


    localdb.execute("delete from conservative_pool_{1}_history where asofdate='{0}'".format(asofdate,factor_name.split('%')[0]))

    raw_df=raw_df[(raw_df['date']==asofdate)&(raw_df['count']==17)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('conservative_pool_{0}_history'.format(factor_name.split('%')[0]),con=localdb,index=False,if_exists='append')

def save_momentum_pool2locabdb(asofdate):

    pool_size = 20
    factor_name='year_logret'
    fre='Q'
    raw_df=pd.read_sql("select * from factor_year_ret where  {0} is not null "
                       .format(factor_name)
                       ,con=localdb)


    localdb.execute("delete from momentum_pool_history where asofdate='{}'".format(asofdate))

    raw_df=raw_df[(raw_df['date']==asofdate)].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('momentum_pool_history',con=localdb,index=False,if_exists='append')

def save_info_ratio_pool2locabdb(asofdate):

    pool_size = 50
    factor_name='info_ratio'
    fre='Q'
    raw_df=pd.read_sql("select * from factor_infor_ratio where zblb='2101'",
                       con=localdb)


    localdb.execute("delete from info_ratio_pool_history where asofdate='{}'".format(asofdate))

    raw_df=raw_df[(raw_df['date']==int(asofdate))].sort_values(factor_name
                                               ,ascending=False)[0:pool_size][['jjdm',factor_name]]
    raw_df['asofdate']=asofdate

    raw_df.to_sql('info_ratio_pool_history',con=localdb,index=False,if_exists='append')

if __name__ == '__main__':


    # save_info_ratio_pool2locabdb('20211227')
    # save_info_ratio_pool2locabdb('20220328')
    # save_info_ratio_pool2locabdb('20220627')

    #save_momentum_pool2locabdb('20220630')
    #
    save_wenjian_pool2locabdb('20220630','25%')
    save_wenjian_pool2locabdb('20220331','25%')
    save_wenjian_pool2locabdb('20211231','25%')

    save_wenjian_pool2locabdb('20220630','10%')
    save_wenjian_pool2locabdb('20220331','10%')
    save_wenjian_pool2locabdb('20211231','10%')

    #save_mutual_core_pool2locabdb('202206')

    print('Done')