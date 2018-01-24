#coding=utf-8

# 获取所有股票的所有历史数据

import time

import sys
import tushare as ts
from sqlalchemy import create_engine
from conf import db
import stock_play.base as base

table_history_all = 'stock_history_all'

engine = create_engine(db.url)

# 下载所有（从上市到最近一天）
def load_all(code, timeToMarket):

    # time.strftime('%Y-%m-%d', time.localtime(date))
    # print(date.strftime("%Y-%m-%d %H:%M:%S"))
    date = timeToMarket
    # date = '19910403'

    startDateArray = time.strptime(str(date), "%Y%m%d")
    # date = time.strftime("%Y-%m-%d", startDateArray)
    # print(startDateArray)

    endDataArray = time.strptime(str(time.strftime('%Y-%m-%d',time.localtime(time.time()))), "%Y-%m-%d")
    # print(endDataArray)

    years = range(startDateArray.tm_year, endDataArray.tm_year + 1)
    print(years)

    for year in years:
        if get_year_data_to_db(code, year):
            continue
        else:
            time.sleep(60)

    print(code + ' load success')
    return True

# 更新最近一年
def load_new_year(code):

    endDataArray = time.strptime(str(time.strftime('%Y-%m-%d',time.localtime(time.time()))), "%Y-%m-%d")

    if get_year_data_to_db(code, endDataArray.tm_year) != True:
        time.sleep(60)

    print(code + ' load success')
    return True


# 获取一个股票一年数据，并保存数据库
def get_year_data_to_db(code, year):

    year_start_date = str(year) + '-01-01'
    year_end_date = str(year) + '-12-31'

    # 最新一年，都从新获取
    if year == time.localtime(time.time()).tm_year:
        sql_delete = '''
                    DELETE FROM {} WHERE code = '{}' AND `date` BETWEEN '{}' AND '{}'
                    '''
        result = engine.execute(sql_delete.format(table_history_all, code, year_start_date,
                                                      year_end_date))  # first()/fetchone()/scalar()
        print('最新一年')
        print(result.rowcount)
    else:
        sql_check = '''
            select count(*) FROM {} WHERE code = '{}' AND `date` BETWEEN '{}' AND '{}' limit 1
            '''
        check_count = engine.execute(sql_check.format(table_history_all, code, year_start_date,
                                                      year_end_date)).scalar()  # first()/fetchone()/scalar()
        print(check_count)

        # 有数据，暂且当作当年的数据已经写入过
        if check_count > 0:
            print(str(code) + '：' + str(year) + '---exists')
            return True

    try:
        time.sleep(1)
        his_h_data = ts.get_h_data(code=code, start=year_start_date, end=year_end_date, pause = 3) # pause 防止请求频繁
    except OSError:
        # time.sleep(60)
        print(str(code) + '：' + str(year) + '---OSError')
        return False
    except Exception:
        print(str(code) + '：' + str(year) + '---error')
        print(sys.exc_info())
        return True

    his_h_data['code'] = code

    his_h_data.to_sql(table_history_all, engine, if_exists='append', index=True)
    # print(his_h_data)

    # 顺利完成，返回
    print(str(code) + '：' + str(year) + '---successed')
    return True
