#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2019/1/3 11:17
# @User    : zhunishengrikuaile
# @File    : functions.py
# @Email   : binary@shujian.org
# @MyBlog  : WWW.SHUJIAN.ORG
# @NetName : 書劍
# @Software: me blog
# 导入url
import random
import requests
from urllib import parse
from bs4 import BeautifulSoup
from soutuapp.config import ROOT_URL, HEADERS


# requests = requests.session()


class AiUtils(object):

    def get_api(self, image='', type='file'):
        '''
        图片上传
        :param data:
        :return:
        '''
        if type == 'file':
            files = {'name': 'image',
                     'image': open(image, 'rb'),
                     }
            url_post = requests.post(url=ROOT_URL, files=files, headers=HEADERS)
        else:
            data = {'image': image, }
            url_post = requests.post(url=ROOT_URL, data=data, headers=HEADERS)

        if dict(url_post.json()).get('data'):
            return url_post.json()['data']
        else:
            return {False, '图片上传出错！', url_post.text}

    def get_wd(self, url):
        '''
        获取wd
        :param url:
        :return:
        '''
        wd = ''
        wd_text = requests.get(url=url, headers=HEADERS)
        buf_sellect = BeautifulSoup(wd_text.text, 'html5lib')
        wd_select = buf_sellect.select(
            '#graph-c-top-image-edit > article > section > div > div.c-row-tile.graph-c-top-image-edit-text > p')
        for x in wd_select:
            wd = x.text
        if len(wd) != 0:
            return parse.unquote(wd)
        wd_str = wd_text.text.split(
            '<div class="graph-c-similar-load graph-c-similar-more">查看更多相似图片</div></div><script>')
        wd_str1 = wd_text.text.split(
            "<script>M.card.setData('c-guess-imglist', {ajaxImgUrl: 'http://graph.baidu.com/ajax/guesswordpic?")

        # print(wd_str[1])
        # 获取wd1
        try:
            wd_1 = str(wd_str[1]).split('wd=')[1].split('&srcp=&tn=wise&idctag=')[0].replace("&cache=2", "")
            wd = wd_1
        except IndexError:
            pass

        # 获取wd2
        try:
            wd_2 = str(wd_str1[1]).split('wd=')[1].split('&rn=')[0].replace("&cache=2", "")
            wd = wd_2
        except IndexError:
            pass
        return parse.unquote(wd)

    def get_tag(self, url):
        '''
        获取tag
        :param url:
        :return:
        '''
        tag = ''
        tag_text = requests.get(url)
        # 获取tag数据
        tag_str = tag_text.text.split(
            '<li class="graph-w-tag-item graph-c-similar-tag-item"data-url="http://graph.baidu.com/ajax/sims/?')

        # 获取tag=
        try:
            tags = str(tag_str[1]).split('tag=')[1].split('&amp;sign=')[0].replace("&cache=2", "")
            tag = tags
        except IndexError:
            pass
        return parse.unquote(tag)

    def get_xiangshi(self, url, wd, tag, page=1):
        '''
        获取同样类型图片的接口全部相似
        :param url:
        :return:
        str(result_url).replace('http://graph.baidu.com/s?sign=',
                                           'http://graph.baidu.com/ajax/sims/?sign=') + '&wd={}&entrance=&page=1&isNoPage=0'.format(
        wd)
        '''
        # if wd == '' and tag == '':
        #     return False
        if wd == '':
            wd = tag
        url_x = 'http://graph.baidu.com/s?sign='
        url_y = 'http://graph.baidu.com/ajax/sims/?sign='
        url_info = '&wd={}&entrance=&page={}&isNoPage=0'.format(wd, page)
        urls = str(url).replace(url_x, url_y) + url_info
        result = requests.get(url=urls)
        if len(dict(result.json()).get('data')) == 0:
            return {False, result.text, '没有找到全部相识的图'}
        else:
            return result.json()['data']

    def get_miaodongbaike(self, wd, tag, sign):
        '''
        获取秒懂百科视频
        :param wd:
        :param tag:
        :return:
        '''
        if wd == '' and tag == '':
            return False
        if wd == '':
            wd = tag
        url = "http://graph.baidu.com/ajax/imgfacelist?sign={sign}&wd={wd}&rn=15&page=0&type=pano&flag=0&tn=wise&baike_lemma_id=&locid=".format(
            sign=sign, wd=wd)
        print('bk', url)
        result = requests.get(url=url)
        if len(dict(result.json()).get('data')) == 0:
            return {False, '没有秒懂百科视频', str(result.json())}
        else:
            return result.json()['data']

    def get_baike(self, wd, tag):
        '''
        获取当前图片的百度百科资源
        https://baike.baidu.com/item/陈道明?fromtitle=陈道明&fromid=123197
        :param wd:
        :param tag:
        :param sign:
        :return:
        '''
        print(wd, tag, '1111111111')
        if wd == '' and tag == '':
            return False
        if wd == '':
            wd = tag

        url = 'https://baike.baidu.com/item/{wd}?fromtitle={wd}&fromid={fromid}'.format(
            wd=wd,
            fromid='1')
        print(url)
        result = requests.get(url=url, headers=HEADERS, verify=False)

        myencoding = ""
        if result.encoding == 'ISO-8859-1':
            encodings = requests.utils.get_encodings_from_content(result.text)
            #     encodings = requests.utils.get_encodings_from_content(result.text)
            if encodings:
                myencoding = encodings[0]
            else:
                myencoding = result.apparent_encoding
        result_text = result.text.encode('ISO-8859-1').decode(myencoding, 'replace')
        bk_buf = BeautifulSoup(result_text, 'html5lib')
        name = bk_buf.select(
            '#BK_before_content_wrapper > div.card-part > div.title-part > div > div.lemma-title-container > span' or '#J-flower > div')
        if len(name) == 0:
            name = bk_buf.select('#J-flower > div > h1')
        type = bk_buf.select('#J-extra-info > ul > li')
        if len(type) == 0:
            type = bk_buf.select('#topbar > a > em')
        contents = bk_buf.select(
            '#BK_before_content_wrapper > div.card-part > div.summary-content')
        # 如果contents等于空
        if len(contents) == 0:
            contents = bk_buf.select('#J-summary-content')

        # <div class="summary-content ellipsis" id="J-summary-content">
        try:
            for Name, Type, Contens in zip(name, type, contents):
                datas = {
                    'name': Name.text,
                    'type': str(Type.text).replace('收起', '').replace('展开', ''),
                    'contents': str(Contens.text).replace('[1]', '').replace('[2]', '').replace('[3]', '').replace(
                        '[4]', '').replace('[5]', '').replace('[6]', '').replace('[7]', '').replace('[8]', '').replace(
                        '[9]', '').replace('[10]', '').replace('[11]', '').replace('[12]', '').replace('[13]',
                                                                                                       '').replace(
                        '[14]', '').replace('[15]', '').replace('[16]', '').replace('[17]', '').replace('[18]',
                                                                                                        '').replace(
                        '[19]', '').replace('[20]', '').replace('[21]', '').replace('[22]', '').replace('[23]',
                                                                                                        '').replace(
                        '[24]', '').replace('[25]', '').replace('[26]', '').replace('[27]', '').replace('[28]',
                                                                                                        '').replace(
                        '[29]', '')
                }
            # contdata = []
            # for contentS in contents:
            #     contdata.append(contentS.text)
            # datas['contdata'] = contdata
            return datas
        except:
            return False

    def get_image(self, sign, url):
        '''
        获取包含图片的相关信息的图集
        http://graph.baidu.com/view/same?sign=263967eca1ad40524540b01546507452&srcp=imageedit_card&tn=wise&idctag=tc&sids=10010_10125_10027_10003_10004_10103_10201_10040_10072_10062_10081_10191_10291_10391_10692_10703_10706_10301_10708_10802_10902_11006_10903_11003_9999&logid=1450353791&entrance=
        :return:
        '''
        # url = str(url).replace('http://graph.baidu.com/s?', 'http://graph.baidu.com/view/same?').replace(
        #     '&f=all&tn=wise&pageFrom=graph_upload_wise&idctag=tc&sids=',
        #     '&srcp=imageedit_card&tn=wise&idctag=tc&sids=') + '&entrance='
        # print(url, 'images')
        url = 'http://graph.baidu.com/view/same?sign={sign}&srcp=imageedit_card&tn=wise&idctag=tc&sids=10010_10125_10028_10003_10005_10104_10201_10040_10072_10062_10080_10190_10290_10390_10692_10704_10705_10301_10709_10802_10902_11006_10905_10911_11001&logid=1450353791&entrance='.format(
            sign=sign)
        result = requests.get(url=url, headers=HEADERS)
        buf_select = BeautifulSoup(result.text, 'html5lib')
        reqult_str = buf_select.select('#graph-samelist > a > div > div')
        title = buf_select.select('#graph-samelist > a > div > div > div > div')
        data_list = []
        for item, title in zip(reqult_str, title):
            # print(title)
            data = {
                'title': item.text,
                'images': str(title).replace(
                    "<div class=\"graph-same-img graph-w-img graph-w-img-s\" data-click='{\"bt\":\"a-clickImg\"}' data-log=\"button\" data-src=\"",
                    "").replace('"></div>', '').replace('amp;', '')
            }

            data_list.append(data)

        return data_list

    def get_yanzhi(self, sign):
        '''
        获取颜值信息
        :param sign:
        :return:
        '''
        url = "http://graph.baidu.com/s?sign={sign}&wd=&f=face&srcp=&tn=wise&idctag=tc&sids=10010_10125_10028_10003_10005_10104_10201_10040_10072_10062_10080_10190_10290_10390_10692_10704_10705_10301_10709_10802_10902_11006_10905_10911_11001&logid=2121008205&entrance=&pageFrom=tool&ua=".format(
            sign=sign)
        print(url, '颜值')
        get_result = requests.get(url=url, headers=HEADERS)
        buf_select = BeautifulSoup(get_result.text, 'html5lib')
        # 获取脸部标签
        tag_select = buf_select.select(
            '#graph-c-face-booth > div.graph-grid-result-body > div > section.graph-c-face-booth-panel > div.graph-c-face-booth-panel-tag-wrapper.graph-flexbox > div > a')
        # # 获取面向平分
        # resu_select = buf_select.select(
        #     '#graph-c-summary > div.graph-grid-result-title > a > div > div.graph-c-summary-title.graph-w-line-clamp1')
        # # 获取面向吉兄
        # resu_kx_select = buf_select.select(
        #     '#graph-c-summary > div.graph-grid-result-title > a > div > div.graph-c-summary-title-mark > span')
        # 获取面向内容
        resu_content_select = buf_select.select(
            '#graph-c-summary > div.graph-grid-result-body.graph-grid-result-body-withmore > a > div > p')
        # 获取颜值平分
        yanzhi_select = buf_select.select(
            '#graph-c-summary > div.graph-grid-result-title > a > div.graph-c-summary-title-wrapper > div.graph-c-summary-title.graph-w-line-clamp1')
        # 获取颜值标签
        yanzhi_bq_select = buf_select.select(
            '#graph-c-summary > div.graph-grid-result-title > a > div.graph-c-summary-title-wrapper > div.graph-c-summary-title-mark > span')
        # 获取颜值的气质
        yanzhi_qz_select = buf_select.select(
            '#graph-c-summary > div.graph-grid-result-body.graph-grid-result-body-withmore > div > a > p')
        # 获取颜值的面部
        yanzhi_mb_select = buf_select.select(
            '#graph-c-summary > div.graph-grid-result-body.graph-grid-result-body-withmore > div > div > a')
        try:
            tag = {
                'tag': []
            }
            for Tag in tag_select:
                tag['tag'].append(Tag.text)

            for resu_content_select in resu_content_select:
                resu = {
                    # 'resu': str(Resu.text).replace('你的面相评分：', ''),
                    # 'resu_kx': resu_kx_select.text,
                    'resu_content': resu_content_select.text
                }

            for Qz in yanzhi_qz_select:
                yanzhi = {
                    # 'Yanzhi': str(Yanzhi.text).replace('你的面相评分：', ''),
                    # 'Bq': Bq.text,
                    'Qz': str(Qz.text).replace('：', '，')
                }

            # 获取颜值和面向更新操作
            for Yanzhi, Bq in zip(yanzhi_select, yanzhi_bq_select):
                resu['resu'] = yanzhi_select[0].text.replace('你的面相评分：', '')
                resu['resu_kx'] = yanzhi_bq_select[0].text
                yanzhi['Yanzhi'] = yanzhi_select[1].text.replace('你的颜值：', '')
                yanzhi['Bq'] = yanzhi_bq_select[1].text

            mb = []
            for Mb in yanzhi_mb_select:
                mbs = str(Mb.text).replace('面部最美：', '')
                if mbs:
                    mb.append(mbs)

            yanzhi['mb'] = mb

            datas = {
                'tag': tag,
                'resu': resu,
                'yanzhi': yanzhi
            }
            return datas
        except:
            return {'msg': '抱歉没有识别到人脸'}

    def get_miaobaike(self, wd, tag):
        '''
        获取秒懂百科
        :param wd:
        :param tag:
        :return:
        '''
        pass


if __name__ == "__main__":
    test_api = AiUtils()
    get_api = test_api.get_api(image='testimg/dm.jpeg', type='file')
    get_wd = test_api.get_wd(url=get_api['url'])
    get_tag = test_api.get_tag(url=get_api['url'])
    get_xiangshi = test_api.get_xiangshi(url=get_api['url'], wd=get_wd, tag=get_tag)
    get_miaodongbaike = test_api.get_miaodongbaike(sign=get_api['sign'], wd=get_wd, tag=get_tag)
    get_baike = test_api.get_baike(wd=get_wd, tag=get_tag)
    get_image = test_api.get_image(sign=get_api['sign'], url=get_api['url'])
    get_yanzhi = test_api.get_yanzhi(sign=get_api['sign'])
    print('接口1：', get_api)
    print('关键字：', get_wd)
    print('标签：', get_tag)
    print('同样的图', get_xiangshi)
    print('秒懂百科视频', get_miaodongbaike)
    print('百度百科数据', get_baike)
    print('包含图片的信息', get_image)
    print('颜值信息', get_yanzhi)
