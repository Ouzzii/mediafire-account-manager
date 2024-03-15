from time import sleep
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.remote.webelement import WebElement
from os import get_terminal_size
class Nonetype:
    def get_attribute(x=""):
        return None
    def click():
        return None

class tools:
    def __init__(self, driver):
        self.driver = driver
    def css_selector(self, selector):
        if len(self.driver.find_elements("css selector", selector)):
            return self.driver.find_element("css selector", selector)
        else:
            return Nonetype
    def css_selector_all(self, selector):
        if len(self.driver.find_elements("css selector", selector)):
            return self.driver.find_elements("css selector", selector)
        else:
            return [Nonetype]

    def xpath(self, selector):
        if len(self.driver.find_elements("xpath", selector)):
            return self.driver.find_element("xpath", selector)
        else:
            return Nonetype
    def waitfor(self, function, selector, behavior = None, timeout = 0, silent = False, exception=False):
        delta = 0.1
        if not timeout:
                _timeout = 150
        else:
                _timeout = timeout
                if int(_timeout/delta) == 0:
                    _timeout = 1
        for _ in range(int(_timeout/delta)):
            sleep(delta)
            if not silent:
                print("waiting for,", selector, end=f"{(len(selector)+13)*' '}\r")
            if behavior == None:
                if function(selector).__class__ == WebElement:
                    return function(selector)
            elif behavior == "click":
                if function(selector).__class__ == WebElement:
                    function(selector)
                    try:
                        function(selector).click()
                        return 0
                    except ElementClickInterceptedException:
                        pass
        if _timeout and exception:
            raise TimeoutError
        else:
            return None
        
    def printr(message):
        print(f"{message}{(get_terminal_size()[0]-len(message)-1)*' '}")