#!/usr/local/bin/python
#coding = utf-8

from selenium.webdriver.support import expected_conditions as EC
import selenium.webdriver.support.ui as ui


class WebDriverLib:
    def __init__(self, driver):
        self.wait = ui.WebDriverWait(driver, 10)

    def waitToFind(self, by):
        return self.wait.until(
            EC.presence_of_element_located(by)
        )

    def waitToVisible(self, by):
        return self.wait.until(
            EC.visibility_of_element_located(by)
        )

    def waitToLeave(self, by):
        return self.wait.until(
            EC.invisibility_of_element_located(by)
        )

    def take_screenshot_on_item(self, driver, element):
        import time
        # time.sleep(10)

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
        location = element.location
        size = element.size
        window_size = driver.get_window_size()
        driver.execute_script("arguments[0].scrollIntoView();", element)

        remain_height = size['height']
        window_height = window_size['height'] - 80
        padding = 60
        left = location['x'] - padding
        right = location['x'] + size['width'] + padding
        screenshot_index = 0
        while True:
            filename = 'screenshot'+str(screenshot_index)+'.png'
            if (remain_height > window_height):
                driver.save_screenshot(filename) # saves screenshot of entire page
                scop_to(filename, left, 0, right, window_height)
                remain_height -= window_height
                driver.execute_script("scrollBy(0,arguments[0]);", window_height)
                screenshot_index += 1
                print 'save ',filename
            else:
                driver.save_screenshot(filename) # saves screenshot of entire page
                scop_to(filename, left, 0, right, remain_height)
                print 'save ',filename
                break

def scop_to(filename, left, top, right, bottom):
    from PIL import Image
    im = Image.open(filename) # uses PIL library to open image in memory
    im = im.crop((left, top, right, bottom)) # defines crop points
    im.save(filename) # saves new cropped image
    print 'crop', filename
