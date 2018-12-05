#!/usr/bin/env python
# -*- coding=utf-8 -*-

import configparser
import json

config_path = 'config.ini'

def makeconfig():
    config = configparser.ConfigParser()
    config['library'] = {}
    config['library']['hla_frequency'] = '/WORK/Disease/chenming/Workshop/hla_freq_annotation/HLA_result.xls'
    config['library']['hla_frequency_json'] = '/WORK/Disease/chenming/Workshop/hla_freq_annotation/HLA_result.json'
    with open(config_path,'w') as odata:
        config.write(odata)
    print("{} Has been generated".format(config_path))

def make_library_dict(library):
    '''
    将注释库文件转换为字典
    '''
    library_dict = {}
    with open(library,'r') as indata:
        for line in indata:
            line_list = line.strip().split('\t')
            if line_list[0] not in library_dict:
                library_dict[line_list[0]] = line_list[3]
            else:
                raise Exception('库文件出现了一个重复的注释内容{}'.format(
                    line_list[0]
                ))
    return library_dict

def update_library():
    '''
    用于更新library的json文件
    '''
    config = configparser.ConfigParser()
    config.read(config_path)
    freq_library = config.get('library','hla_frequency',fallback='no library')
    freq_library_json = config.get('library','hla_frequency_json')
    if freq_library =='no library':
        raise Exception('No HLA frequency library exists')
    else:
        library_dict = make_library_dict(freq_library)
        with open(freq_library_json,'w') as odata:
            json.dump(library_dict,odata)
            print('已生成新的注释库json文件')

def main():
    makeconfig()
    update_library()
if __name__ == '__main__':
    main()
        
