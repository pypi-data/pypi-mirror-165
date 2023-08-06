import numpy as np
import pandas as pd
from hbshare.fe.XZ import db_engine as dbeng
from hbshare.fe.XZ import functionality


util=functionality.Untils()
hbdb=dbeng.HBDB()
fre_map={'M':'2101','Q':'2103','HA':'2106','A':'2201','2A':'2202','3A':'2203'}
localdb = dbeng.PrvFunDB().engine

class Multi_factor_model:

    def __init__(self,factor_list,fre):

        self.factor_list=factor_list
        self.fre=fre

        factor_df=pd.DataFrame()
        count=0
        for factor_name in factor_list:

            raw_factor_data = self.factro_loader(factor_name)

            raw_factor_data['month'] = raw_factor_data['date'].astype(str).str[4:6]

            if (fre == 'Q'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['03', '06', '09', '12'])]
            elif (fre == 'HA'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['06', '12'])]
            elif (fre == 'A'):
                raw_factor_data = raw_factor_data.loc[raw_factor_data['month'].isin(['12'])]

            if (count == 0):
                factor_df = raw_factor_data.copy()
            else:
                factor_df = pd.merge(factor_df
                                     , raw_factor_data, how='inner', on=['jjdm', 'date'])
            count += 1

        self.raw_factor_data=factor_df


    @staticmethod
    def factro_loader(factor_name):

        if(factor_name=='25%_year'):

            sql="SELECT * from factor_year_rank_quantile".format(factor_name)
            factor_date=pd.read_sql(sql,con=localdb)[['jjdm','25%','date']].rename(columns={'25%':factor_name})

        elif(factor_name=='25%_half_year'):

            sql="SELECT * from factor_half_year_rank_quantile".format(factor_name)
            factor_date=pd.read_sql(sql,con=localdb)[['jjdm','25%','date']].rename(columns={'25%':factor_name})

        elif (factor_name == 'year_logret'):

            sql="select jjdm,year_logret,date from factor_year_ret where year_logret is not null "
            factor_date=pd.read_sql(sql, con=localdb)

        else:
            print('input factor name is not included in the model by now ')
            raise  Exception

        return  factor_date

    def factor_correlation_check(self):

        factor_df=self.raw_factor_data
        factor_df.drop(['jjdm','month'],axis=1,inplace=True)

        corr_res=factor_df.groupby('date').corr()

        return  corr_res.reset_index().groupby('level_1').mean()

    def get_the_combined_factors(self,method,factor_list=None):

        if(factor_list is None):
            factor_list=self.factor_list

        if(method=='avg'):

            factor_df=self.raw_factor_data[['jjdm','date']+factor_list]
            factor_df['new_factor']=factor_df[factor_list].mean(axis=1)

        else:
            print('the input method is not suppoered ')
            raise  Exception


        return factor_df[['jjdm','date','new_factor']]


if __name__ == '__main__':


    mfm=Multi_factor_model(['25%_year','25%_half_year','year_logret'],fre='Q')
    #corr=mfm.factor_correlation_check()




    print('Done')