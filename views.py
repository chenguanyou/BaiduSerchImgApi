import os
import time
from uuid import uuid4
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

# 导入sdk
from soutuapp.functions import AiUtils  # 导入搜图SDK

# 导入路径
from MeBlog.settings import BASE_DIR

this_path = os.path.join(BASE_DIR, 'apps/soutuapp/testimg/')


# Create your views here.

class SoutuAppApis(views.APIView):
    '''
    以图搜图接口，
    目前接口不需要进行登陆即可访问
    '''

    def post(self, request, format=None):
        this_img = request.data.get('images')
        img_name = this_path + str(time.time()) + '.jpg'
        with open(img_name, 'wb+') as file_imgs:
            for item in this_img:
                file_imgs.write(item)
            file_imgs.close()

        # 获取本地图片
        AiApi = AiUtils()
        get_api = AiApi.get_api(image=img_name, type='file')
        url = get_api['url']
        sign = get_api['sign']
        get_wd = AiApi.get_wd(url=url)
        get_tag = AiApi.get_tag(url=url)
        get_xiangshi = AiApi.get_xiangshi(url=url, wd=get_wd, tag=get_tag)
        get_miaodongbaike = AiApi.get_miaodongbaike(sign=sign, wd=get_wd, tag=get_tag)
        get_baike = AiApi.get_baike(wd=get_wd, tag=get_tag)
        get_image = AiApi.get_image(sign=sign, url=url)
        get_yanzhi = AiApi.get_yanzhi(sign=sign)
        data = {
            'get_wd': get_wd,
            'get_tag': get_tag,
            'get_xiangshi': get_xiangshi,
            'get_miaodongbaike': get_miaodongbaike,
            'get_baike': get_baike,
            'get_image': get_image,
            'get_yanzhi': get_yanzhi
        }
        # print('接口1：', get_api)
        # print('关键字：', get_wd)
        # print('标签：', get_tag)
        # print('同样的图', get_xiangshi)
        # print('秒懂百科视频', get_miaodongbaike)
        # print('百度百科数据', get_baike)
        # 进行本地文件的删除,先判断是否是文件
        if (os.path.isfile(img_name)):
            os.system('rm -rf {}'.format(img_name))
        else:
            pass

        return Response(data, status=status.HTTP_200_OK)


class SouTuurlView(views.APIView):
    '''
    使用url图片链接进行搜图
    '''

    def post(self, request, format=None):
        img_url = request.data.get('image_url')
        # 获取本地图片
        AiApi = AiUtils()
        get_api = AiApi.get_api(image=img_url, type='url')
        if get_api.get('sign') == None:
            data = {"massage": "图片链接不合法"}
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        url = get_api['url']
        sign = get_api['sign']
        get_wd = AiApi.get_wd(url=url)
        get_tag = AiApi.get_tag(url=url)
        get_xiangshi = AiApi.get_xiangshi(url=url, wd=get_wd, tag=get_tag)
        get_miaodongbaike = AiApi.get_miaodongbaike(sign=sign, wd=get_wd, tag=get_tag)
        get_baike = AiApi.get_baike(wd=get_wd, tag=get_tag)
        get_image = AiApi.get_image(sign=sign, url=url)
        get_yanzhi = AiApi.get_yanzhi(sign=sign)
        data = {
            'get_wd': get_wd,
            'get_tag': get_tag,
            'get_xiangshi': get_xiangshi,
            'get_miaodongbaike': get_miaodongbaike,
            'get_baike': get_baike,
            'get_image': get_image,
            'get_yanzhi': get_yanzhi
        }
        # print('接口1：', get_api)
        # print('关键字：', get_wd)
        # print('标签：', get_tag)
        # print('同样的图', get_xiangshi)
        # print('秒懂百科视频', get_miaodongbaike)
        # print('百度百科数据', get_baike)
        # 进行本地文件的删除,先判断是否是文件
        # if (os.path.isfile(img_name)):
        #     os.system('rm -rf {}'.format(img_name))
        # else:
        #     pass

        return Response(data, status=status.HTTP_200_OK)
