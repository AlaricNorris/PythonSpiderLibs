#!/usr/local/bin/python
#coding = utf-8
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

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


def take_screenshot(url, save_fn="/tmp/capture.png"):
    import time
    from selenium import webdriver
    browser = webdriver.Chrome() # Get local session of firefox
    browser.set_window_size(1200, 900)
    browser.get(url) # Load page
    browser.execute_script("""
        (function () {document.write("<script src='https://github.com/niklasvh/html2canvas/releases/download/0.5.0-alpha1/html2canvas.js'><\/script>");
            //html2canvas(document.body.getElementsByClassName('codehilite')[0], {
            //onrendered: function(canvas) {
              //document.body.appendChild(canvas);
              //}
            //});
        })();
    """)

    # for i in xrange(30):
    #     if "scroll-done" in browser.title:
    #         break
    #     time.sleep(10)

    # browser.save_screenshot(save_fn)
    # browser.close()


def create_element(driver, element):
    # location = li.location
    # size = li.size

    from selenium import webdriver
    from PIL import Image
    import time
    # time.sleep(10)

    # fox = webdriver.Chrome()
    # fox.get('http://stackoverflow.com/')

    # now that we have the preliminary stuff out of the way time to get that image :D
    # element = fox.find_element_by_id('hlogo') # find part of the page you want image of

    driver.execute_script("""
        (function () {
            var y = 0;
            var step = 100;
            window.scroll(0, 0);

            function f() {
                if (y < document.body.scrollHeight) {
                    y += step;
                    window.scroll(0, y);
                    setTimeout(f, 100);
                } else {
                    window.scroll(0, 0);
                    document.title += "scroll-done";
                }
            }

            setTimeout(f, 1000);
        })();
    """)

    for i in xrange(30):
        if "scroll-done" in driver.title:
            break
        time.sleep(10)

    print 'scroll to element'
    driver.execute_script("arguments[0].scrollIntoView();", element)

    driver.save_screenshot('screenshot.png') # saves screenshot of entire page
    # driver.quit()

    im = Image.open('screenshot.png') # uses PIL library to open image in memory
    location = element.location
    size = element.size

    # left = location['x']
    # top = location['y']
    # right = location['x'] + size['width']
    # bottom = location['y'] + size['height']
    # driver.set_window_size(size['width'], size['height'])
    # driver.set_window_position(location['x'], location['y'])
    left = location['x']
    top = 0
    right = location['x'] + size['width']
    bottom = size['height']

    # driver.save_screenshot('screenshot.png') # saves screenshot of entire page
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save('screenshot.png') # saves new cropped image
    print 'scroll by 0,500'
    driver.execute_script("scrollBy(0,500);")
    driver.save_screenshot('screenshot1.png') # saves screenshot of entire page

    time.sleep(30)


def click_show_more_on_item(item):
    try:
        show_more_btn = item.find_element(By.XPATH, ".//a[@class='toggle-expand inline']")
        show_more_btn.click()
    except Exception,e:
        print 'show load more on item error', e
    finally:
        print 'show more on item finished'


def test_screen_shot():
    # take_screenshot('http://codingpy.com/article/take-screenshot-of-web-page-using-selenium/')
    # take_screenshot('http://baidu.com')
    # exit()
    # import time
    # time.sleep(300)

    from selenium import webdriver
    driver = webdriver.Chrome()
    # driver = webdriver.Remote()
    # driver.set_window_size(800, 10000)
    zhihu = ZhihuLib(driver)
    driver.get(zhihu.get_search_url('pokemongo'))

    count = 100
    # search keyword
    # zhihu.load_more_until_zan(count)
    # while last li zan > 100
    #   load more
    # li_list = zhihu.get_li_list()
    # print 'load more End, len is ',str(len(li_list))
    # foreach li
    # if zan > 100
    #    if article:
    #       put in article list
    #    if question:
    #       put int question list
    # save list to local
    zhihu.save_article_question_list(count)
    # item = zhihu.article_list[len(zhihu.article_list)-1]
    item = zhihu.article_list[0]
    click_show_more_on_item(item)
    # create_element(driver, item)
    webdriverlib = WebDriverLib(driver)
    webdriverlib.take_screenshot_on_item(driver, item)
    # output
    #   screenshot save to local
    # zhihu.article_list[0].save_screenshot('/tmp/s2.png')
    # create_element(zhihu.article_list[0])
    # li = zhihu.article_list[0]
    # li.screenshot("/tmp/s2.png")
    # driver.save_screenshot('/tmp/s.png')

if __name__ == '__main__':
    test_screen_shot()
    # from selenium import webdriver
    # driver = webdriver.Chrome()
    # WebDriverLib.take_screenshot_on_item(driver=driver, )
