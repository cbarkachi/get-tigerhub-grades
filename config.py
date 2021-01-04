class Config:
    pass


class Config:
    # /Selenium settings/

    # The path below is for Windows. Modify accordingly for Mac.
    chrome_path = r"user-data-dir=C:\Users\[YOUR_USERNAME]\AppData\Local\Google\Chrome\User Data"

    # /Email Settings/

    email_username = 'cbarkachi@gmail.com'
    # need to supply an app password for EMAIL_PASSWORD if using gmail
    email_password = 'PASSWORD_HERE'
    recipients = ['cbarkachi@gmail.com', '123456789@tmomail.net']
    email_subject = 'TigerHub grade available'
    email_message = 'Try-hard: your grade in %s (%s) is now available on TigerHub.'
    smtp_host = 'smtp.gmail.com'
    smtp_port = 587

    # /TigerHub settings/

    # This has to do with the page where you select a term (e.g. 2020-2021 Fall).
    # Find the appropriate xpath with Chrome Inspect Element
    term_xpath = '//*[@id="TERM_GRID$0_row_1"]'
    # How often, in seconds, TigerHub will be checked
    refresh_frequency = 3600

    # / Database settings /
    use_database = True

    # If you're not using an API-based database, you must specify which class you'd like to be notified about.
    # Use the "Class" column on TigerHub
    desired_class = "COS 340"

    # If you are using a database, modify the information below accordingly
    database_api_key = "DB_API_KEY"
    headers = {
        'content-type': "application/json",
        'x-apikey': database_api_key,
        'cache-control': "no-cache"
    }
    database_url = "DB_URL"
