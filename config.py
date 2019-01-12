#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 11:02
# @User    : zhunishengrikuaile
# @File    : config.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: me blog
'''
百度搜图的配置文件
'''
import random

# 百度识图的url接口
ROOT_URL = "http://graph.baidu.com/upload?uptime="#{}".format(random.randint(1000000, 20000000000))

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Pragma": "no-cache",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1"
}
