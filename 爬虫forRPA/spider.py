from selenium import webdriver
import time
import re
import requests
import json
import sys


def get_url(username, pwd):
    # Create a new instance of the Firefox driver
    browser = webdriver.Chrome(executable_path='./chromedriver')
    # open baidu.com
    browser.get("http://www.chinahby.com/")
    # sleep 2 secs
    time.sleep(3)
    #clean the enter text
    browser.find_element_by_id("UserName").clear()
    #enter something
    browser.find_element_by_id("UserName").send_keys(username)
    browser.find_element_by_id("Password").clear()
    browser.find_element_by_id("Password").send_keys(pwd)
    #submit
    browser.find_element_by_id("btnSubmit").click()
    # sleep 2 secs
    time.sleep(3)
    # print(browser.get_cookies())
    current_url = browser.current_url
    #quit
    browser.quit()
    return current_url

def get_token_cookie(username, pwd):
    url = get_url(username, pwd)
    token = re.findall(r'token=(\d+)#', url)[0]
    try:
        res = requests.get(url)         
        cookies = res.cookies
        cookie = requests.utils.dict_from_cookiejar(cookies)
        result = {}
        result['token'] = token
        
        result['cookie'] = cookie
        return result
    except Exception as err:
        print('获取cookie失败：\n{0}'.format(err))
    

def load_unit_info():
    with open('./mapping.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def get_data():
    machine_name = sys.argv[1]
    date = sys.argv[2]
    username = sys.argv[3]
    pwd = sys.argv[4]
    unit_info = load_unit_info()
    machine_info = unit_info[machine_name]
    unitId = machine_info['unitId']
    threshold = float(machine_info['threshold'])
    print(threshold)
    result_data = {
        "日期": date,
        "产线": machine_info['line'],
        "机器": machine_name,
        "早低谷":"",
        "早高峰":"",
        "午平时":"",
        "晚高峰":"",
        "晚平时":""
    }
    token_cookie = get_token_cookie(username, pwd)
    token = token_cookie['token']
    cookie_dict = token_cookie['cookie']
    cookie = list(cookie_dict.keys())[0] + "=" + list(cookie_dict.values())[0]
    for i in range(1, len(cookie_dict.items())):
        cookie = cookie + "; " +  list(cookie_dict.keys())[i] + "=" + list(cookie_dict.values())[i]
    url = 'http://www.chinahby.com/Main/control/CtrlEP_UseElecData.ashx'
    headers={
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "118",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,
        "Host": "www.chinahby.com",
        "Origin": "http://www.chinahby.com",
        "Pragma": "no-cache",
        "Referer": "http://www.chinahby.com/Main/EP_UseElecData.aspx?token=6700058675281920&unitId=D_395568_235294_345678&companyId=null&sdt=null&edt=null",
        "token": token,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    POST_BODY = f"token={token}&userId=0&sdt1={date}&edt1={date}&unitId={unitId}&companyId=null&code=xldz"
   
    r = requests.post(url,POST_BODY, headers=headers)
    
    # fp = open(f"{machine_name}.json","w",encoding='utf-8')
    
    data = json.loads(str(r.content,'utf-8'))
    print(type(data))
    data = data[0]['ChartElecData'][0]
    dataArray = data['DataArray']
    # timeArray = data['DataReportTime']
    print(dataArray)

    index_morning_low = 32 # 8:01
    index_morning_high = 48 # 12:01
    index_noon_normal = 68 # 17:01
    index_night_high = 84 # 21:01
    index_night_normal = 95 # 23:46

    count_morning_low =0
    count_morning_high = 0
    count_noon_normal = 0
    count_night_high = 0
    count_night_normal = 0

    # 早低谷
    for i in range(0, index_morning_low+1):
        if dataArray[i] == '-':
            continue
        elif float(dataArray[i]) > threshold:
            print(float(dataArray[i]))
            count_morning_low += 15
    # 早高峰
    for i in range(index_morning_low+1, index_morning_high+1):
        if dataArray[i] == '-':
            continue
        elif float(dataArray[i]) > threshold:
            print(float(dataArray[i]))
            count_morning_high += 15
    # 午平时
    for i in range(index_morning_high+1, index_noon_normal+1):
        if dataArray[i] == '-':
            continue
        elif float(dataArray[i]) > threshold:
            print(float(dataArray[i]))
            count_noon_normal += 15
    # 晚高峰
    for i in range(index_noon_normal+1, index_night_high+1):
        if dataArray[i] == '-':
            continue
        elif float(dataArray[i]) > threshold:
            print(float(dataArray[i]))
            count_night_high += 15
    # 晚平时
    for i in range(index_night_high+1, index_night_normal+1):
        if dataArray[i] == '-':
            continue
        elif float(dataArray[i]) > threshold:
            print(float(dataArray[i]))
            count_night_normal += 15
            
    result_data['早低谷'] = count_morning_low
    result_data['早高峰'] = count_morning_high
    result_data['午平时'] = count_night_high
    result_data['晚高峰'] = count_night_high
    result_data['晚平时'] = count_night_normal
    print(result_data)
    return result_data


if __name__ == '__main__':
    get_data()
    # load_unit_info()
    # process_data()


