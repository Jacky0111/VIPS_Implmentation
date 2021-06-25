import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

browser = webdriver.Chrome()
url = 'https://www.thestar.com.my/'
browser.get(url)
time.sleep(30)

file = open('DOM.js', 'r')
java_script = file.read()
print(java_script)
