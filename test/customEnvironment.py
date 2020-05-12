import gym
from gym import spaces
from gym.utils import seeding
from appium import webdriver
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.webdriver.common.touch_action import TouchAction
from subprocess import Popen, PIPE
import time
import random
import os

max_reward = 100

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

deviceName = "emulator-5554"
package_name = 'com.example.myapplication'
search_activity = '.MainActivity'

class CustomEnv(gym.Env):
    appPackage = 'com.example.myapplication'
    search_activity = '.MainActivity'
    app_path_string = '../apps/app-debug.apk'
    app_path = os.path.abspath(app_path_string)

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
    
    currentActivity = driver.current_activity

    def __init__(self,df):

        super(CustomEnv,self).__init__()
        self.reward_range = (0,max_reward)
        self.action_space = spaces.Discrete(10)
        self.observation_space = spaces.Discrete(4)

        if self.currentActivity == '.MainActivity':
            self.state = 0
        elif self.currentActivity == '.Main2Activity':
            self.state = 1
        elif self.currentActivity == '.Main3Activity':
            self.state = 2
        else:
            self.state = 3
        
 

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def reset(self):
        get_current_window_cmd = "dumpsys window windows | grep -E mCurrentFocus"
        p = Popen(["adb","-s",deviceName,"shell",get_current_window_cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
        output, err = p.communicate() 
        output = output.decode("utf-8").split('/')
        main_activity = output[1][:-2]

        activity_count = 0
        print(main_activity)
        

        self.state = 0
        
        return self.state

    def getAction(self,deviceName,package_name,actions):
        
        #get clickable elements
        Clickable_Elements = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
        #implicitly_wait timeout reset
        # if (len(Clickable_Elements) == 0):
        #   driver.reset()
        Textinput_Elements = []
        for element in Clickable_Elements:
            if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == 'true':
                        Textinput_Elements.append(element)

        Clickable_Elements = list(set(Clickable_Elements) - set(Textinput_Elements))
        print(Clickable_Elements)  
        print(Textinput_Elements)
        return Textinput_Elements,Clickable_Elements

    def step(self, action):
        assert self.action_space.contains(action)
        (Textinput_Elements,Clickable_Elements,Total_Elements) = self.getAction(deviceName,package_name,10)
        action_to_perform = Total_Elements[action] 
        element = action_to_perform
        #IF ACTION TO PERFORM IS A TEXT BOX FILL IN TEXT BOX
        if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == 'true':
            resource_id = element.get_attribute("resource-id")
            # print(resource_id)
            #fill username with unique value
            # text_field_element.send_keys(Unspecified_text)
            for pii in PII:
              if pii in resource_id.lower():
                element.click()
                element.send_keys(PII[pii])
        #ELSE IF ACTION TO PERFORM IS A BUTTON CLICK BUTTON
        else: element.click()
        activity = self.driver.current_activity
        print(activity)
        self.state = activity
        return activity