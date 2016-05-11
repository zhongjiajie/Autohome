#! /usr/bin/python
# -*- coding:utf-8 -*-
import time

#------日志模块------#
#获取当前系统时间 返回 年-月-日 时:分:秒
def getNowTime():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

#---写错误日志到autohome.log---#
def writeErrorLog(errorContent,logName):
    cues = '  ERROR_LOG  '      #日志类型提示
    errorDetail = '[' + getNowTime() + ']' + cues + errorContent
    with open(r'%s.log'%logName,'a') as f:
        f.write(errorDetail + '\n')
    return 0

#---写正常日志到autohome.log---#
def writerNormalLog(normalContent,logName):
    cues = '  NORMAL_LOG '      #日志类型提示
    normalDetail = '[' + getNowTime() + ']' + cues + normalContent
    with open(r'%s.log'%logName,'a') as f:
        f.write(normalDetail + '\n')
    return 0