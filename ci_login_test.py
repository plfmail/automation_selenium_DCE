from time import sleep
from ci_base import BasePage
from ci_base import event_log

class Login(BasePage):
    def login(self,username,password):  # 登陆
        self.open()
        loginlist = {'login_username_loc': username, 'login_password_loc': password}
        for k, v in loginlist.items():
            self.type(k, v)
        self.click_element('login_submit_loc')

def login_test(username,password):
    login_test = Login()
    event_log('case', 'start login')
    login_test.login(username,password)
    login_test.get_url()
    login_test.action_result('login')
    login_test.screenshot('login')


if __name__ == '__main__':
    login_test('admin','changeme')
    sleep(1)
    #test1
