class Config:
    # /Selenium settings/

    chrome_path = r"/home/pi/.config/chromium"

    # /Email Settings/

    email_username = 'YOUR EMAIL'
    # need to supply an app password for EMAIL_PASSWORD if using gmail
    email_password = 'YOUR PASSWORD'
    recipients = ['trump@whitehouse.gov', '123456789@tmomail.net']
    email_subject = 'TigerHub grade available'
    email_message = 'Try-hard: your grade in %s (%s) is now available on TigerHub.'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587

    # /TigerHub settings/

    # This has to do with the page where you select a term (e.g. 2020-2021 Fall).
    # Find the appropriate xpath with Chrome Inspect Element
    term_xpath = '//*[@id="TERM_GRID$0_row_1"]'
    # How often, in seconds, TigerHub will be checked
    refresh_frequency = 600

    # / Local storage settings /
    use_local = True

    # If you'd only like to be informed about one class, you must specify it here
    # Use the "Class" column on TigerHub
    desired_class = "COS 340"