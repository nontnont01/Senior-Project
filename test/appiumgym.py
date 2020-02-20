from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from subprocess import Popen, PIPE

import time
import random
import os

start_time = time.time()
#3-20 char a-zA-Z0-9 
Unique_username = "Sylphsgt098VWE"
# 8-... a-zA-Z0-9 
Unique_password = "u8zvTBYNnnGn"
Email = "nont.platong@@gmail.com"

Unspecified_text = "YaaKcuMEgEsr"

PhoneNo = ""
firstname = ""
lastname = ""
Country = "Thailand"
Province = "Bangkok"
DOB = ""
Search = "Mark"


PII = {"email" : Email,
"user" : Unique_username,
"pass" : Unique_password,
"pwd" : Unique_password,
"pword" : Unique_password,
"phoneno" : PhoneNo,
"firstname" : firstname,
"lastname" : lastname,
"country" : Country, 
"province" : Province, 
"dob" : DOB,
"search" : Search}

def perform_random_user_event(deviceName,package_name, actions):
    appPackage = 'io.appium.android.apis'
    search_activity = '.app.SearchInvoke'
    app_path = os.path.abspath('../apps/ApiDemos-debug.apk')
  #setup devices
    desired_caps = {
    "deviceName" : deviceName,
    "platformName": "Android",
    "udid": deviceName,
    "version": "8.1.0",
    "appActivity" : search_activity,
    "appPackage" : appPackage,
    "app" : app_path,
    "autoGrantPermissions" : "true",
    "gpsEnabled" : "true"
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_caps)
    get_current_window_cmd = "dumpsys window windows | grep -E mCurrentFocus"
  # driver.implicitly_wait(15)
  #get app activity
    p = Popen(["adb","-s",deviceName,"shell",get_current_window_cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
    output, err = p.communicate() 
    output = output.decode("utf-8").split('/')
    main_activity = output[1][:-2]
    activity_count = 0
    print(main_activity)

    for count in range(actions):
    # print(count)
    #check if the application is running?
        package = driver.current_package
        if(package != appPackage):
            print("not running the app >>>>>> reset")
            activity_count = 0
            driver.reset()
        else:
        #reset if activity struck (to increase code coverage)
        # driver.implicitly_wait(10)
            if (activity_count >= 30):
                print("activity struck >>>>>> reset")
                driver.reset()
                activity_count = 0
                prev_activity = main_activity
        #perform random user interaction  
            else:
                prev_activity = driver.current_activity
            # driver.implicitly_wait(10)
            #get clickable elements
                Clickable_Elements = driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
            #implicitly_wait timeout reset
            # if (len(Clickable_Elements) == 0):
            #   driver.reset()
                Textinput_Elements = []
                for element in Clickable_Elements:
                    if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == 'true':
                        Textinput_Elements.append(element)

                Clickable_Elements = list(set(Clickable_Elements) - set(Textinput_Elements))
                #print(Clickable_Elements)  
                print(Textinput_Elements)

deviceName = "emulator-5554"
package_name = 'io.appium.android.apis'
perform_random_user_event(deviceName,package_name,100)