# encoding=utf-8

from selenium import webdriver
from time import strftime, gmtime
import requests
import time
import json

# 开启浏览器


def openChrome():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    driver = webdriver.Chrome(options=option)
    return driver


def find(driver, str):
    try:
        driver.find_element_by_xpath(str)
    except:
        return False
    else:
        return True

# 流程


def operate_dk(driver):
    # 打开配置文件
    try:
        with open("config.json", encoding='utf-8') as f:
            config = json.load(f)
    except:
        print("配置文件错误！请检查配置文件是否与py文件放置于同一目录下，或配置文件是否出错！\n请注意'现人员位置'只可填入以下四项中的任意一项：'留校', '在苏州', '江苏省内其他地区', '在其他地区'")
        return -1
    else:
        url = "https://auth.suda.edu.cn/cas/login?service=https%3A%2F%2Fauth.suda.edu.cn%2Fsso%2Flogin%3Fredirect_uri%3Dhttp%253A%252F%252Fauth.suda.edu.cn%252Fsso%252Foauth2%252Fauthorize%253Fscope%253Dclient%2526response_type%253Dcode%2526state%253D123%2526redirect_uri%253Dhttps%25253A%25252F%25252Fauth.suda.edu.cn%25252Fmiddleware%25252Fclient%25253Fapp%25253Dsswsswzx2%252526welcome%25253D%2525E4%2525BA%25258B%2525E5%25258A%2525A1%2525E4%2525B8%2525AD%2525E5%2525BF%252583%252526x_app_url%25253Dhttp%25253A%25252F%25252Faff.suda.edu.cn%25252F_web%25252Fucenter%25252Flogin.jsp%2526client_id%253Dhuc7ES9iOtrLLhTkCZVk%26x_client%3Dcas"
        driver.get(url)
        # 找到输入框并输入查询内容
        elem = driver.find_element_by_id("username")
        elem.send_keys(config["学号"])
        elem = driver.find_element_by_id("password")
        elem.send_keys(config["密码"])
        # 提交表单
        driver.find_element_by_xpath("//*[@id='fm1']/div[7]").click()
        try:
            driver.find_element_by_xpath("//*[text()='首页']")
        except:
            print('登陆失败！请检查学号密码是否正确')
            return -1
        else:
            print('登录成功！')
            url = "http://aff.suda.edu.cn/_web/fusionportal/detail.jsp?_p=YXM9MSZwPTEmbT1OJg__&id=2749&entranceUrl=http%3A%2F%2Fdk.suda.edu.cn%2Fdefault%2Fwork%2Fsuda%2Fjkxxtb%2Fjkxxcj.jsp&appKey=com.sudytech.suda.xxhjsyglzx.jkxxcj."
            driver.get(url)
            driver.find_element_by_xpath(
                "//*[@class='action-btn action-do']").click()

            # 切换到小框内
            iframe1 = driver.find_element_by_id("layui-layer-iframe1")
            driver.switch_to.frame(iframe1)
            flag = False
            while(flag == False):
                time.sleep(1)
                flag = find(driver, "//*[text()='"+config["学号"]+"']")

            driver.find_element_by_xpath("//*[@id='checkbox_jkzk33']").click()
            xrywz = {'在校': 'radio_xrywz5', '在苏州': 'radio_xrywz7',
                     '江苏省内其他地区': 'radio_xrywz9', '在其他地区': 'radio_xrywz23'}
            driver.find_element_by_xpath(
                "//*[@id='"+xrywz[config["现人员位置"]]+"']").click()
            elem = driver.find_element_by_id("input_jtdz")
            elem.send_keys(config["家庭地址"])
            driver.find_element_by_xpath("//*[@id='radio_sfyxglz27']").click()

            # 提交
            driver.find_element_by_xpath("//*[@id='tpost']").click()
            time.sleep(1)
            try:
                driver.find_element_by_xpath("//*[text()='提交成功！']")
                print('打卡成功！')
                driver.find_element_by_xpath(
                    "//a[@class='layui-layer-btn0']").click()
                ddpost("今天的打卡已经成功执行")
                wxpost("主人，打卡成功啦~")
            except:
                try:
                    driver.find_element_by_xpath(
                        "//*[text()='当天已经提交过，是否继续提交？']")
                    print("已打卡过！")
                    driver.find_element_by_xpath(
                        "//a[@class='layui-layer-btn0']").click()
                    ddpost("今天的打卡已经成功执行")
                    wxpost("主人，打卡GET啦~")
                except:
                    print("打卡失败！请重新开始")
                    driver.find_element_by_xpath(
                        "//a[@class='layui-layer-btn0']").click()
                    ddpost("今天的打卡失败，请手动打卡")
                    wxpost("今天的打卡失败，请手动打卡")
            time.sleep(3)
            print("即将退出程序...")
            driver.quit()

# 钉钉webhook机器人推送

def ddpost(content):
    with open("config.json", encoding='utf-8') as f:
        config = json.load(f)
    timenow = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    url = "https://oapi.dingtalk.com/robot/send?access_token="+config['ddkey']
    data = '{"msgtype":"markdown","markdown":{"title":"每日疫情打卡","text":"# 每日打卡提醒 \n >### 消息提示：' + \
        content + ' \n >### 打卡时间：' + timenow + '"}}'
    headers = {'Content-Type': 'application/json'}
    byte_data = data.encode("utf-8")
    rep = requests.post(url=url, data=byte_data, headers=headers)
    print("钉钉打卡成功")

# 微信server酱机器人推送

def wxpost(content):
    with open("config.json", encoding='utf-8') as f:
        config = json.load(f)
    driver.get("https://sc.ftqq.com/"+config['wxkey']+".send?text="+content)
    print("微信打卡成功")


# 主函数
if __name__ == '__main__':
    print("这是一个自动健康打卡的程序。\n\n请在同目录下的config.json中配置打卡信息，例如：\n'学号': '1827405055',\n'密码': '12345678',\n'现人员位置': '在苏州',      (请注意只可填入以下四项中的任意一项：'留校', '在苏州', '江苏省内其他地区', '在其他地区')\n'家庭地址': '工业园区'\n其余所有属性均为打卡系统自动填充的上一次打卡信息\n如果需要自动打卡，可以在ddkey或wxkey当中填写你申请的钉钉webhook机器人accesskey或在wxkey当中填写微信server酱公众号的accesskey\n\n程序即将启动...")
    driver = openChrome()
    operate_dk(driver)
