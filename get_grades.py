from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from time import sleep
import smtplib
import email
from config import Config
from sys import argv
import requests
import json

driver = None

def repeatedly_try(function):
    def wrapper(*args, **kwargs):
        result = None
        while True:
            try:
                result = function(*args, **kwargs)
                break
            except Exception as e:
                print(str(e))
                sleep(1)
        return result
    return wrapper
    

def send_email(class_name, cur_grade):    
    msg = email.message.EmailMessage()

    msg.set_content(Config.email_message % (class_name, cur_grade))
    msg['Subject'] = Config.email_subject

    msg['From'] = Config.email_username
    msg['To'] = ", ".join(Config.recipients)

    server = smtplib.SMTP(Config.smtp_host, Config.smtp_port)
    server.starttls()
    server.login(Config.email_username, Config.email_password)
    server.send_message(msg)
    server.quit()

def initialize():
    global driver
    options = webdriver.chrome.options.Options()
    # For Mac/Linux, change the following path appropriately
    options.add_argument(Config.chrome_path)
    driver = webdriver.Chrome(options=options)


def login():
    driver.get('https://registrar.princeton.edu/tigerhub')
    login_button = driver.find_element_by_xpath('//*[@id="block-registrar-content"]/article/div/div/div/div/div[1]/div/p[3]/a')
    login_button.click()

    driver.switch_to.window(driver.window_handles[-1])

    try:
        submit_button = driver.find_element_by_name("submit")
        submit_button.click()
    except:
        pass

@repeatedly_try
def enter_portal():
    view_grades_button = driver.find_element_by_link_text(
        "View Grades")
    view_grades_button.click()

@repeatedly_try
def view_grades():
    this_year_button = driver.find_elements_by_xpath(Config.term_xpath)[0]
    this_year_button.click()

@repeatedly_try
def fetch_grades():
    class_rows = driver.find_elements(By.XPATH, '//*[@id="win0divTERM_CLASSES$grid$0"]/table/tbody/*')
    if not class_rows:
        raise Exception
    if Config.use_database:
        set_grades = get_database_grades()
        if len(set_grades) == len(class_rows):
            print("All grades have been logged.")
            return
    for grade_row, class_row in enumerate(class_rows):
        class_name = driver.find_element_by_id(f'CLASS${grade_row}').text.strip()
        if Config.use_database:
            if class_name in set_grades:
                continue
            cur_grade = check_grade(class_name, grade_row)
            if cur_grade:
                post_database_grade(class_name, cur_grade)
        elif class_name == Config.desired_class:
            if check_grade(class_name, grade_row):
                return
    sleep(Config.refresh_frequency)
    driver.refresh()
    check_grades()

@repeatedly_try
def check_grade(class_name, grade_row):
    cur_grade = driver.find_element_by_id(f"STDNT_ENRL_SSV1_CRSE_GRADE_OFF${grade_row}").text.strip()
    if cur_grade:
        print(f"{class_name} posted: {cur_grade}")
        send_email(class_name, cur_grade)
        return cur_grade
    return None

def get_database_grades():
    url = Config.database_url
    headers = Config.headers

    response = requests.get(url, headers=headers)

    classes = json.loads(response.content)
    set_grades = {row['class_name'] for row in classes}
    return set_grades

def post_database_grade(class_name, cur_grade):
    url = Config.database_url
    payload = json.dumps( {'class_name': class_name, 'class_grade': cur_grade} )
    headers = Config.headers

    response = requests.post(url, data=payload, headers=headers)

def check_grades():
    enter_portal()
    view_grades()
    fetch_grades()

if __name__ == '__main__':
    initialize()
    login()
    check_grades()