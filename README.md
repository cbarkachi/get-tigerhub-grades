# get-tigerhub-grades

Fetches your grades from Tigerhub and notifies you by email and text each time any of them have been updated by your professor.

Note: Depends on TigerHub auth cookies, meaning if for whatever reason you've disabled cookies in Chrome, this won't work.

See https://github.com/cbarkachi/enroll-in-tigerhub-courses for a similar project with a cleaner Selenium setup (and one with an actual requirements.txt file 😎). Instead of using the repeatedly_try decorator I have here to catch errors related to finding elements, I use Selenium's built-in WebDriverWait module to programmatically wait for elements to appear and be "clickable".

As with the enroll-in-tigerhub-courses repo, you need the latest version of the Chrome web driver for this to work. The included driver in this repo is only for Windows, and not updated of course. Find the latest version for your platform [here](https://chromedriver.chromium.org/downloads).

## Database note

The point of the database setup is so that the module can be deployed to the cloud and run from there on a cron job and without any local storage (e.g. with AWS Lambda). If you'd rather not use an API-based database as I did here, you can also just use a local storage-based approach. A simple Raspberry Pi-based approach can be found in the raspberry_pi directory with the Linux version of the Chromium web driver included.
