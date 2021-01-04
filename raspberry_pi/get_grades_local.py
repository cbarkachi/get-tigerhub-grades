from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from time import sleep
import smtplib
import email
from config_local import Config
from sys import argv
import requests
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = None
wait = None

def send_email(msg_body):
    msg = email.message.EmailMessage()

    msg.set_content(msg_body)
    msg['Subject'] = Config.email_subject

    msg['From'] = Config.email_username
    msg['To'] = ", ".join(Config.recipients)

    server = smtplib.SMTP(Config.smtp_host, Config.smtp_port)
    server.starttls()
    server.login(Config.email_username, Config.email_password)
    server.send_message(msg)
    server.quit()


def initialize():
    print('Initializing')
    global driver
    global wait
    chrome_options = webdriver.chrome.options.Options()
    
    # For Mac/Linux, change the following path appropriately
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f'--user-data-dir={Config.chrome_path}')
    
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 20)

def login():
    print('Logging in...')
    driver.get('https://registrar.princeton.edu/tigerhub')
    login_button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'TigerHub Login')))
    login_button.click()
    driver.switch_to.window(driver.window_handles[-1])
    try:
        submit_button = wait.until(EC.element_to_be_clickable((By.NAME, 'submit')))
        submit_button.click()
    except:
        pass

def enter_portal():
    print("Entering grades portal...")
    view_grades_button = wait.until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, 'View Grades')))
    view_grades_button.click()


def view_grades():
    print("Viewing this year's grades...")
    this_year_button = wait.until(EC.element_to_be_clickable((By.XPATH, Config.term_xpath)))
    this_year_button.click()

def fetch_grades():
    print("Fetching grades...")
    class_rows_rendered = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="win0divTERM_CLASSES$grid$0"]/table/tbody/*')))
    class_rows = driver.find_elements_by_xpath('//*[@id="win0divTERM_CLASSES$grid$0"]/table/tbody/*')
    if not class_rows:
        raise Exception
    if Config.use_local:
        set_grades = get_local_grades()
        print(set_grades)
        if len(set_grades) == len(class_rows):
            # print("All grades have been logged.")
            send_email("All grades have been logged.")
            return
    for grade_row, class_row in enumerate(class_rows):
        class_name = wait.until(EC.element_to_be_clickable((By.id, f'CLASS${grade_row}'))).text.strip()
        if Config.use_local:
            if class_name in set_grades:
                continue
            cur_grade = check_grade(class_name, grade_row)
            if cur_grade:
                post_local_grade(class_name, cur_grade)
        elif class_name == Config.desired_class:
            if check_grade(class_name, grade_row):
                return
    sleep(Config.refresh_frequency)
    driver.refresh()
    check_grades_refresh()


def check_grade(class_name, grade_row):
    print("Checking grade...")
    cur_grade = wait.until(EC.element_to_be_clickable((By.id, f"STDNT_ENRL_SSV1_CRSE_GRADE_OFF${grade_row}"))).text.strip()
    if cur_grade:
        print(f"{class_name} posted: {cur_grade}")
        send_email(Config.email_message % (class_name, cur_grade))
        return cur_grade
    return None


def get_local_grades():
    set_grades = set(os.listdir('/home/pi/Desktop/get-tigerhub-grades-cloud/grades/'))
    return set_grades


def post_local_grade(class_name, cur_grade):
    with open('/home/pi/Desktop/get-tigerhub-grades-cloud/grades/' + class_name, 'w') as grade_file:
        grade_file.write(cur_grade)


def check_grades_refresh():
    enter_portal()
    view_grades()
    fetch_grades()


def check_grades():
    initialize()
    login()
    check_grades_refresh()


if __name__ == '__main__':
    send_email("in this bitch")
    try:
        check_grades()
    except Exception as e:
        send_email(str(e))
