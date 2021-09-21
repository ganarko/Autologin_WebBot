import os,json,logging
from sys import exit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# System Requirement
import pyautogui as pag
# import webbrowser


APP_DIR = os.path.expanduser("~")+"/Apps/Web_Bot/"

config_file = APP_DIR + "sample.json"
log_file = APP_DIR + "std.log"
driver_path = APP_DIR+"drivers/geckodriver"

logging.basicConfig(filename= log_file, format='%(asctime)s | %(message)s', filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def main():

    site, url, username, password, username_field, password_field, login, logout, condition = set_config()

    login_bot(site, url, username, password, username_field, password_field, login, logout, condition)

    logger.info("Completed Run, Successfully")

    if HEADLESS=="yes":
        pag.alert(text="Process Completed Successfully, In Background", title="WebBot Success")
        # webbrowser.open(FINAL_END_POINT)
        exit(1)

    logger.info("Terminated")
    exit(1)

def login_bot(site, url, user, passwd, userField, passwordField, signin, signout, condition):

    if not os.path.exists(driver_path):
        pag.alert(text="No Firefox Driver Found in: /drivers/ Directory", title="Driver Not Found")
        exit(0)

    if HEADLESS=="yes":
        firefoxOptions = Options()
        firefoxOptions.add_argument("-headless")
        driver = webdriver.Firefox(executable_path=driver_path, options=firefoxOptions)
    else:
        driver = webdriver.Firefox(executable_path=driver_path)

    try:
        driver.get(url)
        username = driver.find_element_by_name(userField)
        password = driver.find_element_by_name(passwordField)
        login = ''
        try:
            login = driver.find_element_by_xpath("//input[@type='submit']")
        except Exception:
            try:
                login = driver.find_element_by_name(signin)
            except Exception:
                login = driver.find_element_by_id(signin)

        username.send_keys(user)
        password.send_keys(passwd)

    except Exception:
        pag.alert(text="Not able to parse webpage using driver", title="WebPage Load error")
        logger.info("Not able to Get WebSite/Web Elements")
        logger.info("Terminated")
        exit(0)

    if (condition == "True"):
        logger.info("Logging In")
        # login.click()
        logger.info("Logged In")
    elif (condition == "False"):
        logout = driver.find_element_by_id(signout)
        logger.info("Logging Out")
        # logout.click()
        logger.info("Logged Out")
    else:
        logger.info("No Condition identified, Logging In")
        # login.click()
        return

    logger.info("Condition was identified")

    # change_condition(site,condition)

def change_condition(site,condition):

    conf = open(config_file, "r")
    config = dict(json.load(conf))
    config["websites"][site]["condition"] = str(not condition)
    jsonString = json.dumps(config)
    conf.close()

    jsonFile = open(config_file, "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    logger.info("Changed Sign-IN/OUT Condition")

def set_config():

    if not os.path.exists(config_file):
        logger.warning("NO Config Found")
        pag.alert(text="Config File Not Found in: home/Apps/WebBot/ \n Make sure config.json exists",
                  title="No Config File")
        logger.warning("Terminated")
        exit(0)


    conf = open(config_file, 'r')
    config = dict(json.load(conf))

    try:
        site_to_use = config["site-to-used"]
        site_config = config["websites"][site_to_use]

        msg = "Site in use " + site_to_use
        logger.info(msg)

        global HEADLESS
        HEADLESS = site_config["headless"]
        if "dashboard" in site_config.keys() and site_config["dashboard"] != "null":
            global FINAL_END_POINT
            FINAL_END_POINT = site_config["dashboard"]

        # Site Url from Site Object in Sample Config File
        url = site_config["url"]

        # Credentials for that Site from Site Object
        username = site_config["username"]
        password = site_config["password"]
        # More Secure way is to get Password over runtime from a Dynamic Command
        # pass_command = site_config["password_cmd"] example: pass Browserstack/password (pass tool in Ubuntu)
        # password =subprocess.getoutput(pass_command)

        # Field paramaters of the Web Page to be logged/Signed in
        username_field = site_config["username_field"]
        password_field = site_config["password_field"]
        login = site_config["login_button"]
        logout = site_config["logout_button"]
        condition = site_config["condition"]

        logger.info("Site Config Options were Set")

    except Exception:
        logger.warning("Bad Format Config File")
        pag.alert(text="Invalid/Bad Format Config File \n in: home/Apps/WebBot/config.json", title="Bad Config File")
        logger.warning("Terminated")
        exit(0)

    conf.close()

    return (site_to_use, url, username, password, username_field, password_field, login, logout, condition)


if __name__ == '__main__':
    main()
