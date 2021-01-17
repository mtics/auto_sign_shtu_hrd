# -*- coding:gbk -*-

import time
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select

from private_info import *
import mail


def is_element_present(browser, xpath):
    from selenium.common.exceptions import NoSuchElementException

    try:
        element = browser.find_element_by_xpath(xpath)
    except NoSuchElementException as e:
        # print(e)
        return False
    else:
        return True


def sign_in(uid, pwd):
    # set to no-window
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    # simulate a browser to open the website
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.Chrome()
    browser.get("https://hrd.shanghaitech.edu.cn/")

    msg = ''

    try:

        # Click the Identity Selector to select 'Student'
        browser.find_element_by_xpath("//*[@id='matchingform']/div[2]/div/div/button").click()
        browser.find_element_by_xpath("//*[@id='matchingform']/div[2]/div/div/div/ul/li[2]/a").click()

        # Click the infomationXueYuan Selector to select 'XinxiXueYuan'
        browser.find_element_by_xpath("//*[@id='matchingform']/div[3]/div/div/button").click()
        browser.find_element_by_xpath("//*[@id='matchingform']/div[3]/div/div/div/ul/li[3]/a").click()

        # input uid and password
        print("Inputting the UID and Password of User {0}".format(uid))
        browser.find_element_by_id("j_email").send_keys(uid)
        browser.find_element_by_id("IDcard").send_keys(pwd)

        # click to sign in
        browser.find_element_by_id("matchingbtn").click()
        time.sleep(2)

        # If there is a popup window, close it
        if is_element_present(browser, "//*[@id='HighRisk']/div/div/div[1]/button"):
            browser.find_element_by_xpath("//*[@id='HighRisk']/div/div/div[1]/button").click()
            time.sleep(0.5)

        # click to submit
        print("Signing in for User {0}".format(uid))

        # Daily punch in
        browser.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[3]/button").click()
        time.sleep(0.5)
        browser.find_element_by_id("ReconfirmSafeness-btn").click()

        msg = "Singing in for User {0} is finished".format(uid)

    except Exception as e:
        msg = "while signing in for user " + uid + " there is an exception: \n" + str(e)
        mail.mail(msg, MAIL_ADMAIN)
    finally:
        browser.quit()

    # quit the browser
    print("Singing in for User {0} is finished".format(uid))
    return msg


def timing(hour, minute, the_users):
    now = datetime.datetime.now()
    if now.hour == hour and now.minute == minute:
        print("\n\n\n")
        print(now)
        for user in the_users:
            msg = sign_in(user.uid, user.pwd)
            msg = user.uid + ": " + msg
            print("Emailing to User {0} for notification".format(user.uid))
            mail.mail(msg, user.email)
            print("Emailing is finished")


if __name__ == "__main__":
    # For Single User
    # msg = sign_in(UID, PWD)
    # mail.mail(msg, EMAIL_TO)

    # For Multiple Users
    for user in users:
        msg = sign_in(user.uid, user.pwd)
        print("Emailing to User {0} for notification".format(user.uid))
        mail.mail(msg, user.email)
        print("Emailing is finished")

    # For Timing and Multiple Users
    # while True:
    #
    #     # sign for lizhw
    #     timing(6, 0, users)
    #
    #     # sleep 30 secs
    #     time.sleep(30)
