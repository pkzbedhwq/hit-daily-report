from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
import json

denglu = json.loads(open("denglu.json", "r").read())
XPATH_FORM_CHECKBOX_3 = "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[65]/label"
XPATH_FORM_CHECKBOX_2 = "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[64]/label"
XPATH_FORM_CHECKBOX_1 = "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[63]/label"
XPATH_FORM_BUTTON_SUBMIT = "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[66]/div/div/span[1]"
XPATH_FORM_BUTTON_GET_LOCATION = "/html/body/div[2]/div[2]/div[2]/div/div/div[1]/div[17]/div[2]/div/div/span/a"
URL_LOGIN = "https://ids.hit.edu.cn/authserver/login?service=https%3A%2F%2Fxg%2Ehit%2Eedu%2Ecn%2Fzhxy%2Dxgzs%2Fxg%5Fmobile%2FxsMrsbNew%2Fedit/"
URL_FORM = "https://xg.hit.edu.cn/zhxy-xgzs/xg_mobile/xsMrsbNew/edit/"
proflie = webdriver.FirefoxProfile()
proflie.set_preference("geo.prompt.testing", True)
proflie.set_preference("geo.prompt.testing.allow", True)
proflie.set_preference("geo.wifi.uri", "location.json")
driver = webdriver.Firefox(firefox_profile=proflie)
driver.get(URL_LOGIN)
def wait_page_load(drv, timeout):
    WebDriverWait(drv, timeout).until(lambda dr: dr.execute_script('return document.readyState;') == "complete",message="页面加载超时")
WebDriverWait(driver, 20).until(EC.title_is("统一身份认证平台"),message="无效的登录页面")
wait_page_load(driver, 20)
elem_username = driver.find_element("xpath", '//*[@id="username"]')
elem_password = driver.find_element("xpath", '//*[@id="password"]')
elem_button_login = driver.find_element("xpath", '//*[@id="login_submit"]')
for i in range(0, 100):
    elem_username.send_keys(Keys.BACKSPACE)
    elem_password.send_keys(Keys.BACKSPACE)
elem_username.send_keys(denglu["xuehao"])
elem_password.send_keys(denglu["password"])
elem_button_login.click()
WebDriverWait(driver, 20).until(EC.title_is("HIT学工"),message="点击登录按钮后，登录页面跳转失败")
wait_page_load(driver, 20)
driver.get(URL_FORM)
WebDriverWait(driver, 20).until(lambda drv: drv.execute_script("return document.readyState;"),message="填报页面加载失败")
wait_page_load(driver, 20)
elem_button_location = driver.find_element("xpath", XPATH_FORM_BUTTON_GET_LOCATION)
elem_loading = driver.find_element("xpath", '//*[@id="loading"]')
elem_button_location.click()
WebDriverWait(driver, 20).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="loading"]')),message="获取地理位置失败")
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
elem_checkboxes = [driver.find_element("xpath", XPATH_FORM_CHECKBOX_1),driver.find_element("xpath", XPATH_FORM_CHECKBOX_2),driver.find_element("xpath", XPATH_FORM_CHECKBOX_3)]
for box in elem_checkboxes:
    box.click()
elem_submit = driver.find_element("xpath", XPATH_FORM_BUTTON_SUBMIT)
elem_submit.click()
WebDriverWait(driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, "/html/body/div[3]"), "操作成功"),message="表单提交失败")
driver.close()
exit(0)




