import contextlib
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def get_after_pattern(string, pattern):
    return string.split(pattern)[1]

def build_dict(data):
    return dict(zip(["username", "url"], data))

def profile_search(name, remote_url="http://51.83.33.219:4432"):
    """
    It takes a name as an argument, searches for that name on Reddit, and returns a list of usernames, a
    list of urls, and a dictionary of usernames and urls
    
    :param name: the name of the user you want to search for
    :param remote_url: The url of the remote selenium server, defaults to http://51.83.33.219:4432
    (optional)
    :return: A list of usernames, a list of urls, and a dictionary of usernames and urls.
    """
    try:
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(
        command_executor=remote_url,
        options=chrome_options
        )
        url = f"https://www.reddit.com/search/?q={name}&type=user"
        driver.get(url)
        time.sleep(10)
        res = driver.find_elements(By.CLASS_NAME, "_2torGbn_fNOMbGw3UAasPl")
        keys = []
        usernames = []
        urls = []
        for index, element in enumerate(res):
            with contextlib.suppress(Exception):
                keys.append(f"profile {str(index + 1)}")
                username = get_after_pattern(element.text, "u/")
                usernames.append(username)
                urls.append(f"https://www.reddit.com/user/{str(username)}")
                if index >= 5:
                    break
        values = [build_dict([element, urls[index]]) for index, element in enumerate(usernames)]
        driver.quit()
        return usernames, urls, dict(zip(keys, values))
    
    except Exception:
        if driver:
            driver.quit()

