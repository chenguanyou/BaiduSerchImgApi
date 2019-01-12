from django.conf.urls import url, include

from soutuapp.views import SoutuAppApis     # 上传图片搜图
from soutuapp.views import SouTuurlView     # 使用url搜图

urlpatterns = [
    url('^SoutuAppApis', SoutuAppApis.as_view(), name="SoutuAppApis"),  # 搜图api
    url('SouTuurdlVsiew', SouTuurlView.as_view(), name="SouTuurlView"), # url搜图
]
