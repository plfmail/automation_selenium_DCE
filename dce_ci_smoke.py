# coding=utf-8
import os
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from datetime import datetime
import logging
import random

# ServerAddr = os.environ.get('DCEADDR')
ServerAddr = '10.6.150.51'
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')  # 在虚机上跑
options.add_argument('--disable-gpu')
options.add_argument('--disable-features=VizDisplayCompositor')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-features=VizDisplayCompositor')
options.add_argument('lang=zh_CN.UTF-8')
# options.add_argument('--start-maximized')
options.add_argument('--disable-javascript')
TestWebDriver = webdriver.Chrome(options=options)

message2 =[]
allelement = {'login_username_loc': (By.XPATH, '//*[@class="login-page"]/div[2]/div[1]/div[1]/div[1]//input'),
              'login_password_loc': (By.XPATH, '//*[@class="login-page"]/div[2]/div[1]/div[1]/div[2]//input'),
              'login_submit_loc': (By.XPATH, '//*[@id="login"]//button[1]'),
              'sidebar_applist_loc': (By.XPATH, '//*[@id="app"]//menu//section[2]/menu/span'),
              'applist_loc_firstapp': (By.XPATH, '//*[@class="dao-table-view unselectable"]//tr[1]/td[1]/a'),
              'applist_createapp_loc': (By.XPATH, '//*[@class="dao-btn blue has-icon"]'),
              'applist_createapp_advancefuc_loc': (By.XPATH, '//*[@class="dao-radio-group"]/p/a'),
              'applist_createapp_createbyyaml_loc': (By.XPATH, '//*[@class="dao-radio-group"]/div[4]//input'),
              'applist_createapp_createbyimage_loc': (By.XPATH, '//*[@class="dao-radio-group"]/div[3]//input'),
              'applist_createapp_continue_create_loc': (By.XPATH, '//*[@class="dao-btn blue has-icon compact"]'),
              'applist_createappbyyml_app_name_loc': (By.XPATH, '//*[@class="dao-input-inner"]//input'),
              'applist_createappbyyml_try2048_loc': (By.XPATH, '//*[@class="dao-setting-section"]//a[1]'),
              'applist_createappbyyml_confirm_create_loc': (By.XPATH, '//*[@class="dao-steps"]/div[2]//button[1]'),
              'applist_createappbyimage_customedimage_loc': (By.XPATH, '//*[@class="nav-top lively"]/div[2]'),
              'applist_createappbyimage_imagename_loc': (
                  By.XPATH, '//*[@class="dao-setting-section"]//div[2]/div/div/div[1]/div/div/div/div[1]/input'),
              'applist_createappbyimage_checkaddr_loc': (By.XPATH, '/html/body/div[3]/div[2]/div/div/div[2]/button'),
              # 检验地址
              'applist_createappbyimage_continue_loc': (By.XPATH, '//*[@id="app"]/div[2]/div/div/div[2]/div/button[3]'),
              'applist_createappbyimage_auditapp_loc': (By.XPATH, '//*[@class="dao-btn green"]'),
              'applist_createappbyimage_confirm_loc': (
                  By.XPATH, '//*[@id="app"]/div[2]/div/div/div[2]/div/button[2]/span'),
              'appdetail_opentty_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[1]/button[1]'),
              'appdetail_changerc_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[1]/button[2]'),
              'appdetail_changeimg_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[1]/button[3]'),
              'appdetail_startdeployment_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[2]/button[1]'),
              'appdetail_stopdeployment_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[2]/button[2]'),
              'appdetail_restartdeployment_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[2]/button[3]'),
              'appdetail_setlabel_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[3]/button[1]'),
              # 应用详情前缀 appdetail
              'appdetail_toolbarconfig_loc': (By.XPATH, '//*[@class="dao-table-view-toolbar"]//span[3]/div'),
              'appdetail_assure_loc': (By.XPATH, '//*[@class="dao-dialog-footer"]//button[2]'),
              'appdetail_save_loc': (By.XPATH, '//*[@class="dao-dialog-backdrop alert-dialog"]//button[2]'),
              'appdetail_targetnum_loc': (By.XPATH, '//*[@class="dao-setting-section"]/div[1]/div[1]/div[1]/div[2]//input'),
              'appdetail_chooseversion_loc': (
                  By.XPATH, '//*[@class="dao-dialog-body"]/div[1]/div[2]/div[2]/div[1]/div/div[1]/div/div[1]'),
              'appdetail_versionsearch_loc': (By.XPATH, '//*[@class="search-container"]/input'),
              'appdetail_foundversion_loc': (By.XPATH, '//*[@class="dao-select-category"]/div[3]/span'),
              'appdetail_noty_loc': (By.XPATH, '//*[@class="noty_body"]'),
              'appdetail_managedeployment_assure_loc': (By.XPATH, '//*[@class="dao-dialog-footer"]//button[2]')
              }  # 登陆界面前缀login 侧边栏sidebar 应用列表界面applist 应用列表创建应用方式applist_createapp

logging.basicConfig(filename='../result/log.txt', filemode='w', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# 往html中输出日志
def html_log(message, level='info', content='text', filepath=''):
    if content == 'text':
        with open('../result/testhtml.html', 'w') as f:
            global message2
            message2.append(message)
            for i in message2:
                t = ''
                if i[0] == 'p':
                    t = t + '<img style="width="600px", height="400px"" src=%s>' % (i[4:])
                else:
                    t = t + '<p style="background-color:#21a5f3;">%s</p>' % (i)
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


class BasePage():
    def __init__(self):
        self.driver = TestWebDriver
        self.base_url = ServerAddr

    def _open(self, url):
        url = 'https://' + str(url)
        logger.info(url)
        self.driver.get(url)
        self.driver.set_window_size(1400, 1200)

    def open(self):
        self._open(self.base_url)

    def element_present(self, loc):
        return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(loc))

    def find_element(self, key):
        try:
            loc = allelement[key]
            element = self.element_present(loc)
            while element:
                return self.driver.find_element(*loc)
        except TimeoutException:
            logger.error('页面中未能找到{}元素'.format(key))

    def type(self, key, value):
        try:
            loc = allelement[key]
            element = self.element_present(loc)
            while element:
                return self.driver.find_element(*loc).send_keys(value)
        except TimeoutException:
            logger.error('{}元素不能传值'.format(key))

    def click_element(self, key):
        try:
            if type(key) == str:
                loc = allelement[key]
                WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(loc))
                return self.driver.find_element(*loc).click()
            else:
                return self.driver.find_element(*key).click()
        except TimeoutException:
            logger.error('{}元素不能点击'.format(key))

    def clearcontent(self, key):
        self.find_element(key).clear()

    def screenshot(self, image_name='test', num=[]):
        num.append(1)
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_path = "../result/image/" + image_name + str(len(num)) + '.png'
        html_log('pic ' + file_path)
        logger.info('save image to' + file_path)
        self.driver.get_screenshot_as_file(file_path)

    def action_result(self, testcase):
        testlist = {'login': (By.XPATH, '//*[@id="app"]/div[1]/nav/div[4]/div/ul/li[1]/a/span[1]'),
                    'create app': (By.XPATH, '//*[@class="header-name"]'),
                    'managedeployment': (By.XPATH, '//*[@class="noty_body"]')
                    }
        try:
            noty = testlist[testcase]
            element = self.element_present(noty)
            while element:
                return logger.info('[success]' + testcase)
        except TimeoutException:
            logger.error('[fail]' + testcase)

    def close(self):
        self.driver.close()


def test_login():  # 登陆
    logger.info('start login')
    login_page = BasePage()
    login_page.open()
    loginlist = {'login_username_loc': 'admin', 'login_password_loc': 'changeme'}
    for k, v in loginlist.items():
        login_page.type(k, v)
    login_page.click_element('login_submit_loc')
    sleep(2)
    login_page.action_result('login')
    login_page.screenshot('login')


def create_app_by_yml(app_name):  # 通过yml创建应用
    logger.info('start create app by yml')
    create_app_by_yml = BasePage()
    create_app_by_yml.click_element('sidebar_applist_loc')
    create_app_by_yml.click_element('applist_createapp_loc')
    sleep(1)
    create_app_by_yml.click_element('applist_createapp_advancefuc_loc')
    create_app_by_yml.click_element('applist_createapp_createbyyaml_loc')
    create_app_by_yml.click_element('applist_createapp_continue_create_loc')
    create_app_by_yml.type('applist_createappbyyml_app_name_loc', app_name)
    create_app_by_yml.click_element('applist_createappbyyml_try2048_loc')
    sleep(4)
    create_app_by_yml.click_element('applist_createappbyyml_confirm_create_loc')

def app_create():  # 创建应用
    logger.info('start create app by yml')
    html_log('start create app by yml')
    myapp = 'test' + str(random.randint(1, 1000))
    create_app = BasePage()
    create_app.click_element('sidebar_applist_loc')
    create_app_by_yml(myapp)
    create_app.action_result('create app')
    create_app.screenshot('createapp')


class AppDetailPage(BasePage):
    @property
    def double_assure(self):  # dce上的双重确认操作
        self.click_element('appdetail_assure_loc')
        self.click_element('appdetail_save_loc')

    def opentty(self):
        pass

    def changerc(self, num):  # 改变服务rc值
        logger.info('appdetail start change rc')
        html_log('appdetail start change rc')
        self.click_element('appdetail_changerc_loc')
        self.clearcontent('appdetail_targetnum_loc')
        self.type('appdetail_targetnum_loc', num)
        # self.click_element('assure_loc')
        # self.click_element('save_loc')
        self.double_assure
        self.action_result('appdetail_change rc', 'sign')
        self.screenshot('appdetail_managedeploy')

    def changeimg(self):  # 更改镜像
        logger.info('appdetail start change image')
        html_log('appdetail start change image')
        self.click_element('appdetail_changeimg_loc')
        sleep(2)
        self.click_element('appdetail_chooseversion_loc')
        self.type('appdetail_versionsearch_loc', 'v1.0.3')
        self.click_element('appdetail_foundversion_loc')
        self.double_assure
        self.action_result('appdetail_change image', 'sign')
        self.screenshot('appdetail_managedeploy')

    def managedeployment(self, mov):  # 启动/停止/重启服务
        logger.info('appdetail start ' + mov + ' deployment')
        html_log('appdetail start ' + mov + ' deployment')
        deployment_mov = {'start': (By.XPATH, '//*[@class="left"]//span[2]/button[1]'),
                          'stop': (By.XPATH, '//*[@class="left"]//span[2]/button[2]'),
                          'restart': (By.XPATH, '//*[@class="left"]//span[2]/button[3]')
                          }
        loc = deployment_mov[mov]
        self.click_element(loc)
        sleep(1)
        self.click_element((By.XPATH, '//*[@class="dao-dialog-footer"]//button[2]'))
        self.action_result('appdetail_' + mov + ' deployment', 'sign')

    def managelable(self, mov):  # 编辑标签
        pass

    def action_result(self, act, testcase):  # 页面自己的判断操作是否成功方法，覆盖base_element
        testlist = {
            'sign': (By.XPATH, '//*[@class="noty_body"]')
        }
        noty = testlist[testcase]
        try:
            element = self.element_present(noty)
            while element:
                html_log('[success]' + act)
                return logger.info('[success]' + act)
        except TimeoutException:
            html_log('[fail]' + act)
            return logger.error('[fail]' + act)


if __name__ == '__main__':
    integratedapp = AppDetailPage()
    logger.info('start manage app')
    html_log('start manage app')
    test_login()
    # app_create()
    # sleep(2)
    # integratedapp.changerc(2)
    # sleep(1)
    # integratedapp.changeimg()
    # sleep(1)
    # list = ['restart', 'stop']
    # for i in list:
    #     integratedapp.managedeployment(i)
    #     sleep(5)
    integratedapp.close()
