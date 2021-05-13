'''
Desc: 基金统计
File: /statistic.py
Project: fund_info
File Created: Thursday, 13th May 2021 11:04:55 am
Author: luxuemin2108@gmail.com
-----
Copyright (c) 2021 Camel Lu
'''
import time
import datetime
import os
import sys
sys.path.append('../')
sys.path.append(os.getcwd() + '/src')
from utils.index import get_season_index
from sql_model.fund_query import FundQuery


class FundStatistic:
    def __init__(self):
      # 统计上一个季度
        last_quarter_time = time.localtime(time.time() - 3 * 30 * 24 * 3600)
        time.strftime("%m-%d", last_quarter_time)
        year = time.strftime("%Y", last_quarter_time)
        date = time.strftime("%m-%d", last_quarter_time)
        index = get_season_index(date)
        quarter_index = year + '-Q' + str(index)
        self.quarter_index = quarter_index

    def statistic_stock_fund_count(self, *, query_index=None, filter_count=100):
        each_query = FundQuery()
        query_index = query_index if query_index else self.quarter_index
        results = each_query.select_top_10_stock(query_index)
        # pprint(results)
        code_dict = dict()
        for result in results:
            # print(result)
            for index in range(1, len(result), 2):
                code = result[index]
                name = result[index + 1]
                key = str(code) + '-' + str(name)
                if(key in code_dict and code != None):
                    code_dict[key] = code_dict[key] + 1
                else:
                    code_dict[key] = 1
        filer_dict = dict()

        for key, value in code_dict.items():  # for (key,value) in girl_dict.items() 这样加上括号也可以
            if value > filter_count and key != None:
                filer_dict[key] = value
                # print(key + ":" + str(value))
        list = sorted(filer_dict.items(), key=lambda x: x[1], reverse=True)
        return list
