from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time

def test_proxy(proxy):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--proxy-server={}'.format(proxy))
    driver = webdriver.Chrome(chrome_options=chrome_options)

    try:
        driver.get("https://soundcloud.com/punjab-studio/confess-jerry")
        return True
    except Exception as e:
        print("Proxy is not working:", e)
        return False
    finally:
        time.sleep(100)
        driver.quit()
"""
185.16.61.36:45212
35.247.214.238:3129
35.247.234.213:3129
23.132.185.101:53128
35.247.199.249:3129

35.247.236.134:3129
34.140.70.242:8080
"""
# Example usage:
proxy = '185.16.61.36:45212'
if test_proxy(proxy):
    print("Proxy is working!")
else:
    print("Proxy is not working.")