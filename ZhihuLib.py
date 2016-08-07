#!/usr/local/bin/python
#coding = utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
import os

from WebDriverLib import WebDriverLib


class ZhihuLib:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverLib(driver)
        self.SEARCH_BASE_URL = 'https://www.zhihu.com/search'
        self.article_list = []
        self.question_list = []

    def get_search_url(self, q='', type='content', sort='upvote'):
        return self.SEARCH_BASE_URL + '?q=' + q + '&type=' + type + '&sort=' + sort

    def get_load_more(self):
        result = None
        try:
            result = self.wait.waitToVisible((By.XPATH, "//a[@class='zg-btn-white zu-button-more']"))
        except Exception, e:
            print 'get load more error',e
        finally:
            return result

    def get_li_list(self):
        list = []
        try:
            ul = self.driver.find_element(By.XPATH, "//ul[@class='list contents navigable']")
            list = ul.find_elements_by_xpath(".//li")
            for li in list:
                if li.get_attribute('class').find('answer-item') >= 0:
                    list.remove(li)
        except Exception, e:
            print 'get li list wrong ', e
        finally:
            return list

    def get_last_zan_count(self):
        zan_count = 0
        try:
            li_list = self.get_li_list()
            last_li = li_list[len(li_list)-1]
            zan = last_li.find_element(By.XPATH,
                                       ".//a[@class='zm-item-vote-count hidden-expanded js-expand js-vote-count']")
            print 'zan count html:', zan.get_attribute('innerHTML')
            if zan.text == "":
                zan_count = int(zan.get_attribute('innerHTML'))
            else:
                zan_count = int(zan.text)
        except Exception,e:
            print 'get last zan count error', e
        finally:
            print 'get last zan count finished', str(zan_count)
            return zan_count

    def get_zan_count(self, li):
        zan_count = 0
        try:
            zan = li.find_element(By.XPATH,
                                       ".//a[@class='zm-item-vote-count hidden-expanded js-expand js-vote-count']")
            print 'zan count html:', zan.get_attribute('innerHTML')
            if zan.text == "":
                zan_count = int(zan.get_attribute('innerHTML'))
            else:
                zan_count = int(zan.text)
        except Exception, e:
            print 'get zan count error', e
        finally:
            return zan_count

    def load_more_until_zan(self, count):
        try:
            print 'len', len(self.get_li_list())
            zan_count = self.get_last_zan_count()
            print zan_count
            while True:
                load_more = self.get_load_more()
                zan_count = self.get_last_zan_count()
                print 'zan count ', str(zan_count)
                if zan_count > count:
                    load_more.click()
                else:
                    break

        except Exception,e:
            print 'load_more_until_zan something\'s wrong', e
        finally:
            print 'load more finished'

    def save_article_question_list(self, count):
        li_list = self.get_li_list()
        print 'load more End, len is ',str(len(li_list))
        # foreach li
        # if zan > 100
        #    if article:
        #       put in article list
        #    if question:
        #       put int question list
        # save list to local
        for li in li_list:
            print li.get_attribute('class')
            if self.get_zan_count(li) > count:
                cls = li.get_attribute('class')
                if cls.find('article-item') >= 0:
                    self.article_list.append(li)
                else:
                    self.question_list.append(li)

        print 'article list', self.article_list
        print 'question list', self.question_list


    def click_show_more_on_item(self, item):
        try:
            from selenium.webdriver import ActionChains
            show_more_btn = item.find_element(By.XPATH, ".//a[@class='toggle-expand inline']")
            ActionChains(self.driver).move_to_element(show_more_btn).click().perform()
            # show_more_btn.click()
        except Exception,e:
            print 'show load more on item error', e
        finally:
            print 'show more on item finished'


def click_hide_more(item):
    try:
        # hide_more_btn = driver.find_element(By.XPATH,
        #                                     ".//div[@class='action-item item-collapse js-collapse is-sticky'] or button[@class='action-item item-collapse js-collapse']")
        hide_more_btn = item.find_element(By.XPATH, ".//button[@class='action-item item-collapse js-collapse' or @class='action-item item-collapse js-collapse is-sticky']")
        hide_more_btn.click()
    except Exception,e:
        print 'hide more on item error', e
    finally:
        print 'hide more on item finished'


def save_article_info_phantomjs(driver, post_item, dir_path):
    import os
    token = post_item.find_element(By.XPATH, ".//meta[@itemprop='post-url-token']").get_attribute('content')
    path = dir_path+'/'+token
    if not os.path.isdir(path):
        os.mkdir(path)

    webdriverlib = WebDriverLib(driver)
    # webdriverlib.take_screenshot_on_item(driver, post_item, path)
    # webdriverlib.wait_for_img_loading_finished(driver)
    webdriverlib.take_screenshot_on_element(driver, post_item, path)


def save_article_info_chrome(driver, post_item, dir_path):
    import os
    token = post_item.find_element(By.XPATH, ".//meta[@itemprop='post-url-token']").get_attribute('content')
    title = post_item.find_element(By.XPATH, ".//div[@class='title']/a").text
    summary = post_item.find_element(By.XPATH, ".//div[contains(@class,'summary')]").get_attribute('innerHTML')
    print token,title,summary

    path = dir_path+'/'+token
    if not os.path.isdir(path):
        os.mkdir(path)

    save_to_file(token, title, summary, path)

    webdriverlib = WebDriverLib(driver)
    webdriverlib.take_screenshot_on_item(driver, post_item, path)
    # webdriverlib.wait_for_img_loading_finished(driver)
    # webdriverlib.take_screenshot_on_element(driver, post_item, path)


def save_to_file(token, title, summary, path):
    f = open(path+'/title', 'w')
    f.write(encode_to_gb2312(title))
    f.close()

    f = open(path+'/summary', 'w')
    f.write(encode_to_gb2312(summary))
    f.close()

    f = open(path+'/token', 'w')
    f.write(encode_to_gb2312(token))
    f.close()


def encode_to_gb2312(text):
    try:
        if isinstance(text, unicode):
            text = text.encode('gb2312')
        else:
            text = text.decode('utf-8').encode('gb2312')
    except Exception, e:
        print 'encode error', e
        text = ""
    return text

def screenshot(raw, item, dir_path, name='screenshot.png'):
    token = item.find_element(By.XPATH, ".//meta[@itemprop='post-url-token']").get_attribute('content')
    path = dir_path+'/'+token
    if not os.path.isdir(path):
        os.mkdir(path)

    left = item.location['x']
    top = item.location['y']
    right = left + item.size['width']
    bottom = top + item.size['height']
    raw.crop((left, top, right, bottom)).save(path+'/'+name)
    print 'save '+path+'/'+name


def save_screenshot_chrome():
    import os
    dir_path = "/tmp/zhihu"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    from selenium import webdriver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome()
    zhihu = ZhihuLib(driver)
    driver.get(zhihu.get_search_url('pokemongo'))

    count = 100
    zhihu.load_more_until_zan(count)
    zhihu.save_article_question_list(count)

    for item in zhihu.article_list:
        # print 'before: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']
        zhihu.click_show_more_on_item(item)
        # print 'mid: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']
        save_article_info_chrome(driver, item, dir_path)
        # print 'after: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']


def test_screen_shot():
    import os
    dir_path = "/tmp/zhihu"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    from selenium import webdriver
    # driver = webdriver.Chrome()
    driver = webdriver.PhantomJS()
    zhihu = ZhihuLib(driver)
    driver.get(zhihu.get_search_url('pokemongo'))

    count = 100
    zhihu.load_more_until_zan(count)
    zhihu.save_article_question_list(count)


    for item in zhihu.article_list:
        # print 'before: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']
        zhihu.click_show_more_on_item(item)
        # print 'mid: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']
        # print 'after: ',item.location['x'],item.location['y'],item.size['width'],item.size['height']
    webdriverlib = WebDriverLib(driver)
    webdriverlib.wait_for_img_loading_finished(driver,60)

    driver.save_screenshot('/tmp/zhihu/raw.png')

    from PIL import Image

    raw = Image.open('/tmp/zhihu/raw.png')

    for item in zhihu.article_list:
        # save_article_info(driver, item, dir_path)
        screenshot(raw, item, dir_path)


def test():
    import os
    dir_path = "/tmp/zhihu"
    if not os.path.isdir(dir_path):
        os.mkdir(dir_path)

    from selenium import webdriver
    # driver = webdriver.Chrome()
    driver = webdriver.Chrome()
    zhihu = ZhihuLib(driver)
    driver.get(zhihu.get_search_url('pokemongo'))

    count = 100
    zhihu.save_article_question_list(count)
    zhihu.click_show_more_on_item(zhihu.article_list[0])
    save_article_info_chrome(driver, zhihu.article_list[0], dir_path)
    save_article_info_chrome(driver, zhihu.article_list[1], dir_path)

if __name__ == '__main__':
    save_screenshot_chrome()
    # test()
    # from selenium import webdriver
    #
    # driver = webdriver.PhantomJS()
    # zhihu = ZhihuLib(driver)
    # driver.get(zhihu.get_search_url('pokemongo'))
    # driver.save_screenshot('/tmp/raw.png')
    #
    # from PIL import Image
    # im = Image.open('/tmp/raw.png')
    # im.crop((0, 0, 300, 500)).save('/tmp/rawcrop.png')
    # im.crop((150, 0, 300, 500)).save('/tmp/rawcrop2.png')


    # from selenium import webdriver
    # driver = webdriver.Chrome()
    # driver.get('https://www.douban.com/group/topic/6747157/')
    # body = driver.find_element_by_class_name('mod')
    # WebDriverLib(driver).take_screenshot_on_item(driver, body, '/tmp/douban')
    #
    # driver.get('http://www.baidu.com/')
    # lg = driver.find_element_by_id('lg')
    # WebDriverLib(driver).take_screenshot_on_item(driver, lg, '/tmp/baidu')
    #
    # driver.get('https://www.zhihu.com/search?type=content&q=pokemongo/')
    # lg = driver.find_element_by_xpath("//div[@class='zg-wrap zu-main clearfix']")
    # WebDriverLib(driver).take_screenshot_on_item(driver, lg, '/tmp/zhihu1')
