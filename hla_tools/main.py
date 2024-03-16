#!/usr/bin/env python
# -*- coding=utf-8 -*-
import sys
import argparse

from hla_annotation import freq_annotation
from hla_share import hla_share

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
该命令用于对hla的结果进行注释，
输出文件将增加如下几列
AlleleResolution    MostMatchedResolution   FrequencyInLibrary
这几列的含义如下：
HLA分到位数(2,4,6,8);频率注释到的最大位数(2,4,6,8);频率注释(0~1)
''',
help='用于hla位点的频率注释，基于1716个样本的库文件')
share = subparsers.add_parser('share', help='用于hla共有筛选')
share.add_argument('--samples','-s',help='样本名称列表，与输入文件一一对应')
share.add_argument('--files','-f',help='文件输入列表，数量应该与samples参数一致')
share.add_argument('--resolution','-r',choices=[2,4,6,8],type=int,default=8,help='选择输出的HLA基因分辨率，默认都输出')
share.add_argument('--ofile','-o',nargs='?',type=argparse.FileType('w'),default=sys.stdout,
help='hla的输出文件,默认输出到标准输出')
share.add_argument('--sort',choices=['alphabet','percent'],default='alphabet',
help='结果排序方法，默认为按基因字母顺序排序，可选择按照百分比从大到小输出')
share.set_defaults(func=hla_share)

anno.add_argument('--file','-f',help='hla的输入文件')
anno.add_argument('--ofile','-o',nargs='?',default=sys.stdout,type=argparse.FileType('w'),help='hla的输出文件')
anno.add_argument('--method','-m',choices=['exact','recursion'],default='exact',
help='查询模式，可选择递归查询或者精确查询，默认为精确匹配,在递归模式下，查询的HLA分型将在得不到结果时自动去除两位再查询，直到2分位')
anno.add_argument('--anno_cols','-c',default=[2,3],nargs='+',type=int,
help='指定需要进行频率注释的列，可以为一到多列，列数从1开始，默认为2，3列,空格分隔')
anno.add_argument('--head',action='store_true',
help='该参数用于说明输入文件第一行是否为标题行，如果是，则会自动为该标题行添加AlleleResolution\tMostMatchedResolution\tFrequencyInLibrary，否则不添加')
anno.set_defaults(func=freq_annotation)

args = parser.parse_args()
args.func(args)