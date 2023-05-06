import random
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

from bs4 import BeautifulSoup
import requests
import os
import random
import mailparser
import re
import time
from log import get_log
import psutil

log = get_log(__name__)
class RegisterAc:
    host = "imap-mail.outlook.com"
    def __init__(self,ac,proxy,url,new_time):
            self.url = url
            self.proxy = proxy
            self.new_time = new_time
            temp = ac.split(";")
            self.id = int(temp[0])
            self.email = temp[1]
            self.email_pwd = temp[2]
            self.name = temp[3] if temp[3].replace(" ",'') != '' else self.generate_string(12)
            self.pwd = temp[4] if temp[4].replace(" ",'') != '' else self.generate_string(12)
        
            self.web_id = temp[5] if temp[5].replace(" ",'') != '' else self.create_web()
            self.stauts = temp[6]


    # 生成随机字符串
    def generate_string(self,len):
        import string
        # 生成由数字和字母组成的密码
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(len))
        # 检查密码中是否包含数字和字母
        if not any(char.isdigit() for char in password):
            password = password[:-1] + random.choice(string.digits)
        if not any(char.isalpha() for char in password):
            password = password[:-1] + random.choice(string.ascii_letters)
        return password

    # 创建指纹浏览器
    def create_web(self):

        headers = {
                'platform': '',  # 账号平台
                'platformIcon': 'other',  # 取账号平台的 hostname 或者设置为other
                'url': '',  # 打开的url，多个用,分开
                'name': self.email,  # 窗口名称
                'remark': '',  # 备注
                'userName': '',  # 用户账号
                'password': '',  # 用户密码
                'cookie': '',  # cookie
                'proxyMethod': 2,  # 代理类型 1平台 2自定义
                'proxyType': 'noproxy',  # 自定义代理类型 ['noproxy', 'http', 'https', 'socks5', '911s5']

                'proxyUserName': '',  # 代理账号
                'proxyPassword': '',  # 代理密码
                "browserFingerPrint": {
                    'coreVersion': '104',  # 内核版本，默认104，可选92
                    'ostype': 'Android',  # 操作系统平台 PC | Android | IOS
                    'os': 'Linux i686',  # 为navigator.platform值 Win32 | Linux i686 | Linux armv7l | MacIntel，当ostype设置为IOS时，设置os为iPhone，ostype为Android时，设置为 Linux i686 | | Linux armv7l
                    'version': '',  # 浏览器版本，建议92以上，不填则会从92以上版本随机
                    'userAgent': '',  # ua，不填则自动生成
                    'isIpCreateTimeZone': True,  # 基于IP生成对应的时区
                    'timeZone': '',  # 时区，isIpCreateTimeZone 为false时，参考附录中的时区列表
                    'timeZoneOffset': 0,  # isIpCreateTimeZone 为false时设置，时区偏移量
                    'webRTC': '0',  # webrtc 0替换 | 1允许 | 2禁止
                    'ignoreHttpsErrors': False,  # 忽略https证书错误，true | false
                    'position': '1',  # 地理位置 0询问 | 1允许 | 2禁止
                    'isIpCreatePosition': True,  # 是否基于IP生成对应的地理位置
                    'lat': '',  # 经度 isIpCreatePosition 为false时设置
                    'lng': '',  # 纬度 isIpCreatePosition 为false时设置
                    'precisionData': '',  # 精度米 isIpCreatePosition 为false时设置
                    'isIpCreateLanguage': True,  # 是否基于IP生成对应国家的浏览器语言
                    'languages': '',  # isIpCreateLanguage 为false时设置，值参考附录
                    'isIpCreateDisplayLanguage': False,  # 是否基于IP生成对应国家的浏览器界面语言
                    'displayLanguages': '',  # isIpCreateDisplayLanguage 为false时设置，默认为空，即跟随系统，值参考附录
                    'openWidth': 500,  # 窗口宽度
                    'openHeight': 950,  # 窗口高度
                    'resolutionType': '1',  # 分辨率类型 0跟随电脑 | 1自定义
                    'resolution': '360 x 748',  # 自定义分辨率时，具体值
                    'windowSizeLimit': True,  # 分辨率类型为自定义，且ostype为PC时，此项有效，约束窗口最大尺寸不超过分辨率
                    'devicePixelRatio': 1,  # 显示缩放比例，默认1，填写时，建议 1｜1.5 | 2 | 2.5 | 3
                    'fontType': '2',  # 字体生成类型 0系统默认 | 1自定义 | 2随机匹配
                    'font': '',  # 自定义或随机匹配时，设置的字体值，值参考附录字体
                    'canvas': '0',  # canvas 0随机｜1关闭
                    'canvasValue': None,  # canvas为0随机时设置， 噪音值 10000 - 1000000
                    'webGL': '0',  # webGL图像，0随机｜1关闭
                    'webGLValue': None,  # webGL为0时，随机噪音值 10000 - 1000000
                    'webGLMeta': '0',  # webgl元数据 0自定义｜1关闭
                    'webGLManufacturer': '',  # webGLMeta 自定义时，webGL厂商值，参考附录
                    'webGLRender': '',  # webGLMeta自定义时，webGL渲染值，参考附录
                    'audioContext': '0',  # audioContext值，0随机｜1关闭
                    'audioContextValue': None,  # audioContext为随机时，噪音值， 1 - 100 ，关闭时默认10
                    'mediaDevice': '0',  # 媒体设备信息，0自定义｜1关闭
                    'mediaDeviceValue': None,  # mediaDevice 噪音值，不填则由系统生成，填值时，参考附录
                    'speechVoices': '0',  # Speech Voices，0随机｜1关闭
                    'speechVoicesValue': None,  # speechVoices为0时，随机时由系统自动生成，自定义时，参考附录
                    'hardwareConcurrency': '4',  # 硬件并发数
                    'deviceMemory': '8',  # 设备内存
                    'doNotTrack': '1',  # doNotTrack 0开启｜1关闭
                    # ClientRects true使用相匹配的值代替您真实的ClientRects | false每个浏览器使用当前电脑默认的ClientRects
                    'clientRectNoiseEnabled': True,
                    'clientRectNoiseValue': 0,  # clientRectNoiseEnabled开启时随机，值 1 - 999999
                    'portScanProtect': '0',  # 端口扫描保护 0开启｜1关闭
                    'portWhiteList': '',  # 端口扫描保护开启时的白名单，逗号分隔
                    'colorDepth': '24',  # 颜色深度
                    'deviceInfoEnabled': True,  # 自定义设备信息，默认开启
                    'computerName': '',  # deviceInfoEnabled 为true时，设置
                    'macAddr': '',  # deviceInfoEnabled 为true时，设置
                    # ssl是否禁用特性，默认不禁用，注意开启后自定义设置时，有可能会导致某些网站无法访问
                    'disableSslCipherSuitesFlag': False,
                    'disableSslCipherSuites': None,  # ssl 禁用特性，序列化的ssl特性值，参考附录
                    'enablePlugins': False,  # 是否启用插件指纹
                    'plugins': ''  # enablePlugins为true时，序列化的插件值，插件指纹值参考附录
                }
            }
        s = requests.session()
        try:
            a = s.post(f"{self.url}/browser/update", json=headers).json()
            b = a['data']['id']
            return b
        except:
            self.pane.update_table(self.pane.ac_table,self.id,5,"创建异常")
            log.error("创建指纹浏览器异常")
            return ""

    #打开指纹浏览器
    def open_web(self):
        if self.web_id != "":
            # headers = {'id': f'{self.web_id}','loadExtensions':True,'args':['--headless']}
            headers = {'id': f'{self.web_id}','loadExtensions':True}
            s = requests.session()
            a = s.post(f"{self.url}/browser/open", json=headers).json()
            web_http = a['data']['http']
            chrome_options = Options()
            try:
                chrome_options.add_experimental_option("debuggerAddress", web_http)
                driver = Chrome(executable_path=os.getcwd() + "/assets/chromedriver.exe", chrome_options=chrome_options)
                driver.set_page_load_timeout(10)
                # driver.set_window_size(1280,1280)
                # driver.set_window_position(random.randint(0, 20) * 20, random.randint(0, 20) * 20)
                # driver.switch_to.window(driver.window_handles[1])
                return driver
            except Exception as e:
                log.error(e)
                return False
        log.error("self.web_id 为空")
        return False

    # 关闭指纹浏览器
    def close_web(self):
        headers = {'id': f'{self.web_id}'}
        s = requests.session()
        s.post(f"{self.url}/browser/close", json=headers).json()

    # 获取浏览器详情
    def detail_wen(self):
        headers = {'id': f'{self.web_id}'}
        s = requests.session()
        dada_json = s.post(f"{self.url}/browser/detail", json=headers).json()
        self.browserFingerPrint = dada_json['data']['browserFingerPrint']
        self.lastIp = dada_json['data']['lastIp']


    # 删除浏览器
    def del_web(self):
        headers = {'ids': [f'{self.web_id}']}
        s = requests.session()
        data = s.post(f"{self.url}/browser/delete/ids", json=headers).json()




    # 注册步骤
    def start_register(self):
        try:
            self.driver = self.open_web()
            if not self.driver:
                self.pane.update_table(self.pane.ac_table,self.id,5,"打开异常")
                log.error("打开指纹浏览器异常")
                self.save("失败")
                return 
            
            
            self.driver.get("https://accounts.kakao.com/weblogin/create_account/?app_type=web&continue=https%3A%2F%2Faccounts.kakao.com%2Fweblogin%2Faccount&lang=ko#selectVerifyMethod")
            wait = WebDriverWait(self.driver, 10, 1)
            time.sleep(3)
            print("a1")
            print("a2")
            btn_g = self.wait_for_element(By.CSS_SELECTOR, ".btn_g.highlight.submit")

            btn_g.click()

        except Exception as e:
 
            log.error(e)
            self.save("失败") 

    # 获取邮箱验证码
    def email_code(self,n =0):
        try:
            if n > 2:
                log.error("没有获取到验证码")
                return '没获取到验证码'
            from imapclient import IMAPClient
            with IMAPClient(self.host) as server:
                server.login(self.email, self.email_pwd)
                server.select_folder('INBOX')
                messages = server.search(['FROM', 'noreply@kakaocorp.com'])  # in your case: ['FROM', 'email@outlook.example']
                code_list = []
                for uid, message_data in server.fetch(messages, 'RFC822').items():
                    email_message = mailparser.parse_from_bytes(message_data[b'RFC822'])
                    soup = BeautifulSoup(email_message.body, "html.parser")
                    msg_body = soup.get_text()
                    s = re.findall(r"\d{8}", str(msg_body).replace("\n",''))[0]
                    code_list.append(s)
                print(code_list[-1])
                return code_list[-1]
        except Exception as e:
            print(e)
            time.sleep(3)
            n +=1
            return self.email_code(n=n)

    # 打识别
    def verify_code(self):
        print("进入打码")
        # 切换到勾选框
        try:
            iframe = self.driver.find_element_by_css_selector('iframe[src*="anchor"]')
        except:
            return True
        self.driver.switch_to.frame(iframe)
        # 获取勾选框的打勾状态
        for i in range(30):
            anchor = self.driver.find_element_by_id('recaptcha-anchor')
            is_checked = anchor.get_attribute("aria-checked")
            print(is_checked)
            if is_checked != "false":               
                return True
            time.sleep(3)
        return False

    def save(self,name):
        self.detail_wen()
        path = os.getcwd()+ "/{}{}.txt".format(name,self.new_time)
        note1 = open(path,mode="a+",encoding="UTF-8")
        ac = "{0};{1};{2};{3};{4};{5}".format(self.email,self.email_pwd,self.name,self.pwd,self.lastIp,self.browserFingerPrint)
        note1.write(ac+"\n")
        note1.close()


    def wait_for_element(self, by=By.ID, value=None, max_attempts=3):
        """每3秒检查一次元素是否存在，最多尝试max_attempts次。"""
        attempts = 0
        while attempts < max_attempts:
            try:
                element = self.driver.find_element(by,value)
                return element
            except NoSuchElementException:
                attempts += 1
                print("重新获取元素，",value)
                time.sleep(3)
        raise NoSuchElementException(f"无法找到元素：{value}")


    def mytouch(self,element):
        # 模拟单击操作
        actions = ActionChains(self.driver)
        actions.click(element).perform()

# 获取指纹浏览器使用端口
def get_url():
    url = "http://127.0.0.1:"
    for proc in psutil.process_iter():
        if proc.name() == '比特浏览器.exe':
            for x in proc.connections():
                if x.status == psutil.CONN_LISTEN:
                    url = url + str(x.laddr.port)
                    return url
    return None




if __name__ == "__main__":
        ac = "1;a;a;;;;;"
        proxy = {
            "http":"127.0.0.1:2801",
            "https":"127.0.0.1:2801"
        }
        web_url = get_url()
        new_time=""
        register_ac = RegisterAc(ac,proxy,web_url,new_time)
        register_ac.start_register()
        register_ac.close_web()
        register_ac.del_web()