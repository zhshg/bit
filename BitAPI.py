"""
@Author: 小样
@Date: 2022-10-30
@wechat: mz-cyx
@description: 比特浏览器API接口
@version: 1.0
@AD: 专业定制外网自动化程序，Twitter、Facebook、Tiktok等等

##所有定义的接口
#1. 浏览器接口
#1.1 创建浏览器 browser_id=bit.create_driver(username, password, proxyType, proxyIp, proxyPort, proxyUsername, proxyPassword, **kwargs)
#1.2 打开浏览器 bit.open_browser(browser_id)
#1.3 关闭浏览器 bit.close_browser(browser_id)
#1.4 删除浏览器 bit.del_browser(browser_id)
#1.5 获取浏览器详情 bit.browser_detail(browser_id)
#1.6 获取浏览器列表 bit.browser_list(page=0,pageSize=100,username='',groupId='')
#1.7 窗口排列 bit.windowbounds(type = 'box', startX = 0, startY = 0, width = 500, height = 500, col = 3, spaceX = 0, spaceY = 0, offsetX = 0, offsetY = 0)
#1.8 更新窗口分组 bit.update_browser_group(group_id, browser_ids)
#1.9 更新浏览器代理 bit.update_browser_proxy(self, browser_id, proxyType, proxyIp, proxyPort, proxyUser, proxyPass)
#1.10 更新浏览器备注 bit.update_browser_remark(browser_id,remark)
#1.11 通过序号关闭窗口 bit.batch_close_browser_by_seq(seqs)

#2. 分组接口
#2.1 添加分组 bit.add_group(group_name)
#2.2 编辑分组 bit.edit_group(group_id,group_name)
#2.3 删除分组 bit.del_group(group_id)
#2.4 获取分组列表 bit.group_list(page=0,pageSize=100)
#2.5 获取分组详情 bit.group_detail(group_id)

#3. 其他自定义的方法
#3.1 获取端口 bit.get_bit_port()
#3.2 创建并打开分组，返回webdriver对象和窗口ID driver,driver_id=bit.get_driver(username='', password='', proxyType='noproxy', proxyIp='', proxyPort='', proxyUsername='', proxyPassword='', **kwargs)
#3.3 获取浏览器的指定字段信息 bit.get_browser_info(driver_id,columns=['name','remark']) #columns为要获取的字段，返回字典
#3.4 更新浏览器的分组（直接传分组名，有别于官方的更新分组接口） bit.update_browser_groupname(driver_id,group_name)
#3.5 获取指定分组名的id bit.query_group_id(group_name)
#3.6 获取或添加分组，返回分组ID bit.get_or_add_group(group_name)
#3.7 获取浏览器窗口的分组名 bit.query_browser_group_name(driver_id)


#使用前，安装依赖：
# pip install requests selenium faker loguru
# 请自行将104版本的chromedriver.exe和脚本放同一个目录下
"""
from selenium import webdriver
import os
import time
import random
import requests
import json
from faker import Faker
from loguru import logger

faker = Faker()
webgl_vendors = ['Google Inc.', 'Microsoft',
                 'Apple Inc.', 'ARM', 'Intel Inc.', 'Qualcomm']
webgl_renders = ['ANGLE (Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 5300 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 620 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (Intel(R) HD Graphics Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (NVIDIA GeForce GTX 1050 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2070 SUPER Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics Family Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0)', 'Intel(R) HD Graphics 4600', 'ANGLE (NVIDIA GeForce GTX 750 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K600 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro M1000M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon (TM) R9 370 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (AMD Radeon HD 7700 Series Direct3D9Ex vs_3_0 ps_3_0)', 'Apple GPU', 'Intel(R) UHD Graphics 620', 'Mali-G72', 'Mali-G72 MP3', 'ANGLE (NVIDIA GeForce GTX 750  Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 750 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 750 Ti Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 760 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 770 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 780 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 850M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 850M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 860M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 950M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 950M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 960 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 960 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 960M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 960M Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 970 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 980 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 980 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce GTX 980 Ti Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce GTX 980M Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX130 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX150 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX230 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce MX250 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2060 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2060 Direct3D9Ex vs_3_0 ps_3_0)', 'ANGLE (NVIDIA GeForce RTX 2060 SUPER Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA GeForce RTX 2070 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro K620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro FX 380 Direct3D11 vs_4_0 ps_4_0)', 'ANGLE (NVIDIA Quadro NVS 295 Direct3D11 vs_4_0 ps_4_0)', 'ANGLE (NVIDIA Quadro P1000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P2000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P400 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P4000 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P600 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (ATI Mobility Radeon HD 4330 Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (ATI Mobility Radeon HD 4500 Series Direct3D11 vs_4_1 ps_4_1)', 'ANGLE (ATI Mobility Radeon HD 5000 Series Direct3D11 vs_5_0 ps_5_0)',
                 'ANGLE (ATI Mobility Radeon HD 5400 Series Direct3D11 vs_5_0 ps_5_0)', 'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8935)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6079)', 'ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7870)', 'ANGLE (AMD, Radeon (TM) RX 470 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.1034.6)', 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-10.18.13.6881)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 970 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)', 'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.14028.11002)', 'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8681)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.5671)', 'ANGLE (AMD, AMD Radeon RX 5700 XT Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13025.1000)', 'ANGLE (AMD, AMD Radeon RX 6900 XT Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13011.1004)', 'ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.13002.23)', 'ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9466)', 'ANGLE (Intel, Intel(R) HD Graphics 5500 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5126)', 'ANGLE (Intel, Intel(R) HD Graphics 6000 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5126)', 'ANGLE (Intel, Intel(R) HD Graphics 610 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9466)', 'ANGLE (Intel, Intel(R) HD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9168)', 'ANGLE (Intel, Intel(R) HD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6589)', 'ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.9126)', 'ANGLE (Intel, Mesa Intel(R) UHD Graphics 620 (KBL GT2), OpenGL 4.6 (Core Profile) Mesa 21.2.2)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050 Ti/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 460.73.01)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050 Ti/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 460.80)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1050/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1060 6GB/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1080 Ti/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 1650/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 650/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 750 Ti/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 860M/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce GTX 950M/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce MX150/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, GeForce RTX 2070/PCIe/SSE2, OpenGL 4.5 core)', 'ANGLE (NVIDIA Corporation, NVIDIA GeForce GTX 660/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 470.57.02)', 'ANGLE (NVIDIA Corporation, NVIDIA GeForce RTX 2060 SUPER/PCIe/SSE2, OpenGL 4.5.0 NVIDIA 470.63.01)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll-26.21.14.4250)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 5GB Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7168)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1060 6GB Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7212)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1070 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6677)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1080 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7111)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7212)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1650 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7111)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 SUPER Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7196)', 'ANGLE (NVIDIA, NVIDIA GeForce GTX 1660 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-30.0.14.7196)']
color_depths = [1, 2, 3, 4, 5, 8, 12, 15, 16, 18, 24, 30, 32, 48]
systems = ['Win32', 'Linux i686', 'Linux armv7l', 'MacIntel']
payload_config = {
    "groupId": "",  # 群组ID，绑定群组时传入，如果登录的是子账号，则必须赋值，否则会自动分配到主账户下面去
    "platform": '',  # 账号平台
    "platformIcon": 'other',  # 取账号平台的 hostname 或者设置为other
    "url": '',  # 打开的url，多个用,分开
    "name": '',  # 窗口名称
    # 备注
    "remark": '',
    "userName": '',  # 用户账号
    # "password": password,  # 用户密码
    "password": '',  # 用户密码
    "cookie": '',  # cookie
    "proxyMethod": 2,  # 代理类型 2自定义;3提取IP
    # 自定义代理类型 ['noproxy', 'http', 'https', 'socks5']
    "proxyType": 'noproxy',
    "host": '',  # 代理主机
    "port": '',  # 代理端口
    "proxyUserName": '',  # 代理账号
    "proxyPassword": '',  # 代理密码
    'dynamicIpUrl': '',  # proxyMethod = 3时，提取IP链接
    'dynamicIpChannel': '',  # 提取链接服务商，rola | doveip | cloudam | common
    'isDynamicIpChangeIp': False,  # 每次打开都提取新IP，默认false
    # ip检测服务IP库，默认ip-api，选项 ip-api | ip123in | luminati，luminati为Luminati专用
    'ipCheckService': 'ip-api',
    'abortImage': False,  # 是否禁止图片加载
    'abortMedia': False,  # 是否禁止媒体加载
    'stopWhileNetError': False,  # 网络错误时是否停止
    'syncTabs': False,  # 是否同步标签页
    'syncCookies': True,  # 是否同步cookie
    'syncIndexedDb': False,  # 是否同步indexedDB
    'syncBookmarks': True,  # 是否同步书签
    'syncAuthorization': False,  # 是否同步授权
    'syncHistory': True,  # 是否同步历史记录
    'isValidUsername': False,  # 是否验证用户名
    'workbench': 'localserver',
    'allowedSignin': True,  # 允许google账号登录浏览器，默认true
    'syncSessions': False,  # 同步浏览器Sessions，历史记录最近关闭的标签相关，默认false
    'clearCacheFilesBeforeLaunch': False,  # 启动前清理缓存文件，默认false
    'clearCookiesBeforeLaunch': False,  # 启动前清理cookie，默认false
    'clearHistoriesBeforeLaunch': False,  # 启动前清理历史记录，默认false
    'randomFingerprint': False,  # 是否启用随机指纹，默认false
    'disableGpu': False,  # 是否禁用GPU，默认false
    'enableBackgroundMode': False,  # 是否启用后台模式，默认false
    'muteAudio': True,  # 是否静音，默认True
}
fingerprint_config = {
    'coreVersion': '104',
    'ostype': 'Android',  # 操作系统平台 PC|Android|IOS
    'os': 'Win32',  # 为navigator.platform值 Win32 | Linux i686 | Linux armv7l | MacIntel，当ostype设置为IOS时，设置os为iPhone，ostype为Android时，设置为 Linux i686 || Linux armv7l
    'version': '',  # 浏览器版本
    'userAgent': '',
    'timeZone': '',  # 时区
    'timeZoneOffset': 0,  # 时区偏移量
    'isIpCreateTimeZone': True,  # 时区
    'webRTC': '0',  # webrtc 0|1|2
    'position': '1',  # 地理位置 0|1|2
    'isIpCreatePosition': True,  # 位置开关
    'lat': '',  # 经度
    'lng': '',  # 纬度
    'precisionData': '',  # 精度米
    'isIpCreateLanguage': False,  # 语言开关
    'languages': 'en-US',  # 默认系统
    'isIpCreateDisplayLanguage': False,  # 显示语言默认不跟随IP
    'displayLanguages': 'en-US',  # 默认系统
    'resolutionType': '0',  # 分辨
    'resolution': '',
    'fontType': '0',  # 字体生成类型
    'font': '',  # 字体
    'canvas': '0',  # canvas
    'canvasValue': None,  # canvas 噪音值 10000 - 1000000
    'webGL': '0',  # webGL
    'webGLValue': None,  # webGL 噪音值 10000 - 1000000
    'webGLMeta': '0',  # 元数据
    'webGLManufacturer': '',  # 厂商
    'webGLRender': '',  # 渲染
    'audioContext': '0',  # audioContext
    'audioContextValue': None,  # audioContext噪音值 1 - 100 ，关闭时默认10
    'mediaDevice': '0',  # mediaDevice
    'mediaDeviceValue': None,  # mediaDevice 噪音值，修改时再传回到服务端
    'speechVoices': '0',  # Speech Voices，默认随机
    'speechVoicesValue': None,  # peech Voices 值，修改时再传回到服务端
    'hardwareConcurrency': '4',  # 并发数
    'deviceMemory': '8',  # 设备内存
    'doNotTrack': '1',  # doNotTrack
    'portScanProtect': '',  # port
    'portWhiteList': '',
    'colorDepth': '32',
    'devicePixelRatio': '1.2',
    'openWidth': 1280,
    'openHeight': 1000,
    'ignoreHttpsErrors': True,  # 忽略https证书错误
    'clientRectNoiseEnabled': False,  # 默认关闭
    'clientRectNoiseValue': 0,  # 关闭为0，开启时随机 1 - 999999
    'deviceInfoEnabled': False,  # 设备信息，默认关闭
    'computerName': '',  # deviceInfoEnabled 为true时，设置
    'macAddr': ''  # deviceInfoEnabled 为true时，设置
}


class BitBrowser:

    def __init__(self, website):
        self.website = website  # 网站，用于浏览器窗口名称
        self.bit_port = self.get_bit_port()

    @classmethod
    def test_port(cls, port):
        url = f'http://127.0.0.1:{port}'
        try:
            res = requests.get(url, timeout=5)
            if res.status_code == 200:
                return True
        except:
            import traceback
            traceback.print_exc()
            return False

    @classmethod
    def get_bit_port(cls):
        # 获取比特浏览器的本地端口
        json_file = fr'C:\Users\{os.getlogin()}\AppData\Roaming\bitbrowser\config.json'
        if not os.path.exists(json_file):
            # 尝试枚举
            users = os.listdir('C:/Users')
            for user in users:
                x = fr'C:\Users\{user}\AppData\Roaming\bitbrowser\config.json'
                if os.path.exists(x):
                    json_file = x
                    break
            else:
                logger.error(f'请先安装比特浏览器:{json_file}')
                return False
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            bit_api = data['localServerAddress']
            cls.bit_port = bit_api.split(':')[-1]
            if cls.test_port(cls.bit_port):
                return cls.bit_port
            else:
                logger.error(f'请检查比特浏览器是否已经启动')
                return False

    def __request(self, endpoint, payload):
        """
        请求接口
        """
        endpoint = endpoint[1:] if endpoint.startswith('/') else endpoint
        api = f'http://127.0.0.1:{self.bit_port}/{endpoint}'
        res = None
        for _ in range(3):
            try:
                res = requests.post(api, json=payload, timeout=15)
                data = res.json()
                if data.get('success'):
                    return data
                else:
                    logger.error(f'endpoint: {endpoint} 请求结果: {data}')
                    time.sleep(3)
            except:
                if res:
                    logger.error(f'endpoint: {endpoint} 请求结果: {res.text}')
                else:
                    logger.error(
                        f'endpoint: {endpoint} 请求超时')
                time.sleep(3)
        return {}

    ##############################################浏览器接口#########################################################
    def create_driver(self, username='', password='', proxyType='noproxy', proxyIp='', proxyPort='', proxyUser='', proxyPassword='', **kwargs):
        """
        创建浏览器
        仅传入用户名、密码、代理
        """
        logger.info(f'创建/更新浏览器: username:{username}; password:{password}')
        # 浏览器对象
        remark = f'{username}----{password}'
        payload = payload_config.copy()
        payload['name'] = f'{self.website}:{username}'
        payload['remark'] = remark
        payload['proxyType'] = proxyType
        payload['host'] = proxyIp
        payload['port'] = proxyPort
        payload['proxyUserName'] = proxyUser
        payload['proxyPassword'] = proxyPassword
        if proxyType not in ['noproxy', 'http', 'https', 'socks5']:
            if 'rola' in proxyIp:
                ProxyType = 'rola'
            elif 'doveip' in proxyIp:
                ProxyType = 'doveip'
            elif 'cloudam' in proxyIp:
                ProxyType = 'cloudam'
            else:
                ProxyType = 'common'
            # 自定义提取代理
            payload['proxyType'] = 'socks5'
            payload['host'] = ''
            payload['port'] = ''
            payload['proxyMethod'] = 3
            payload['dynamicIpChannel'] = ProxyType
            payload['dynamicIpUrl'] = proxyIp

        # 指纹对象随机生成
        fingerprint = fingerprint_config.copy()
        fingerprint['version'] = str(random.randint(98, 106))
        fingerprint['computerName'] = f'Computer-{faker.first_name()}'
        fingerprint['macAddr'] = (
            '-'.join(['%02x' % faker.pyint(0, 255) for i in range(6)])).upper()
        # fingerprint['os'] = random.choice(
        #     ['Win32', 'Linux i686', 'Linux armv7l', 'MacIntel'])
        fingerprint['webGLManufacturer'] = random.choice(webgl_vendors)
        fingerprint['webGLRender'] = random.choice(webgl_renders)
        fingerprint['colorDepth'] = random.choice(color_depths)
        fingerprint['hardwareConcurrency'] = random.choice([2, 4, 6, 8])
        fingerprint['deviceMemory'] = random.choice([4, 8, 16, 32, 64])
        fingerprint['version'] = random.randint(100, 107)
        fingerprint['canvasValue'] = random.randint(10000, 1000000)
        fingerprint['webGLValue'] = random.randint(10000, 1000000)
        fingerprint['clientRectNoiseValue'] = random.randint(1, 999999)
        fingerprint['audioContextValue'] = random.randint(1, 100)
        fingerprint['mediaDeviceValue'] = random.randint(1, 100)
        fingerprint['speechVoicesValue'] = random.randint(1, 100)
        fingerprint['resolution'] = random.choice(
            ['1024 x 768', '1280 x 800', '1280 x 960', '1920 x 1080', '1440 x 900', '1280 x 1024'])
        fingerprint['openWidth'] = fingerprint['resolution'].split(' x ')[0]
        fingerprint['openHeight'] = fingerprint['resolution'].split(' x ')[1]

        # 从kwargs更新参数
        for k, v in kwargs.items():
            if fingerprint.get(k):
                fingerprint[k] = v
            if payload.get(k):
                payload[k] = v
        payload['browserFingerPrint'] = fingerprint

        # 查询是否已经创建过，如果已经创建过则保留原来的指纹
        driver = self.browser_list(username=username)
        if driver:
            payload['id'] = driver[0]['id']
            # 保留原来的分组
            if driver[0].get('groupId'):
                payload['groupId'] = driver[0]['groupId']
            # 保留原来的指纹
            browser_detail = self.browser_detail(driver[0]['id'])
            payload['browserFingerPrint'] = browser_detail['browserFingerPrint']

        data = self.__request('browser/update', payload)
        if data.get('success'):
            logger.info(f'创建浏览器成功，{username}')
            return data['data']['id']
        else:
            logger.error(f'创建浏览器失败，{username}')
            return False

    def open_browser(self, browser_id, loadExtensions=True, args=[], extractIp=True):
        """
        打开窗口
        """
        logger.info(f'打开窗口: {browser_id}')
        payload = {
            'id': browser_id,
            'loadExtensions': loadExtensions,
            'args': args,
            'extractIp': extractIp
        }
        data = self.__request('browser/open', payload)
        if data.get('success'):
            options = webdriver.ChromeOptions()
            ws_url = data['data']['http']
            options.add_experimental_option(
                'debuggerAddress', ws_url)
            options.arguments.extend(
                ["--no-default-browser-check", "--no-first-run"])
            options.arguments.extend(["--no-sandbox", "--test-type"])
            driver = webdriver.Chrome(options=options)
            # 随机位置
            x = random.randint(0, 500)
            y = random.randint(10, 200)
            driver.set_window_position(x, y)
            # 设置大小
            # driver.set_window_size(400, 1000)
            # 关闭其他页面，只保留一个
            try:
                while 1:
                    windows = driver.window_handles
                    if len(windows) > 1:
                        for idx, i in enumerate(windows):
                            if idx == len(windows)-1:
                                break
                            if i != driver.current_window_handle:
                                driver.switch_to.window(i)
                                driver.close()
                                driver.switch_to.window(windows[-1])
                    else:
                        break
            except:
                logger.error(f'关闭其他页面失败，重新打开：{browser_id}')
                time.sleep(5)
                return self.open_browser(browser_id)
            # 加载stealth.min.js
            if os.path.exists('./stealth.min.js'):
                with open('./stealth.min.js') as f:
                    js = f.read()
                driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                    "source": js
                })
            return driver
        else:
            logger.error(f'打开窗口失败: {browser_id}')
            return False

    def close_browser(self, browser_id):
        """
        关闭窗口
        """
        logger.info(f'关闭窗口{browser_id}')
        payload = {'id': browser_id}
        data = self.__request('browser/close', payload)
        if data.get('success'):
            logger.info(f'关闭窗口成功: {browser_id}')
            return True
        else:
            logger.error(f'关闭窗口失败: {browser_id}')
            return False

    def del_browser(self, browser_id):
        """
        删除窗口
        """
        logger.info(f'删除窗口{browser_id}')
        bit_api = f'http://127.0.0.1:{self.bit_port}'
        payload = {'id': browser_id}
        data = self.__request('browser/delete', payload)
        if data.get('success'):
            logger.info(f'删除窗口成功: {browser_id}')
            return True
        else:
            logger.error(f'删除窗口失败: {browser_id}')
            return False

    def browser_detail(self, browser_id):
        """
        获取窗口详情
        """
        logger.info(f'获取窗口详情{browser_id}')
        payload = {'id': browser_id}
        data = self.__request('browser/detail', payload)
        if data.get('success'):
            logger.info(f'获取窗口详情成功: {browser_id}')
            return data.get('data')
        else:
            logger.error(f'获取窗口详情失败: {browser_id}')
            return False

    def browser_list(self, page=0, pageSize=100, username: str = '', groupId=''):
        """
        查询窗口
        """
        logger.info(f'查询窗口: {username}')
        payload = {
            "page": page,
            "pageSize": pageSize,
        }
        if username != '':
            payload['name'] = f'{self.website}:{username}'
        if groupId != '':
            payload['groupId'] = groupId
        return self.__request('browser/list', payload).get('data', {'list': []}).get('list', [])

    def windowbounds(self, type: str = 'box', startX: int = 0, startY: int = 0, width: int = 500, height: int = 500, col: int = 3, spaceX: int = 0, spaceY: int = 0, offsetX: int = 0, offsetY: int = 0):
        """
        窗口排列
        : params:type: *排列方式，宫格 box ，对角线 diagonal
        : params:startX: *Int起始X位置，默认0
        : params:startY: *Int起始Y位置，默认0
        : params:width: *Int宽度，最小500
        : params:height: *Int高度，最小200
        : params:col: *Int宫格排列时，每行列数
        : params:spaceX: *Int宫格横向间距，默认0
        : params:spaceYInt宫格纵向间距，默认0: 
        : params:offsetX: *Int对角线横向偏移量
        : params:offsetY: *Int对角线纵向偏移量
        """
        if type not in ['box', 'diagonal']:
            logger.error('排列方式错误,自动选用box')
            type = 'box'
        if width < 500:
            logger.error('宽度最小500,自动设置为500')
            width = 500
        if height < 200:
            logger.error('高度最小200,自动设置为200')
            height = 200
        payload = {
            'type': type,
            'startX': startX,
            'startY': startY,
            'width': width,
            'height': height,
            'col': col,
            'spaceX': spaceX,
            'spaceY': spaceY,
            'offsetX': offsetX,
            'offsetY': offsetY
        }
        data = self.__request('windowbounds', payload)
        if data.get('success'):
            logger.info(f'窗口排列成功')
            return True
        else:
            logger.error(f'窗口排列失败')
            return False

    def update_browser_group(self, group_id, browser_ids):
        """
        更新窗口分组
        """
        logger.info(f'更新窗口分组{group_id}')
        payload = {
            'groupId': group_id,
            'browserIds': browser_ids
        }
        data = self.__request('browser/group/update', payload)
        if data.get('success'):
            logger.info(f'更新窗口分组成功: {group_id}')
            return True
        else:
            logger.error(f'更新窗口分组失败: {group_id}')
            return False

    def update_browser_proxy(self, browser_id, proxyType, proxyIp, proxyPort, proxyUser, proxyPass):
        """
        更新浏览器代理
        """
        logger.info(f'更新浏览器代理{browser_id}')
        payload = {
            "ids": [browser_id],
            "ipCheckService": "ip123",
            "proxyMethod": 2,
            "proxyType": proxyType,
            "host": proxyIp,
            "port": int(proxyPort) if proxyPort else "",
            "proxyUserName": proxyUser,
            "proxyPassword": proxyPass,
        }
        # 如果需要更新的代理为提取链接，那设置proxyType不在['noproxy', 'http', 'https', 'socks5']之中，proxyIp为提取链接
        if proxyType not in ['noproxy', 'http', 'https', 'socks5']:
            if 'rola' in proxyIp:
                ProxyType = 'rola'
            elif 'doveip' in proxyIp:
                ProxyType = 'doveip'
            elif 'cloudam' in proxyIp:
                ProxyType = 'cloudam'
            else:
                ProxyType = 'common'
            # 自定义提取代理
            payload['proxyType'] = 'socks5'
            payload['host'] = ''
            payload['port'] = ''
            payload['proxyUserName'] = ''
            payload['proxyPassword'] = ''
            payload['proxyMethod'] = 3
            payload['dynamicIpChannel'] = ProxyType
            payload['dynamicIpUrl'] = proxyIp
        data = self.__request('browser/proxy/update', payload)

        if data.get('success'):
            logger.info(f'更新浏览器代理成功: {browser_id}')
            return True
        else:
            logger.error(f'更新浏览器代理失败: {browser_id}')
            return False

    def update_browser_remark(self, browser_id: str, remark: str):
        """
        批量更新浏览器的备注
        """
        logger.info(f'更新浏览器的备注:{browser_id}->{remark}')
        payload = {
            'browserIds': [browser_id],
            'remark': remark
        }
        data = self.__request('browser/remark/update', payload)
        if data.get('success'):
            logger.info(f'批量更新浏览器的备注成功')
            return True
        else:
            logger.error(f'批量更新浏览器的备注失败')
            return False

    def batch_close_browser_by_seq(self, seqs: list):
        """
        批量通过序号关闭窗口
        """
        logger.info(f'批量通过序号关闭窗口')
        payload = {
            'seqs': seqs
        }
        data = self.__request('browser/close/byseqs', payload)
        if data.get('success'):
            logger.info(f'批量通过序号关闭窗口成功')
            return True
        else:
            logger.error(f'批量通过序号关闭窗口失败')
            return False

    ###################################################分组接口########################################################
    def add_group(self, group_name):
        """
        添加分组
        """
        logger.info(f'添加分组{group_name}')
        payload = {'groupName': group_name, 'sortNum': 1}
        data = self.__request('group/add', payload)
        if data.get('success'):
            logger.info(f'添加分组成功: {group_name}')
            return data['data']['id']
        else:
            logger.error(f'添加分组失败: {group_name}')
            return False

    def edit_group(self, group_id, group_name):
        """
        编辑分组
        """
        logger.info(f'编辑分组:{group_name}')
        payload = {'id': group_id, 'groupName': group_name, 'sortNum': 1}
        data = self.__request('group/edit', payload)
        if data.get('success'):
            logger.info(f'编辑分组成功: {group_name}')
            return True
        else:
            logger.error(f'编辑分组失败: {group_name}')
            return False

    def del_group(self, group_id):
        """
        删除分组
        """
        logger.info(f'删除分组:{group_id}')
        payload = {'id': group_id}
        data = self.__request('group/delete', payload)
        if data.get('success'):
            logger.info(f'删除分组成功: {group_id}')
            return True
        else:
            logger.error(f'删除分组失败: {group_id}')
            return False

    def group_list(self, page=0, pageSize=100):
        """
        查询分组列表，传入group_name则查询指定的分组
        """
        logger.info(f'查询分组列表')
        payload = {
            'page': page,
            'pageSize': pageSize
        }
        data = self.__request('group/list', payload)
        if data.get('success'):
            logger.info(f'查询分组列表成功')
            return data['data']['list']
        else:
            logger.error(f'查询分组列表失败')
            return []

    def group_detail(self, group_id):
        """
        查询分组详情
        """
        logger.info(f'查询分组详情')
        payload = {'id': group_id}
        data = self.__request('group/detail', payload)
        if data.get('success'):
            logger.info(f'查询分组详情成功')
            return data
        else:
            logger.error(f'查询分组详情失败')
            return False

    ###################################################自定义的一些方法########################################################
    def get_driver(self, username='', password='', proxyType='noproxy', proxyIp='', proxyPort='', proxyUsername='', proxyPassword='', **kwargs):
        """
        便捷创建并打开浏览器，返回driver对象和浏览器id
        """
        browser_id = self.create_driver(
            username, password, proxyType, proxyIp, proxyPort, proxyUsername, proxyPassword, **kwargs)
        if browser_id:
            driver = self.open_browser(browser_id)
            if driver:
                return driver, browser_id
            else:
                return False, browser_id
        else:
            return False, False

    def get_browser_info(self, browser_id, cols=['name']):
        """
        获取窗口信息
        :param browser_id: 窗口id
        :param cols: 需要获取的字段: name,remark,platform,platformIcon,proxyType,host,port,proxyUserName,proxyPassword,proxyMethod,agentId,cookie,userName,password,url,groupId,seq
        """
        logger.info(f'获取窗口信息:{browser_id}')
        detail = self.browser_detail(browser_id)
        if detail.get('success'):
            return {col: detail['data'].get(col, '') for col in cols}
        else:
            return False

    def update_browser_groupname(self, browser_id, group_name):
        """
        快速更新浏览器分组
        """
        logger.info(f'更新浏览器分组:{browser_id}->{group_name}')
        group_id = self.get_or_add_group(group_name)
        # 获取信息
        browser = self.browser_detail(browser_id)
        if browser:
            detail = browser['data']
            detail['groupId'] = group_id
            res = self.__request('browser/update', detail)
            if res.get('success'):
                logger.info(f'更新浏览器分组成功:{browser_id}->{group_name}')
                return True
            else:
                logger.error(f'更新浏览器分组失败:{browser_id}->{group_name}:{res}')
                return False
        else:
            logger.error(f'更新浏览器分组失败:{browser_id}->{group_name}:获取浏览器信息失败')
            return False

    def query_group_id(self, group_name):
        """
        查询指定分组存在不存在，如果存在，返回分组id
        """
        logger.info(f'查询指定分组:{group_name}')
        for _ in range(5):
            group_list = self.group_list(_)
            for group in group_list:
                if group['groupName'] == group_name:
                    group_id = group['id']
                    logger.info(f'查询指定分组成功:{group_name}')
                    return group_id
        else:
            logger.error(f'查询指定分组失败:{group_name}')
            return False

    def get_or_add_group(self, group_name):
        """
        获取或添加分组
        """
        logger.info(f'获取或添加分组:{group_name}')
        group_name = group_name.lower()
        group_id = self.query_group(group_name)
        if group_id:
            return group_id
        else:
            return self.add_group(group_name)

    def query_browser_group_name(self, browser_id):
        """
        查询浏览器分组名称
        """
        brow_detail = self.browser_detail(browser_id)
        group_id = brow_detail['data'].get('groupId', None)
        if group_id:
            group_detail = self.group_detail(group_id)
            group_name = group_detail['data']['groupName']
            return group_name
        else:
            return ''


if __name__ == '__main__':
    # 使用示例
    # 使用前，安装依赖：
    # pip install requests selenium faker loguru
    # 请自行将104版本的chromedriver.exe和脚本放同一个目录下

    website = 'twitter'  # 网站名称，创建浏览器和查询浏览器时需要用到
    # 创建对象
    bit = BitBrowser(website)
    # 创建并打开浏览器
    # 创建浏览器，必传参数：username,password,proxyType,proxyIp,proxyPort,proxyUsername,proxyPassword
    # 即：用户名，密码，代理类型，代理ip，代理端口，代理用户名，代理密码
    # - 其他参数可以通过kwargs传入，也可以不传
    # - 传入的代理类型，如果不是在['noproxy', 'http', 'https', 'socks5']中，默认为提取代理，脚本会设置proxyMethod=3, proxyIp为提取链接，传入dynamicIpUrl
    driver, browser_id = bit.get_driver(username=f'xxx', password='xxx', proxyType='noproxy',
                                        proxyIp='', proxyPort='', proxyUsername='', proxyPassword='', dynamicIpUrl='')
    driver.get('https://nowsecure.nl/')
    time.sleep(100)

    # 关闭浏览器
    bit.close_browser(browser_id)
    # # 删除浏览器
    bit.del_browser(browser_id)

    # from undetected_chromedriver import Chrome
    # driver = Chrome(version_main=107)
    # driver.get('https://pixelscan.net/')
    # time.sleep(100)
