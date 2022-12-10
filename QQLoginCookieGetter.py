# 步骤1:获取登录cookie文件
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_cookie_json(qq_number,password):
        qq_number = qq_number
        password = password

        login_url = 'https://i.qq.com/'
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(login_url)
        driver.switch_to.frame('login_frame')
        driver.find_element(By.XPATH,'//*[@id="switcher_plogin"]').click()
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="u"]').send_keys(qq_number)
        driver.find_element(By.XPATH,'//*[@id="p"]').send_keys(password)
        time.sleep(1)
        driver.find_element(By.XPATH,'//*[@id="login_button"]').click()
        time.sleep(1)
        time.sleep(20)#等待手动登录拿cookies
        cookie_list = driver.get_cookies()
        cookie_dict = {}
        for cookie in cookie_list:
            if 'name' in cookie and 'value' in cookie:
                cookie_dict[cookie['name']] = cookie['value']
        with open('cookie_dict2.txt', 'w') as f:
            json.dump(cookie_dict, f)
        return True


if __name__ == '__main__':
    get_cookie_json("账号",
                    "密码")#换账号记得删除timeout2,intxt2,cookie2文件再重新生成