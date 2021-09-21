import os,json,logging
from sys import exit
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
# System Requirement
import pyautogui as pag
import webbrowser


APP_DIR = os.path.expanduser("~")+"/Apps/WebBot/"

config_file = APP_DIR + "config.json"
log_file = APP_DIR + "std.log"
driver_path = APP_DIR+"drivers/geckodriver"

HEADLESS = "no"
FINAL_END_POINT = ""
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
        pag.alert(text="No Firefox Driver Found in: home/Apps/WebBot/drivers/", title="Driver Not Found")
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
        condition = True
    elif (condition == "False"):
        condition = False
    else:
        logger.info("No Condition identified, Logging In")
        login.click()
        return

    logger.info("Condition was identified")

    if condition:
        logger.info("Logging In")
        login.click()
        logger.info("Logged In")
    else:
        logout = driver.find_element_by_id(signout)
        logger.info("Logging Out")
        logout.click()
        logger.info("Logged Out")

    change_condition(site,condition)


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
        site_to_used = config["site-to-used"]
        site_config = config["websites"][site_to_used]

        msg = "Site in use " + site_to_used
        logger.info(msg)

        global HEADLESS
        HEADLESS = site_config["headless"]
        if HEADLESS=="yes":
            global FINAL_END_POINT
            FINAL_END_POINT = site_config["dashboard"]


        url = site_config["url"]
        username = site_config["username"]
        password = site_config["password"]
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

    return (site_to_used,url,username,password,username_field,password_field,login,logout,condition)


if __name__ == '__main__':
    main()
