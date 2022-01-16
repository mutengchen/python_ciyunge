from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
# 打开浏览器
option = webdriver.ChromeOptions()
option.add_argument('headless')  # 设置option
option.add_argument('--no-sandbox')
option.add_argument('--disable-gpu')
option.add_argument('--disable-dev-shm-usage')
if_duo_data = []
if_kong_data = []
ic_duo_data = []
ic_kong_data = []
driver = webdriver.Chrome(chrome_options=option,executable_path=r'C:/chromedriver.exe')  # 调用带参数的谷歌浏览器
def getElement(select,xinghao,type):
    select.select_by_value(xinghao)
    driver.find_element_by_id("btnSearch").click()
    time.sleep(1)
    #获取多头数据变动值//li[@data='80050220']
    duo = driver.find_element_by_id("ulDtcc").find_element_by_xpath('li[@data="80050220"]').find_element_by_xpath('span[@class="V2e4"]')
    
    #获取空头数据变动值
    kong = driver.find_element_by_id("ulKtcc").find_element_by_xpath('li[@data="80050220"]').find_element_by_xpath('span[@class="V2e4"]')
    if type=="IF":
        if_duo_data.append(duo.text)    
        if_kong_data.append(kong.text)
    else:
        ic_duo_data.append(duo.text)    
        ic_kong_data.append(kong.text)
   



if __name__ == "__main__":
    #获取IC数据
    driver.get("http://data.eastmoney.com/IF/Data/Contract.html?va=IC")
    #选择全部四个iF
    select  = Select(driver.find_element_by_id("futures_contract"))
    
    # getElement(select,"ic2110","IC")
    # getElement(select,"ic2111","IC")
    # getElement(select,"ic2112","IC")
    getElement(select,"ic2203","IC")
    getElement(select,"ic2206","IC")
    getElement(select,"ic2201","IC")
    #获取IF数据
    driver.get("http://data.eastmoney.com/IF/Data/Contract.html?va=IF")
    #选择全部四个iF
    select  = Select(driver.find_element_by_id("futures_contract"))
    # getElement(select,"if2110","IF")
    # getElement(select,"if2111","IF")
    # getElement(select,"if2112","IF")
    getElement(select,"if2203","IF")
    getElement(select,"if2206","IF")
    getElement(select,"if2201","IF")

    #遍历计算
    if_duo_res = 0
    if_kong_res = 0
    ic_kong_res = 0
    ic_duo_res = 0

    for item in if_duo_data:
        if_duo_res = if_duo_res + int(item)
    for item in ic_duo_data:
        ic_duo_res = ic_duo_res + int(item)
    for item in if_kong_data:
        if_kong_res = if_kong_res + int(item)
    for item in ic_kong_data:
        ic_kong_res = ic_kong_res + int(item)  
    print("if多单变化",if_duo_res)
    print("if空单变化",if_kong_res)
    print("ic多单变化",ic_duo_res)
    print("ic空单变化",ic_kong_res)
    zongde = (if_duo_res+ic_duo_res)-(ic_kong_res+if_kong_res)
    print("综合：",zongde)

    # driver.find_element_by_name("btnSearch").click()
    # #寻找title = 中信期货代号（80050220）的li标签
    # #获取IC数据
    # driver.get("http://data.eastmoney.com/IF/Data/Contract.html?va=IC")

    # #获取IH数据
    # driver.get("http://data.eastmoney.com/IF/Data/Contract.html?va=IH")

