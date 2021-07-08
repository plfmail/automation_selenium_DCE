# coding=utf-8
from ci_base import BasePage
from ci_base import event_log
from ci_login_test import login_test
from time import sleep
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import random


class AppCreatePage(BasePage):
    def Create_App_by_Yml(self, app_name):  # 通过yml创建应用
        self.click_element('sidebar_applist_loc')
        self.click_element('applist_createapp_loc')
        sleep(1)
        self.click_element('applist_advancefuc_loc')
        self.click_element('applist_create_by_yaml_loc')
        self.click_element('applist_continue_create_loc')
        self.type('applist_createappbyyml_appname_loc', app_name)
        self.click_element('applist_createappbyyml_try2048_loc')
        sleep(4)
        self.click_element('applist_createappbyyml_confirmcreate_loc')
        # sleep(1)

    def Create_App_throughImage(self,image_addr,app_name):  # 通过镜像创建应用
        self.click_element('sidebar_applist_loc')
        self.click_element('applist_createapp_loc')
        self.click_element('applist_create_by_image_loc')
        self.click_element('applist_continue_create_loc')
        self.click_element('applist_createappbyimage_customizeimage_loc')
        self.type('applist_createappbyimage_customizeimage_imagename_loc',image_addr)
        self.click_element('applist_createappbyimage_customizeimage_ensureaddr_loc')
        sleep(2)
        self.click_element('applist_createappbyimage_continue_loc')
        self.clearcontent('applist_createappbyimage_appname_loc')
        self.type('applist_createappbyimage_appname_loc',app_name)
        sleep(1)
        self.click_element('applist_createappbyimage_continue_loc')
        self.click_element('applist_createappbyimage_continue_loc')
        self.click_element('applist_createappbyimage_continue_loc')
        self.click_element('applist_createappbyimage_auditapp_loc')
        self.click_element('applist_createappbyimage_deployapp_loc')

    def create_app_action_result(self,appname):
        try:
            noty = '//*[@class="header-name"]'
            element = self.element_present(noty)
            cmd = 'kubectl get app | grep ' + appname
            appresource = self.get_hostcmd(cmd)
            print(appresource)
            if appname in appresource:
                sign2 = False
            print(sign2)
            print('666')
            print(element)
            while element and sign2:
                return event_log('{} - success - '.format(datetime.now()),'createapp success')
            return event_log('{} - fail - '.format(datetime.now()), 'createapp fail')
        except TimeoutException:
            return event_log('{} - fail - '.format(datetime.now()),'createapp fail')


if __name__ == '__main__':
    login_test('admin','changeme')
    app_name = 'autobyyaml' + str(random.randint(1, 1000))
    create_app_byyaml = AppCreatePage()
    event_log('case','create app by yaml')
    create_app_byyaml.Create_App_by_Yml(app_name)
    sleep(2)
    create_app_byyaml.create_app_action_result(app_name)
    create_app_byyaml.screenshot('create_app_byyaml')
    #test1