#!/usr/bin/env python
# -*- coding=utf-8 -*-

#该脚本用于进行hla分型结果的share分析

#读入文件列表和样本名称列表
#计算每一个基因的每一个分辨率按照AF和样本量计算出来的共有比例
#可选择基因
#可选择分辨率
import re
from collections import defaultdict

def hla_share(args):
    samples_list = args.samples.split(',')
    files_list = args.files.split(',')
    assert len(samples_list) == len(files_list),'样本名称列表应该与文件列表长度一致，且一一对应'
    samples_num = len(samples_list)
    hla_dict = make_hla_dict(samples_list,files_list)
    hla_stat(hla_dict,args.ofile,samples_num,args.resolution,args.sort)

def hla_tag_check(allele):
    '''
    用于检测allele是否有HLA-的标志，如果有就去掉
    '''
    return re.sub('HLA-','',allele.strip())

def make_hla_dict(samples_list,files_list):
    '''
    读入samples 和files并将他们的结果拆解分辨率放入到字典中
    hla_dict结构：hla_name:[sample1,sample2...]
    '''
    hla_dict = defaultdict(list)
    for sam,f in zip(samples_list,files_list):
        with open(f,'r') as indata:
            for line in indata:
                line_list = line.strip().split('\t')
                allele1 = hla_tag_check(line_list[1])
                allele2 = hla_tag_check(line_list[2])
                for allele in [allele1,allele2]:
                    if allele.strip() != '-' and allele.strip() != 'Not typed':
                        alist = allele.split(':')
                        for i in range(len(alist)):
                            key = ":".join(alist[:i+1])
                            hla_dict[key].append(sam)
    
    return hla_dict

def hla_stat(hla_dict,ofile_obj,samples_num,resolution,sort_type):
    '''
    统计AF和样本数的共有数量及百分比并输出到ofile
    '''
    output_list = []
    ofile_obj.write('HLA_typing\tAF_number\tAF_percent\tSample_number\tSample_percent\tSamples\n')
    for i in hla_dict:
        af_num = len(hla_dict[i])
        af_percent = float(af_num)/float(samples_num*2)#每个人有两条allele因此乘2
        sam_num = len({i for i in hla_dict[i]})
        sam_percent = float(sam_num)/float(samples_num)
        if resolution_restrict(i,resolution):
            samples_str = "|".join({j for j in hla_dict[i]})
            output_list.append([i,af_num,af_percent,sam_num,sam_percent,samples_str])
    #排序后输出
    #print(output_list)
    if sort_type == 'alphabet':
        output_list.sort(key=alphabet_sort)
        for i in output_list:
            ofile_obj.write("\t".join(map(str,i))+'\n')
    elif sort_type == 'percent':
        output_list.sort(key=percent_sort)
        for i in output_list:
            ofile_obj.write("\t".join(map(str,i))+'\n')


def resolution_restrict(key,resolution):
    '''
    判断分辨率大小
    '''
    if len(key.split(':'))*2 <=resolution:
        return True
    else:
        return False

def alphabet_sort(key):
    return key[0]

def percent_sort(key):
    return -key[2]
