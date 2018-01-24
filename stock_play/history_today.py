#coding=utf-8

import time

import sys
import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
from conf import db
from multiprocessing import Process

timeFormat = '%Y-%m-%d %H:%M:%S'

py_start = time.time() # print(py_start)
today = time.strftime(timeFormat, time.localtime(py_start)) # print(today)
DateTimeArray = time.strptime(str(today), timeFormat) # print(DateTimeArray) # print(DateTimeArray.tm_hour)
if DateTimeArray.tm_hour < 15:
    print('请15点后运行')
    exit()

table_history = 'stock_history'

today = time.strftime('%Y%m%d',time.localtime(time.time()))
# today = '2017-12-19'

engine = create_engine(db.url)

sql_all_stock_codes = '''
select s.code FROM stock_stock s
  LEFT JOIN stock_history h ON h.code = s.code AND h.date = '{}'
WHERE h.date is NULL
ORDER BY s.code 
'''
print(sql_all_stock_codes.format(today))
all_stock_codes = engine.execute(sql_all_stock_codes.format(today))
print(all_stock_codes)

#
def get_hist_data(codes, start):
    if len(codes) > 0:
        for code in codes:
            # code = row.code
            print(code)
            his_data = ts.get_hist_data(code=code, start=start)
            # print(his_data)
            if his_data is None or his_data.empty:
                print('empty')
                continue
            his_data['code'] = code
            his_data['date'] = today

            # 存入数据库
            try:
                his_data.to_sql(table_history, engine, if_exists='append', index=False)
            except Exception:
                print(sys.exc_info())
                break

# 多进程
# codes_0_1 = []
# # codes_1_2 = []
# # codes_2_3 = []
# codes_3_4 = []
# # codes_4_5 = []
# # codes_5_6 = []
# codes_6_7 = []
#
# for code in all_stock_codes:
#     if code.code > '600000':
#         codes_6_7.append(code.code)
#     elif code.code > '500000':
#         # codes_5_6.append(code.code)
#         continue
#     elif code.code > '400000':
#         # codes_4_5.append(code.code)
#         continue
#     elif code.code > '300000':
#         codes_3_4.append(code.code)
#     elif code.code > '200000':
#         # codes_2_3.append(code.code)
#         continue
#     elif code.code > '100000':
#         # codes_1_2.append(code.code)
#         continue
#     else:
#         codes_0_1.append(code.code)
#
# # code_group = (codes_0_1, codes_1_2, codes_2_3, codes_3_4, codes_4_5, codes_5_6, codes_6_7)
# code_group = (codes_0_1, codes_3_4, codes_6_7)
#
# # r = range(1, 700)
# # step = 100
# # range_list = [ r[x:x+step] for x in range(0,len(r), step)]# 把页码分段
# # print(range_list)
# # exit()
# processList = []
#
# for x in code_group:
#     p = Process(target = get_hist_data, args=(x, today))
#     processList.append(p)
#
# for p in processList:
#     p.start()
#     # p.join()

codes = []
for code in all_stock_codes:
    codes.append(code.code)

# get_hist_data(codes, today)

py_end = time.time()

print(py_start)
print(py_end)
print(py_end - py_start)





