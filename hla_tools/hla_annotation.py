#!/usr/bin/env python
# -*- coding=utf-8 -*-

#该脚本用于HLA频率的注释与整合
#功能1：根据1716个人的HLA注释库文件对各个脚本的HLA结果进行注释
#功能2：对不同的样本进行HLA share的一个比较，支持设置control

#注释文件预期生成的列：
#title上面的注释内容：样本名称，
#title内容：基因名称 allele1 allele2 细分程度(2，4，6，8) 频率注释细分程度(2,4,6,8) 频率注释
#share的结果在以上的title增加如下几列
#样本名称 # 2分位共有 4分位共有 6分位共有 8分位共有
#这里共有的计算方式有两种，一种是按照allele，一种是按照样本数 
import sys
import re
import json
import configparser
import argparse

def get_library_dict():
    '''
    从json文件中读取library dictionary
    '''
    config = configparser.ConfigParser()
    config.read('config.ini')
    library_path = config.get('library','hla_frequency_json',feedback='no')
    if library_path == 'no':
        raise Exception('No HLA library json exists!')
    else:
        with open(library_path,'r') as indata:
            library_dict = json.load(indata)
    return library_dict

def hla_tag_check(allele):
    '''
    用于检测allele是否有HLA-的标志，如果有就去掉
    '''
    return re.sub('HLA-','',allele.strip())

def typing_freq(allele,library_dict):
    '''
    用于给allele的分型结果进行频率注释，判断分型的位数并给予对应的频率，
    如果没有对应的频率就向前两位再进行判断。
    返回结果包括(分辨率(2,4,6,8),人群频率分辨率，人群频率)
    '''
    resolution = len(allele.split(':'))*2
    print(allele)
    if allele.strip() == '-' or allele.strip() == 'Not typed':
        freq = '.'
        match_resolution = 0
        resolution = '.'
    else:
        while True:
            freq = library_dict.get(allele.strip(),False)
            if not freq:
                if not allele:
                    freq = "."
                    match_resolution = 0
                    break
                allele = ":".join(allele.split(':')[:-1])
            else:
                freq = str(round(float(freq),8))#参照GnormAD保留小数点后面8位
                match_resolution = len(allele.split(':'))*2
                break
        
    
    print(str(resolution),str(match_resolution),str(freq))
    return (str(resolution),str(match_resolution),str(freq))

def HLA_annotation(filename,ofile,library_dict):
    '''
    该脚本用于对HLA的结果文件进行注释，结果文件分为三列，分别是基因，allele1 allele2
    '''
    with open(filename,'r') as indata,\
    open(ofile,'w') as odata:
        otitle = "HLAGene\tAllele1\tAllele2\tAlleleResolution\tMostMatchedResolution\tFrequencyInLibrary\n"
        odata.write(otitle)
        for line in indata:
            line_list = line.strip().split('\t')
            allele1 = hla_tag_check(line_list[1])
            allele2 = hla_tag_check(line_list[2])
            anno_tuple1 = typing_freq(allele1,library_dict)
            anno_tuple2 = typing_freq(allele2,library_dict)
            anno_items = ["/".join(i) for i in zip(anno_tuple1,anno_tuple2)]
            for i in anno_items:
                line_list.append(i)
            odata.write("\t".join(line_list)+'\n')

def freq_annotation(args):
    filename = args.file
    ofile = args.ofile
    library_dict = get_library_dict()
    HLA_annotation(filename,ofile,library_dict)

#if __name__ == '__main__':
    # if len(sys.argv) != 3:
    #    raise Exception('接收2个参数，依次为输入文件，输出文件')
    # filename = sys.argv[1]
    # ofile = sys.argv[2]
    # main(filename,ofile)
    #library_dict = make_library_dict('HLA_result.xls')
    #typing_freq('DPB1*104:01',library_dict)