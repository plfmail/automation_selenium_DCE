# coding=utf-8
import os
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import logging
import subprocess
import yaml
from datetime import datetime
from time import sleep


ServerAddr = 'https://10.6.153.100'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')  #Bypass OS security model
options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument("--remote-debugging-port=9515")
# options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')  #overcome limited resource problems
# options.add_argument('--start-maximized')
options.add_argument('--disable-javascript')
TestWebDriver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
TestWebDriver.page_source.encode('utf-8')

# 从元素位置文件中读取元素xpath
with open('ci_base_element_loc.txt', 'r',encoding="utf-8") as f:
    origin = f.read()
    slice = origin.split('\n')
    # print(len(slice))
    allelement = {}
    i = 0
    while i < len(slice):
        if len(slice[i]) > 0 and slice[i][0] != '#' :
            w = slice[i].split(':')[1].split(',')[0]
            allelement[str(slice[i].split(':')[0])] = w[1:]
        i = i + 1

# logging.basicConfig(filename='./log.txt',filemode='w',level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
# formatter = logging.Formatter(fmt="%(asctime)s %(filename)s[line:%(lineno)d]%(levelname)s - %(message)s",
#                                   datefmt="%m/%d/%Y %I:%M:%S %p")
# console = logging.StreamHandler()
# console.setLevel(logging.WARNING)
# console.setFormatter(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logger.addHandler(console)
message2 =[]

# 往html中输出日志
def html_log(message, level='info', content='text', filepath=''):
    if content == 'text':
        # logger = logging.getLogger(__name__)
        # logger.level = level
        with open('../result/testhtml.html', 'w') as f:
            global message2
            message2.append(message)
            for i in message2:
                t = ''
                kind = i.split('-')[3]
                try:
                    if kind == ' pic ':
                        t = t + '<img style="width:600px; height:400px" src=%s>' % (i.split('pic - ')[1])
                    elif kind == ' case ':
                        t = t + '<p><h1 style="background-color:#14a0e0;">%s</h1></p>' % (i)
                    elif kind == ' success ':
                        t = t + '<p><h2 style="background-color:green;">%s</h2></p>' % (i)
                    elif kind == ' fail ':
                        t = t + '<p><h2 style="background-color:red;">%s</h2></p>' % (i)
                    elif kind == ' error ':
                        t = t + '<p><h3 style="background-color:red;">%s</h3></p>' % (i)
                    elif kind == ' info ':
                        t = t + '<p><h3 style="background-color:yellow;">%s</h3></p>' % (i)
                except:
                    kind = 'unknow kind'
                    t = t + '<p><h2 style="background-color:red;">%s</h2></p>' % (i + kind)
                base = """
                <html>
                <head></head>
                <body>
                %s
                </body> 
                </html>""" % (t)
                f.write(base)
    if content == 'image':
        pass


def event_log(mes_kind, mes):
    logger.info('[' + mes_kind + '] ' + mes)
    html_log('{} - '.format(datetime.now()) + mes_kind + ' - ' + mes)

# 定义BasePage类，包含open、find_element、click、element_visible等方法，被所有页面继承
# 元素定位全部使用xpath，在element_loc 定义过的元素，传参类型为字符串
# 在element_loc 中没有定义的元素，在具体页面进行了定义，传参类型为元组
class BasePage():

    def __init__(self):
        self.driver = TestWebDriver
        self.base_url = ServerAddr

    # def on_page(self):
    #     return pagetitle in driver.dr.title  # 根据传过来的pagetitle判断是否在正确界面

    def _open(self, url):
        self.driver.get(url)
        self.driver.set_window_size(1300, 1000)

    def open(self):
        # self._open(self.base_url,self.pagetitle)
        self._open(self.base_url)

    def element_present(self, loc):
        loc = (By.XPATH, loc)
        # return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc))
        while not WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc)):
            sleep(2)
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc))
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc))

    def element_clickable(self, loc):
        loc = (By.XPATH, loc)
        return WebDriverWait(self.driver,10).until(EC.element_to_be_clickable(loc))

    def find_element(self, key):
        try:
            loc = allelement[key]
            element = self.element_present(loc)
            while element:
                logger.debug('已定位到{}元素'.format(key))
                return self.driver.find_element(By.XPATH, loc)
        # except TimeoutException:
        except:
            self.screenshot('{}finderror'.format(key))
            return event_log('error','页面中未能找到{}元素'.format(key))

    def type(self, key, value):
        try:
            loc = allelement[key]
            element = self.element_present(loc)
            while element:
                logger.debug('{}元素传值成功'.format(key))
                return self.driver.find_element(By.XPATH, loc).send_keys(value)
        # except TimeoutException:
        except:
            self.screenshot('{}typeerror'.format(key))
            return event_log('error','{}元素不能传值'.format(key))

    def click_element(self, key):
        try:
            if type(key) == str:
                loc = allelement[key]
                element = self.element_clickable(loc)
                while element:
                    logger.debug('{}元素点击成功'.format(key))
                    return self.driver.find_element(By.XPATH, loc).click()
            # else:
            #     return self.driver.find_element(*key).click()
        # except TimeoutException:
        except:
            self.screenshot('{}clickerror'.format(key))
            return event_log('error','{}元素不能点击'.format(key))

    def move_element(self,key):
        pos = self.find_element(key)
        return ActionChains(self.driver).move_to_element(pos).perform()

    def double_click(self,key):
        pos = self.find_element(key)
        return ActionChains(self.driver).double_click(pos).perform()

    def get_url(self):
        current_url = self.driver.current_url
        print(current_url)
        url = current_url.split('/')[3:]
        title = ''
        for i in url:
            title = title + i
        event_log('info','current_page_url: ' + title)
        return self.driver.current_url

    def get_cookie(self):
        return self.driver.get_cookies()

    def get_handle(self):
        all_handles = self.driver.window_handles
        # print(all_handles)
        return all_handles

    def switch_win(self,handle):
        return self.driver.switch_to.window(handle)

    def clearcontent(self, key):
        self.find_element(key).clear()

    def screenshot(self, image_name='test', num=[]):
        num.append(1)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = base_dir + "/result/image/" + image_name + str(len(num)) + '.png'
        logger.debug('产生截图 ' + file_path)    #命令行截图输出设定为debug级别
        event_log('pic',file_path)
        self.driver.get_screenshot_as_file(file_path)

    def action_result(self, testcase):
        testlist = {'login': '//*[@id="app"]/div[1]/nav/div[3]/div/ul/li[1]/a/span[1]',
                    'create app': '//*[@class="header-name"]',
                    'managedeployment': '//*[@class="noty_body"]'
                    }
        try:
            noty = testlist[testcase]
            element = self.element_present(noty)
            while element:
                # return
                logger.info('[success] ' + testcase)
                return html_log('{} - success - '.format(datetime.now()) + testcase)
        except TimeoutException:
            logger.info('[fail] ' + testcase)
            return html_log('{} - fail - '.format(datetime.now()) + testcase)

    def get_hostcmd_output(self,cmd):
        with open('process.yaml', 'w') as q:
            d = subprocess.getoutput(
                'nsenter --mount=/host/proc/1/ns/mnt -n/host/proc/1/ns/net kubectl get deployment test246-2048 -o yaml')
            q.write(d)
        with open('process.yaml', 'r') as q:
            dic = yaml.load(q, Loader=yaml.FullLoader)
            print(dic)
            print(type(dic))
            print(dic['spec']['template']['spec']['containers'][0]['image'])
            print(type(dic['spec']))

    def get_hostcmd(self,cmd):
        return subprocess.getoutput(
            'nsenter --mount=/host/proc/1/ns/mnt -n/host/proc/1/ns/net ' + cmd)

    def close(self):
        self.driver.close()

    # 名称被占用
    @property
    def whennamealreadytoken(self):  # dce名称重复告警不统一
        alreadytoken = self.driver.find_element(By.XPATH,
                                                '//*[@id="app"]/div[2]/div/div/div[1]/div/div[2]/div[2]/div[1]/div[3]/div/div[2]/div/div/span/svg')


if __name__ == '__main__':
    test = webdriver.Chrome()
