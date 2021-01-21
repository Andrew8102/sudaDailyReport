# -*- coding:utf-8 -*-
"""
@author: 古时月
@file: daka.py
@time: 2021/1/21 10:54

"""
from selenium import webdriver
import requests
from selenium.webdriver.support.ui import Select
import time
import json


class Daka():
    def __init__(self, filename):
        self.config = filename
        self.driver = self.openChorme()
    
    def openChorme(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
        options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
        options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        options.add_argument('--headless')  # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
        options.add_argument('disable-infobars')
        driver = webdriver.Chrome(options=options)
        return driver
    
    def find(self, str):
        try:
            self.driver.find_element_by_xpath(str)
        except:
            return False
        else:
            return True
    
    # 流程
    def operate_dk(self):
        # 打开配置文件
        try:
            with open(self.config, encoding='utf-8') as f:
                configs = json.load(f)
        except:
            print("配置文件错误，请检查配置文件是否与py文件在同一目录下，或配置文件是否出错！\n请注意'现人员位置'只可填入以下四项中的任意一项：'留校', '在苏州', '江苏省内其他地区', '在其他地区'")
            return -1
        else:
            url = "https://auth.suda.edu.cn/cas/login?service=https%3A%2F%2Fauth.suda.edu.cn%2Fsso%2Flogin%3Fredirect_uri%3Dhttps%253A%252F%252Fauth.suda.edu.cn%252Fsso%252Foauth2%252Fauthorize%253Fscope%253Dopenid%252520profile%2526response_type%253Dcode%2526redirect_uri%253Dhttps%25253A%25252F%25252Fauth.suda.edu.cn%25252Fmiddleware%25252FgetProfile%25253Fapp%25253Dsswsswzx2%252526welcome%25253D%252525E4%252525BA%2525258B%252525E5%2525258A%252525A1%252525E4%252525B8%252525AD%252525E5%252525BF%25252583%252526x_app_url%25253Dhttp%25253A%25252F%25252Faff.suda.edu.cn%25252F_web%25252Fucenter%25252Flogin.jsp%2526client_id%253DzB0IOMznM2aInolxZ7F1%2526state%253D123%26x_client%3Dcas"
            self.driver.get(url)
            # 找到输入框并输入查询内容
            elem = self.driver.find_element_by_id("username")
            elem.send_keys(configs['学号'])
            elem = self.driver.find_element_by_id("password")
            elem.send_keys(configs["密码"])
            # 提交表单
            self.driver.find_element_by_class_name("login-btn").click()
            try:
                self.driver.find_element_by_xpath("//*[text()='首页']")
            except:
                print('登陆失败！请检查学号密码是否正确')
                return -1
            else:
                print('登录成功！')
                url = "http://aff.suda.edu.cn/_web/fusionportal/detail.jsp?_p=YXM9MSZwPTEmbT1OJg__&id=2749&entranceUrl=http%3A%2F%2Fdk.suda.edu.cn%2Fdefault%2Fwork%2Fsuda%2Fjkxxtb%2Fjkxxcj.jsp&appKey=com.sudytech.suda.xxhjsyglzx.jkxxcj."
                self.driver.get(url)
                self.driver.find_element_by_xpath("//*[@class='action-btn action-do']").click()
        
                # 切换到小框内
                iframe1 = self.driver.find_element_by_id("layui-layer-iframe1")
                self.driver.switch_to.frame(iframe1)
                flag = False
                while (flag == False):
                    time.sleep(1)
                    flag = self.find("//*[text()='" + configs["学号"] + "']")
                elem = self.driver.find_element_by_id("input_swtw")
                elem.send_keys("36.5")
                elem = self.driver.find_element_by_id("input_xwtw")
                elem.send_keys("36.5")
                self.driver.find_element_by_id("checkbox_jkzk33").click()
                # driver.find_element_by_id("select_xrywz").click()
                select2 = self.driver.find_element_by_id('select2-select_xrywz-container')
                # selectTag = Select(driver.find_element_by_id("select_xrywz"))
                # selectTag.select_by_value('38')
                select2.click()
                time.sleep(1)
                ul = self.driver.find_elements_by_class_name('select2-results__option')
                # for i in range(2, len(ul)):
                #     print(ul[i].get_attribute('id'))
                xrywz = {'在校': ul[2].get_attribute('id'),
                         '在苏州': ul[3].get_attribute('id'),
                         '江苏省内其他地区': ul[4].get_attribute('id'),
                         "在境外、在中高风险地区": ul[5].get_attribute('id'),
                         "在中高风险地区所在城市": ul[6].get_attribute('id'),
                         '在其他地区': ul[7].get_attribute('id')}
                self.driver.find_element_by_xpath(
                    "//*[@id='" + xrywz[configs["现人员位置"]] + "']").click()
                elem = self.driver.find_element_by_id("input_jtdz")
                elem.send_keys(configs["家庭地址"])
                # driver.find_element_by_xpath("//*[@id='radio_sfyxglz29']").click()
                self.driver.find_element_by_id('radio_sfyxglz7').click()
                self.driver.find_element_by_id('radio_sfywc11').click()
                self.driver.find_element_by_id('radio_sfygrzjcg15').click()
                self.driver.find_element_by_id('radio_sfyxcgjjc19').click()
                self.driver.find_element_by_id('radio_sfyzgfxljs23').click()
                self.driver.find_element_by_id('radio_sfyzgfxryjc27').click()
                
                # 提交
                self.driver.find_element_by_xpath("//*[@id='tpost']").click()
                time.sleep(1)
                try:
                    self.driver.find_element_by_xpath("//*[text()='提交成功！']")
                    print('打卡成功！')
                    self.driver.find_element_by_xpath(
                        "//a[@class='layui-layer-btn0']").click()
                    # self.ddpost("今天的打卡已经成功执行")
                    self.wxpost("主人，打卡成功啦~")
                except:
                    try:
                        self.driver.find_element_by_xpath(
                            "//*[text()='当天已经提交过，是否继续提交？']")
                        print("已打卡过！")
                        self.driver.find_element_by_xpath(
                            "//a[@class='layui-layer-btn0']").click()
                        # self.ddpost("今天的打卡已经成功执行")
                        self.wxpost("主人，打卡GET啦~")
                    except:
                        print("打卡失败！请重新开始")
                        self.driver.find_element_by_xpath(
                            "//a[@class='layui-layer-btn0']").click()
                        # self.ddpost("今天的打卡失败，请手动打卡")
                        self.wxpost("今天的打卡失败，请手动打卡")
                time.sleep(3)
                print("即将退出程序...")
                self.driver.quit()

        # 钉钉webhook机器人推送

    def ddpost(self, content):
        with open(self.config, encoding='utf-8') as f:
            configs = json.load(f)
        timenow = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        url = "https://oapi.dingtalk.com/robot/send?access_token=" + configs['ddkey']
        data = '{"msgtype":"markdown","markdown":{"title":"每日疫情打卡","text":"# 每日打卡提醒 \n >### 消息提示：' + \
                content + ' \n >### 打卡时间：' + timenow + '"}}'
        headers = {'Content-Type': 'application/json'}
        byte_data = data.encode("utf-8")
        rep = requests.post(url=url, data=byte_data, headers=headers)
        print("钉钉打卡成功")

        # 微信server酱机器人推送

    def wxpost(self, content):
        with open(self.config, encoding='utf-8') as f:
            configs = json.load(f)
        self.driver.get("https://sc.ftqq.com/" + configs['wxkey'] + ".send?text=" + content)
        print("微信打卡成功")
        
    def run(self):
        print('健康打卡程序启动')
        self.operate_dk()
            

   
        