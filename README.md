# Linux无界面自动化打卡组合拳

   适用于Linux系统的苏大每日健康打卡的无界面打卡程序，按照下面操作自行设置即可，主代码修改自[
   EuGEne](https://blog.csdn.net/weixin_44739303/article/details/106245788)老哥，谢谢你

   如果是macOS或者Windows可以魔改本教程实现打卡

   ## Python pip安装selenium

   ```bash
pip install selenium
   ```

   ## CentOS 或其他版本Linux安装chrome

   ```bash
curl https://intoli.com/install-google-chrome.sh | bash
   ```

   ## 如果是macOS或windows

   自己手动下载chrome浏览器就行，如果早就安装了就不用管了，然后可以参考原作者的实现有界面打卡

   ## 下载Chrome-driver

   先查看chrome版本

   ```
google-chrome --version
   ```

   再下载对应版本的driver

   [http://npm.taobao.org/mirrors/chromedriver](http://npm.taobao.org/mirrors/chromedriver)上查地址

   复制一下链接地址

   然后拼接并解压

   ```bash
wget http://npm.taobao.org/mirrors/chromedriver/84.0.4147.30/chromedriver_linux
unzip chromedriver_linux64.zip
   ```

   ## 放入主程序

   新建一个`daka.py`的文件，这个地方修改了原作者的一些代码，主要在打开浏览器函数中作了修改

   ```python
   # -*- coding: utf-8 -*-
    
   from selenium import webdriver
   import time
   import json
   
   # 开启浏览器
   def openChrome():
       options = webdriver.ChromeOptions()
       options.add_argument('--no-sandbox') # 解决DevToolsActivePort文件不存在的报错
       options.add_argument('window-size=1600x900') # 指定浏览器分辨率
       options.add_argument('--disable-gpu') # 谷歌文档提到需要加上这个属性来规避bug
       options.add_argument('--hide-scrollbars') # 隐藏滚动条, 应对一些特殊页面
       options.add_argument('blink-settings=imagesEnabled=false') # 不加载图片, 提升速度
       options.add_argument('--headless') # 浏览器不提供可视化页面.linux下如果系统不支持可视化不加这条会启动失败
       options.add_argument('disable-infobars')
       driver = webdriver.Chrome(options=options,executable_path='./chromedriver')
       return driver
   
   def find(driver,str):
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
        url = "http://ids1.suda.edu.cn/amserver/UI/Login?goto=http%3a%2f%2fmyauth.suda.edu.cn%2fdefault.aspx%3fapp%3dsswsswzx2%26jumpto%3d&welcome=%e5%b8%88%e7%94%9f%e7%bd%91%e4%b8%8a%e4%ba%8b%e5%8a%a1%e4%b8%ad%e5%bf%83&linkName=%e5%a6%82%e6%9e%9c%e6%97%a0%e6%b3%95%e4%bd%bf%e7%94%a8%e7%bb%9f%e4%b8%80%e8%ba%ab%e4%bb%bd%e7%99%bb%e5%bd%95%ef%bc%8c%e8%af%b7%e7%82%b9%e5%87%bb%e8%bf%99%e9%87%8c&linkUrl=http://aff.suda.edu.cn/_web/ucenter/login.jsp&gx_charset=UTF-8"
        driver.get(url)
        # 找到输入框并输入查询内容
        elem = driver.find_element_by_id("IDToken1")
        elem.send_keys(config["学号"])
        elem = driver.find_element_by_id("IDToken9")
        elem.send_keys(config["密码"])
        # 提交表单
        driver.find_element_by_xpath("//*[@id='loginBtn']").click()
        try:
            driver.find_element_by_xpath("//*[text()='首页']")
        except:
            print('登陆失败！请检查学号密码是否正确')
            return -1
        else:
            print('登录成功！')
            url = "http://aff.suda.edu.cn/_web/fusionportal/detail.jsp?_p=YXM9MSZwPTEmbT1OJg__&id=2749&entranceUrl=http%3A%2F%2Fdk.suda.edu.cn%2Fdefault%2Fwork%2Fsuda%2Fjkxxtb%2Fjkxxcj.jsp&appKey=com.sudytech.suda.xxhjsyglzx.jkxxcj."
            driver.get(url)
            driver.find_element_by_xpath("//*[@class='action-btn action-do']").click()

            # 切换到小框内
            iframe1 = driver.find_element_by_id("layui-layer-iframe1")
            driver.switch_to.frame(iframe1)
            flag = False
            while(flag == False):
                time.sleep(1)
                flag = find(driver, "//*[text()='"+config["学号"]+"']")
            elem = driver.find_element_by_id("input_swtw")
            elem.send_keys("36.8")
            elem = driver.find_element_by_id("input_xwtw")
            elem.send_keys("36.8")    	
            driver.find_element_by_xpath("//*[@id='checkbox_jkzk35']").click()
            xrywz = {'在校': 'radio_xrywz5', '在苏州': 'radio_xrywz7',
                     '江苏省内其他地区': 'radio_xrywz9', '在其他地区': 'radio_xrywz23'}
            driver.find_element_by_xpath(
                "//*[@id='"+xrywz[config["现人员位置"]]+"']").click()
            elem = driver.find_element_by_id("input_jtdz")
            elem.send_keys(config["家庭地址"])
            driver.find_element_by_xpath("//*[@id='radio_sfyxglz29']").click()

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

   ```

   保存，然后在同目录下新建一个`config.json`文件用来存放个人信息，自行修改即可，注意人员位置只可以填写以下四项中的任意一项：‘留校’, ‘在苏州’, ‘江苏省内其他地区’, ‘在其他地区’

   ```json
   {
       "学号": "xxxxxx",
       "密码": "xxxxxx",
       "现人员位置": "江苏省内其他地区",
       "家庭地址": "home",
       "ddkey":"钉钉webhook的accesskey",
       "wxkey":"server酱的accesskey"
   }
   ```

   ## 运行

   最后python3 data.py即可自动打卡

   ![image-20200723074142728](https://imgconvert.csdnimg.cn/aHR0cHM6Ly90dmExLnNpbmFpbWcuY24vbGFyZ2UvMDA3UzhaSWxneTFnaDBrYnl6ZG1tajMxYTIwZDRuNGQuanBn?x-oss-process=image/format,png)

   可以通过定时任务来自动化进行打卡操作

   ## 自动推送

   可以在打卡成功后自定义推送给自己的邮箱或者qq微信来实现推送功能
   如果需要自动打卡，可以在config.json文件中的ddkey当中填写你申请的钉钉webhook机器人accesskey

![image-20200808103315685](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghj77cpgjdj30ci04u0t5.jpg)   

或在wxkey当中填写微信server酱公众号的accesskey

![image-20200808103329886](https://tva1.sinaimg.cn/large/007S8ZIlgy1ghj77lggymj30d7062gmm.jpg)

这样均可以实现自动化打卡

## 更新

0730 更新打卡的地址

0808 新增自动推送

0824 更新温度打卡

   ## 致谢名单

   1. [CentOS7下无界面使用Selenium+chromedriver进行自动化测试](https://blog.csdn.net/pengjunlee/article/details/91997908?)

   2. [自动健康打卡程序](https://blog.csdn.net/weixin_44739303/article/details/106245788)

   3. [INSTALLING GOOGLE CHROME ON CENTOS, AMAZON LINUX, OR RHEL](https://intoli.com/blog/installing-google-chrome-on-centos/)

   4. [MAC安装chromedriver提示“Message: 'chromedriver' executable needs to be in PATH.”](https://blog.csdn.net/walter_chan/article/details/50464625)