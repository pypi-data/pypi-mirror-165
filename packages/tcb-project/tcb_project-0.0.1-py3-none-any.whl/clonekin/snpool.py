from clonekin import request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict


class SnPool():
    def __init__(self, query_list):  # load data
        self.data = []
        self.target = []
        self.initiation_list = []
        self.variation_list = pd.DataFrame()
        self.result = pd.DataFrame()
        for i in query_list:
            self.data.append(i.result)
            self.target.append(i.target)
        self.working()

    def ext_gene(self):
        genelist = []
        for i in self.data:
            genelist.extend(i['gene'].to_list())
        return list(set(genelist))

    def working(self):
        genelist = self.ext_gene()
        data = []
        for i in self.data:
            local_gene = i['gene'].to_list()
            local_var = i['variation_number'].to_list()
            local_tab = dict(zip(local_gene, local_var))
            for j in genelist:
                if not j in local_gene:
                    local_tab[j] = 0
            sum_var = sum(local_tab.values())
            for k, v in local_tab.items():
                local_tab[k] = (v + 0.1) * 100 / sum_var
            data.append(local_tab)
        sum_dict = {}
        for _ in data:
            for k, v in _.items():
                sum_dict.setdefault(k, []).append(v)
        cal_dict = {}
        for k, v in sum_dict.items():
            cal_dict[k] = stat(v)
        self.result = pd.DataFrame.from_dict(cal_dict, orient='index', columns=self.target)
        self.initiation_list = pd.DataFrame.from_dict(sum_dict,orient='index', columns=self.target)


    def plot(self, gene):
        x = self.target
        y = list(self.variation_list.loc[self.variation_list['gene'] == gene].values)[0][1:]
        plt.scatter(x, y)
        plt.title('Frequency of ' + gene)


def stat(list_ele):  # 计算新行
    total = 0
    iter_num = len(list_ele)
    new_list = []
    j = 1
    for i in range(iter_num):
        total = total + list_ele[i]
    for i in range(iter_num):
        if total != 0:
            m = list_ele[i] / total
        else:
            m = 1
        j = j * m
        new_list.append(m)
    alt = []
    for i in list_ele:
        alt.append(i)
    alt.sort()
    sec = alt[-2]
    if max(list_ele) != min(list_ele):
        j = (j / (max(new_list) * (max(list_ele) - sec) ** (len(list_ele) - 1))) ** (1 / (len(list_ele) - 1))
    else:
        j = 'NA'
    m_list = ['_'] * len(new_list)
    if j != 'NA':
        for i in range(len(new_list)):
            if new_list[i] == max(new_list):
                m_list[i] = j / new_list[i]
    return m_list


def ext_gene(datalist):
    genelist = []
    for i in datalist:
        genelist.extend(i['gene'].to_list())
    return list(set(genelist))






