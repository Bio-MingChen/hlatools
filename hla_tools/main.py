#!/usr/bin/env python
# -*- coding=utf-8 -*-

import argparse

from hla_annotation import freq_annotation

parser = argparse.ArgumentParser(
    prog='hlatools',
    usage='%(prog)s [sub-command] [options]',
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description='''\
    该脚本用于根据hla分析结果进行相关后续分析
    请通过指定子命令来执行相关子功能的内容
    ''',
    epilog = '[contact]chenming@novogene.com')
subparsers = parser.add_subparsers(title='subcommands',
    description='可用子命令',
    help='请输入子命令+ -h来查看子命令的用法')

anno = subparsers.add_parser('anno', 
formatter_class=argparse.RawDescriptionHelpFormatter,
description='''\
该命令用于对hla的结果进行注释，要求输入文件由以下三列构成
基因名称    Allele1    Allele2
输出文件将增加如下几列
AlleleResolution    MostMatchedResolution   FrequencyInLibrary
这几列的含义如下：
HLA分到位数(2,4,6,8);频率注释到的最大位数(2,4,6,8);频率注释(0~1)
''',
help='用于hla位点的频率注释，基于1716个样本的库文件')
share = subparsers.add_parser('share', help='用于hla共有筛选')

anno.add_argument('--file','-f',help='hla的输入文件，由基因名称，Allele1，Allele2三列构成')
anno.add_argument('--ofile','-o',help='hla的输出文件')
anno.set_defaults(func=freq_annotation)

args = parser.parse_args()
args.func(args)