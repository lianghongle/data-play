#coding=utf-8

# 获取所有股票的所有历史数据

import src.base as base
import src.history_all as history_all

print('获取所有股票的所有历史数据')

all_stock = base.get_all_stock()

print('遍历所有股票')
# 遍历所有股票
for index in all_stock.index:

    code = all_stock.loc[index].values[0] # 股票代码
    timeToMarket = all_stock.loc[index].values[15] # date = df.ix['600848']['timeToMarket'] #上市日期YYYYMMDD
    print(str(code) + ':' + str(timeToMarket))

    if history_all.load_all(code, timeToMarket):
        continue

print('all stocks load success')
