from appium import webdriver
import time
import requests
import json
des_leidian = {
                "platformName": "Android",#设备系统
                "deviceName": "2e1bd4f97d84",#设备名称，adb devices查看
                "platformVersion": "7.1.2",#手机或模拟器的版本号
                "appPackage": "com.android.browser",#apk包名
                "appActivity": "com.android.browser.BrowserActivity",#打开的进程名
                "noReset": True,
                "udid": "2e1bd4f97d84",   # 识别手机唯一标识
                'unicodeKeyboard': True,   # appium自带键盘
                'resetKeyboard': True,     # 解决中文乱码问题
                'noSign': True,
                "automationName": "Uiautomator2",  # toast 必须用Uiautomator2
                "autoGrantPermissions": True
                }

des_yeshen = {
                "platformName": "Android",
                "deviceName": "5de12c08",
                "platformVersion": "6.0.1",
                "appPackage": "com.mmc.feelsowarm",
                "appActivity": "com.mmc.feelsowarm.WelcomeActivity",
                "noReset": True,
                "udid": "5de12c08",   # 识别手机唯一标识
                "automationName": "Uiautomator2",  # toast 必须用Uiautomator2
                "autoGrantPermissions": True,
                'unicodeKeyboard': True,   # appium自带键盘
                'resetKeyboard': True,     # 解决中文乱码问题
                }

def dingding(e):

    """
         通过钉钉进行报警消息推送
         :param e:报错信息
         :return: 无
    """
    # 获取当前时间
    ticks=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    # text参数必须是str类型，所以需要转化数据格式
    text = str(ticks+"\n"+"测试结果："+"测试不通过\n"+"报错信息："+str(e))
    # 钉钉机器人推送信息接口，不同机器人access_token不同，目前为数据智能中心监控告警机器人
    url='https://oapi.dingtalk.com/robot/send?access_token=b110a5c9050fd5ed76682fc47563a01442306d7dc938a66f0e9ecd68d73c2fcf'
    program={
     "msgtype": "text",
     "text": {"content":text},
    }
    headers={'Content-Type': 'application/json'}
    f=requests.post(url,data=json.dumps(program),headers=headers)
    print("钉钉返回信息：",f.text)

def search(deviceName = "leidian", port = 4723):
    try:
        '''启动app'''

        if deviceName == "leidian":
           des = des_leidian
        elif deviceName == "yeshen":
           des = des_yeshen
        else:
           des = des_leidian
        driver = webdriver.Remote('http://127.0.0.1:%s/wd/hub' % port, des)
       #driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub' , des)

        '''打开自带浏览器-点击搜索输入框-输入访问链接-点击访问上报ip-返回首页'''
        ticks=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))  # 获取当前时间
        print("打开浏览器当前时间戳为:", ticks)
        driver.find_element_by_id("com.android.browser:id/search_hint").click()  # 点击输入栏
        time.sleep(5)
        driver.find_element_by_id("com.android.browser:id/url").send_keys('https://cs.lingjisuanming.cn/api/test?report_ip=1') # 输入链接
        time.sleep(5)
        driver.find_element_by_id("com.android.browser:id/rightBtn").click() # 点击访问
        time.sleep(3)
        driver.back()
        print("访问成功！")
        time.sleep(5)
        driver.quit()
        print("关闭浏览器！")
    except Exception as e:
        # 抛异常钉钉告警
            dingding(e)
            print(e)

def run(interval=3600):
    # 设置每隔一小时执行一次方法
    while True:
        try:
            time_remaining = interval-time.time()%interval
            search()
            print("下次执行时间为 %s (%s seconds)..."%((time.ctime(time.time()+time_remaining)), time_remaining))
            time.sleep(time_remaining)
        except Exception as e:
            # 抛异常钉钉告警
            dingding(e)
            print(e)

if __name__=="__main__":
    run()
