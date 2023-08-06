import sys
import zlib
from collections import Counter

import numpy as np
import pandas as pd
import json
import requests
from clonekin import snpool


class TcbData():  # 一个query对应一组数据
    def __init__(self, type=None, name=None, num=None, threshold=None):
        if num == None:
            self.num = '100'
        else:
            self.num = str(num)
        if threshold == None:
            self.threshold = 4
        else:
            self.threshold = threshold
        self.type = type
        self.name = name
        if self.type != None and self.name != None:
            self.url = 'http://166.111.153.73/olmb/api/reqscr.php?t=' + self.type + '&c=' + self.name + '&n=' + self.num
            self.get = requests.get(self.url)
            self.data = json.loads(zlib.decompress(self.get.content))
            self.status = self.get.status_code
            self.info = self.get.reason
            self.co_data = pd.DataFrame()
            if self.check():
                self.impact = self.get_impact()
                self.result = self.summary()
            else:
                print('=======================================================\n'
                      'DATA ERROR::There might be something wrong with dataset\n'
                      '=======================================================' + self.type + self.name,
                      file=sys.stderr)
        else:
            print('======================================================================\n'
                  'URL ERROR::Not a valid query, there might be some missing information!\n'
                  '======================================================================', file=sys.stderr)

    def check(self):  # 检查文件是否完整
        if self.status == 200:
            if self.data['length'] != 0:
                return True
        else:
            print(self.info, file=sys.stderr)

    def get_impact(self):  # 得到impact文件
        data = self.data['data']
        co_data = []
        for k, v in data.items():
            for i in v:
                if i[2] != '' and i[1] != 'synonymous_variant':
                    i.append(k)
                    co_data.append(i)
                if i[2] == '' and 'splice' in i[1]:
                    i[2] = 'splice_variant'
                    i.append(k)
                    co_data.append(i)
        return pd.DataFrame(co_data)

    def summary(self):  # 原genetorch filter函数
        conc = self.impact
        filter = conc.groupby([0, 2]).filter(lambda x: len(x) <= self.threshold)
        result = get_re(filter)
        n = result.shape[0]
        result.index = list(range(n))
        return result

def get_re(co_data):
    co_data = co_data.drop_duplicates()
    genelist = list(set(co_data[0].to_list()))
    line = []
    for gene in genelist:
        temp_df = co_data[co_data[0] == gene]
        sample = list(set(temp_df[3].to_list()))
        size = len(sample)
        var = Counter(temp_df[2].to_list())
        var = dict(var)
        var_num = len(var)
        line.append([sample, size, gene, var, var_num])
    result = pd.DataFrame(line, columns=['sample', 'size', 'gene', 'variation', 'variation_number'])
    result = result[~result['variation'].isin([[]])]
    result = result.sort_values(by=['size'], ascending=False)
    result = result.reset_index(drop=True)
    return result
