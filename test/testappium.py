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

Email = "boomngongseniorproject@gmail.com"

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


#get clickable elements
# Clickable_Elements = driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")



# ele


#Test 1000 randomly click action

def perform_random_user_event(deviceName,package_name, actions):
  #appPackage = package_name[6:]
  #appPackage = 'io.appium.android.apis'
  appPackage = 'com.example.myapplication'
  search_activity = '.MainActivity'
  app_path = os.path.abspath('../apps/app-debug.apk')
  #setup devices
  desired_caps = {
    "deviceName" : deviceName,
    #"deviceName" : "emulator-5554",
    "platformName": "Android",
    "udid": deviceName,
    "version": "8.1.0",
    #"appActivity" : "aarddict.android.DictionariesActivity",
    "appActivity" : search_activity,
    "appPackage" : appPackage,
    "app" : app_path,
    #"app" : "/Users/lemonn/SeniorProject/AndroidStorage/CoverageAPK/instr/" + package_name + ".apk",
    "autoGrantPermissions" : "true",
    "gpsEnabled" : "true"
  }

  #driver = webdriver.Remote("http://0.0.0.0:4724/wd/hub", desired_caps)
  driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', desired_caps)
  get_current_window_cmd = "dumpsys window windows | grep -E mCurrentFocus"
  # driver.implicitly_wait(15)
  #get app activity
  p = Popen(["adb","-s",deviceName,"shell",get_current_window_cmd], stdin=PIPE, stdout=PIPE, stderr=PIPE) 
  output, err = p.communicate() 
  rc = p.returncode
  output = output.decode("utf-8").split('/')
  main_activity = output[1][:-2]
  


  #print(main_activity)

  window_size = driver.get_window_size()
  #print(window_size)
  activity_count = 0


#######################################################################################
# perform user interaction
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
        activity = driver.current_activity
        print(activity)
        print('1 =')
        print(Clickable_Elements)
        #time.sleep(5)
        #print(driver.page_source)

        Textinput_Elements = []
        for element in Clickable_Elements:
          if element.get_attribute("class") == "android.widget.EditText" and element.get_attribute("focusable") == 'true':
            Textinput_Elements.append(element)

        Clickable_Elements = list(set(Clickable_Elements) - set(Textinput_Elements))
        print('2 =')
        print(Clickable_Elements)


#iMonkey
        #random action 0,1,2,3,4
        if (len(Clickable_Elements) == 0):
          random_action = random.randrange(2,4)
        elif (len(Textinput_Elements) == 0):
          random_action = random.randrange(1,3)
        else:
          random_action = random.randrange(3)


        #0, filled a random text field | or fill all ?
        if(random_action == 0):
          temp = random.randrange(len(Textinput_Elements))


          for text_field_element in Textinput_Elements:
            resource_id = text_field_element.get_attribute("resource-id")
            # print(resource_id)
            #fill username with unique value
            # text_field_element.send_keys(Unspecified_text)
            for pii in PII:
              if pii in resource_id.lower():
                text_field_element.click();
                text_field_element.send_keys(PII[pii]);




        #1 randomly click on clickable element
        elif (random_action == 1):
          temp = random.randrange(len(Clickable_Elements))
          Clickable_Elements[temp].click()



#Monkey
        #swipe randomly (4 direction)
        elif (random_action == 2):
          height = window_size['height']
          width = window_size['width']

          temp = random.randrange(3)
          

          #driver.swipe(startX, startY, endX, endY, duration)
          if temp == 0:
            driver.swipe(width/2, height/2, width/2, height/4, 400)
          if temp == 1:
            driver.swipe(width/2, height/2, width/2,  height*3/4, 400)
          if temp == 2:
            driver.swipe(width/2, height/2, width/4, height/4, 400)
          if temp == 3:
            driver.swipe(width/2, height/2, width*3/4, height/4, 400)


          #system level event ('back button' for now)
        elif (random_action == 3):
          driver.press_keycode(4)


        elif (random_action == 4):
          temp_x = random.randrange(100)
          temp_y = random.randrange(100)

          coor_x = window_size["width"] * temp_x /100
          coor_y = window_size["height"] * temp_y/100

          TouchAction(driver).press(x=coor_x, y=coor_y).perform()
        # print("Random number between 0 and 10 : ", random.randrange(10))
        #click randomly
        

        curr_activity = driver.current_activity

        if(curr_activity == prev_activity):
          activity_count+= 1

  print("\n")
  #print(str(actions) +" actions --- %s seconds ---" % (time.time() - start_time))
  driver.quit()


#package_name = "instr_aarddict.android"
deviceName = "emulator-5554"
#package_name2 = 'io.appium.android.apis'
package_name2 = 'com.example.myapplication'



perform_random_user_event(deviceName,package_name2,100)








#test application "zti.zealtech.doa"
#1000 actions --- 2175.314507961273 seconds ---  >> 35 mins
# 500 actions --- 1044.3399090766907 seconds --- >> 17 mins
# 100 actions --- 185.88411283493042 seconds --- >> 3  mins


#APK_path = "/Users/lemonn/SeniorProject/AndroidStorage/CoverageAPK/instr/instr_aarddict.android.apk"







