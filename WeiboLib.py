#!/usr/local/bin/python
#coding = utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from WebDriverLib import WebDriverLib


class WeiboLib:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverLib(driver)
        self.login_url = 'https://passport.weibo.cn/signin/login'
        self.post_url = 'http://m.weibo.cn/mblog'
        self.search_url = 'http://m.weibo.cn/searchs'

    def Login(self, user, passwd):
        try:
            print "Login with",user,":",passwd
            self.driver.get(self.login_url)
            elem_user = self.wait.waitToVisible((By.ID,"loginName"))
            elem_user.send_keys(user)
            elem_pwd = self.wait.waitToVisible((By.ID,"loginPassword"))
            elem_pwd.send_keys(passwd)
            elem_pwd.send_keys(Keys.RETURN)
            self.wait.waitToLeave((By.ID,"loginAction"))
            print 'Current:',self.driver.current_url
            print 'Cookies:'
            print self.driver.get_cookies()
            # for cookie in driver.get_cookies():
            #     for key in cookie:
            #         print key, cookie[key]

            print 'Login Success'
        except Exception,e:
            print "Something Wrong When Login", e
        finally:
            print "Login End."

    def Post(self, msg):
        try:
            self.driver.get(self.post_url)
            print 'Loading post page...'
            btn_send = self.driver.find_element(By.XPATH,"//a[@data-node='send']")
            if (btn_send != None):
                print 'Ready to post'
                text_content = self.driver.find_element(By.ID, "txt-publisher")
                assert text_content, not None
                text_content.send_keys(msg)
                time.sleep(1)
                btn_send.click()
            else:
                print 'Not logged in yet'
        except Exception,e:
            print 'Something Wrong When Post',e
        finally:
            print 'Post End'

    def PostWithPic(self, msg, path):
        try:
            self.driver.get(self.post_url)
            print 'Loading post page...'
            btn_send = self.driver.find_element(By.XPATH,"//a[@data-node='send']")
            if (btn_send != None):
                print 'Ready to post'
                text_content = self.driver.find_element(By.ID, "txt-publisher")
                pic_upload = self.driver.find_element(By.CLASS_NAME, "picupload")
                assert text_content, not None
                text_content.send_keys(msg)
                if (pic_upload != None):
                    print 'Uploading path ',path
                    pic_upload.send_keys(path)
                else:
                    print 'Pic btn not found'
                time.sleep(1)
                btn_send.click()
            else:
                print 'Not logged in yet'
        except Exception,e:
            print 'Something Wrong When Post',e
        finally:
            print 'Post End'

if __name__ == "__main__":
    user = "2509335746@qq.com"
    passwd = "lixindong14tc"

    from selenium import webdriver
    driver = webdriver.Chrome()
    weibo = WeiboLib(driver)
    weibo.Login(user, passwd)
    weibo.PostWithPic(u'#RIO# is so amazing!!\n --' + str(time.time()), '/Users/lixindong/Documents/avatar.jpg')
    # time.sleep(20)
    # driver.close()
