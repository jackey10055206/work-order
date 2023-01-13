from selenium import webdriver
import time

url = 'http://192.168.101.64:8080/'
path = 'chromedriver.exe'
browser = webdriver.Chrome(executable_path=path)


def login():
    path = 'chromedriver.exe'
    browser = webdriver.Chrome(executable_path=path)
    browser.get("http://192.168.101.64:8080")


    element_username = browser.find_element_by_id("input_username")
    element_username.send_keys("root")

    element_password = browser.find_element_by_id("input_password")
    element_password.send_keys("jackey8869")

    button = browser.find_element_by_id("input_go")
    button.click()
    browser.close