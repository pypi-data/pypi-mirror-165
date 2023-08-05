import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def replace_spaces(string):
    """
    It replaces all spaces in a string with periods
    
    :param string: The string to be modified
    :return: The string with all spaces replaced with periods.
    """
    return string.replace(" ", ".")

def profile_search(search, remote_url="http://51.83.33.219:4432"):
    """
    It opens a browser, goes to the quora search page, finds the elements with the class name "q-box
    qu-color--blue_dark qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0
    dxHfBI" and "q-text qu-bold", and returns the urls and usernames of the profiles
    
    :param search: The search term you want to search for
    :return: A list of usernames, a list of urls, and a dictionary of profiles.
    """
    try:
        # Opening a browser and going to the quora search page.
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=remote_url, options=chrome_options)
        url = f"https://www.quora.com/search?q={search}&type=profile"
        driver.get(url)
        time.sleep(2)
        
        # Finding the elements with the class name "q-box qu-color--blue_dark qu-cursor--pointer
        # qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 dxHfBI" and "q-text qu-bold"
        urls_selector = driver.find_elements_by_class_name(replace_spaces("q-box qu-color--blue_dark qu-cursor--pointer qu-hover--textDecoration--underline Link___StyledBox-t2xg9c-0 dxHfBI"))
        usernames_selector = driver.find_elements_by_class_name(replace_spaces("q-text qu-bold"))

        urls = [element.get_attribute("href") for element in urls_selector]
        usernames = [element.text for element in usernames_selector]
        usernames = usernames[1:]
        profiles = [f"profile {str(index + 1)}" for index, _ in enumerate(usernames)]
        profiles = [f"profile {str(index + 1)}" for index, _ in enumerate(usernames)]
        values = [{"username": username, "url": url} for username, url in zip(usernames, urls)]

        profiles_dict = dict(zip(profiles, values))
        driver.quit()
        logging.info(f"Search on quora for {search} has been done")
        return usernames, urls, profiles_dict
    
    except Exception as e:
        logging.error(f"Search on quora for {search} has failed")
        driver.quit()

#print(profile_search("Emmanuel macron"))