#coding=utf-8

# 获取所有股票基本数据，并写入数据库

import time
import tushare as ts
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from conf import db
import os

table_stock = 'stock_stock'

def get_all_stock():

    print('获取所有股票基本数据')

    # 所有股票基本数据的文件,可以临时保存文件
    # tmp_file_all_stock = './../files/all_stock.csv'
    tmp_file_all_stock = './../files/all_stock_' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.csv'
    # tmp_file_all_stock = './../files/all_stock_' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.csv'
    # all_stock.sort_values(by='code').to_csv('./../files/all_stock_' + time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())) + '.csv')

    tmpFileCheck = os.path.isfile(tmp_file_all_stock)
    if tmpFileCheck:
        # 从文件读取所有股票基本数据
        print('从文件读取所有股票基本数据')
        all_stock = pd.read_csv(tmp_file_all_stock, dtype={'code': np.str_, 'totalAssets': np.str_}).sort_values(by='code')
        # print(all_stock.sort_values(by=['code']))
    else:
        # 从API获取所有股票基本数据
        print('从API获取所有股票基本数据')
        all_stock = ts.get_stock_basics()
        all_stock = all_stock.reset_index().sort_values('code')
        all_stock.to_csv(tmp_file_all_stock, index=False)

    # 存入数据库
    engine = create_engine(db.url)
    """
    code,代码
    name,名称
    industry,所属行业
    area,地区
    pe,市盈率
    outstanding,流通股本
    totals,总股本(万)
    totalAssets,总资产(万)
    liquidAssets,流动资产
    fixedAssets,固定资产
    reserved,公积金
    reservedPerShare,每股公积金
    eps,每股收益
    bvps,每股净资
    pb,市净率
    timeToMarket,上市日期
    """
    all_stock.to_sql(table_stock, engine, if_exists='replace', index=False)

    print('获取所有股票基本数据 完成')
    return all_stock





