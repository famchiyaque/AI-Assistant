from selenium import webdriver
import webbrowser
import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

spotify_buttons = {
    "pause": "pause-play",
    "back": "song-back",
    "next": "song-next",
    "play": "pause-play"
}

driver_instance = None

def get_driver():
    global driver_instance
    if driver_instance is None:
        driver_instance = webdriver.Edge()
        driver_instance.get("http://localhost:7768")
        time.sleep(3)
    return driver_instance

def execute_command(driver, command):
    try:
        inactive_element = driver.find_element(By.ID, 'inactive')
        if inactive_element:
            print("inactive p found")
            return "instance not active"
    except NoSuchElementException:
        pass  # 'inactive' element not found, proceed with the rest of the logic

    try:
        button = driver.find_element(By.ID, spotify_buttons[command])
        if button:
            print("correct button found, being clicked")
            button.click()
    except NoSuchElementException:
        print("inactive not found, neither the button, terminating driver")
        return "Button not found for command: " + command
      

def spotify_player(command):
    print("entered spotify player function")
    driver = get_driver()

    time.sleep(3)
    curr_url = driver.current_url
    print("curr url: ", curr_url)
    
    if '/auth/callback' in curr_url:
        execute_command(driver, command)
    else:
        try:
            login_btn = driver.find_element(By.ID, 'login-btn')
            if login_btn:
                print("login button found")
                login_btn.click()
                time.sleep(3)
        except NoSuchElementException:
            pass
        
        result = execute_command(driver, command)
        if result:
            return result