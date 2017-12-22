#coding=utf-8

# 获取所有股票的最近一年所有数据

import src.base as base
import src.history_all as history_all

print('获取所有股票的最近一年所有数据')

all_stock = base.get_all_stock()

print('遍历所有股票')
# 遍历所有股票
for index in all_stock.index:

    code = all_stock.loc[index].values[0] # 股票代码
    print(str(code))

    if history_all.load_new_year(code):
        continue

print('all stocks load success')
