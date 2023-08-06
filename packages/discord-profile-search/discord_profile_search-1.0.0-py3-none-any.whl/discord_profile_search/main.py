import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
import time




def profile_search(search, remote_url='http://54.36.177.119:4450'):
    """
    It takes a search term, and returns a list of usernames, a list of urls, and a dictionary of
    usernames and urls.
    
    :param search: The username you want to search for
    :param remote_url: The url of the remote webdriver, defaults to http://54.36.177.119:4450 (optional)
    :return: A list of usernames, a list of urls, and a dictionary of usernames and urls
    """

    try:
        
       # Opening a webdriver, and going to the url.
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=remote_url, options=chrome_options)
        url = f"https://discordhub.com/user/search?csrf_token=ImNkOTI3YzYyN2IzYWNhNjkzYjE2MWRhNmUzYjgwOTcxMmI0NzU3MGUi.YwyNew.wHSXOdsk77obQuXD7fbH1bXjEFs&user_search_bar={search}"        
        driver.get(url)
        time.sleep(2)


        # A list comprehension that is getting the text of all the elements with the class name "title"
        usernames = [element.text for element in driver.find_elements(By.CLASS_NAME, "title")]      
        
        # Getting the href attribute of all the elements with the xpath //h4[@class="title"]/a
        urls = [element.get_attribute('href') for element in  driver.find_elements_by_xpath('//h4[@class="title"]/a')]        
        
        # Creating a dictionary of usernames and urls.
        values = [{"username": username, "url": url} for username, url  in zip(usernames, urls)]   
        keys = [f"profile {str(index + 1)}" for index, _ in enumerate(usernames)]
        profiles_dict = dict(zip(keys, values))
        
        # It closes the webdriver.
        driver.quit()
        
        # Logging the search term that was used.
        logging.info(f"Search on twitch for {search} has been done")
        
        # Returning a list of usernames, a list of urls, and a dictionary of usernames and urls.
        return usernames, urls, profiles_dict
    
    except Exception as e:
       # Logging the error and the search term that was used.
        logging.error(e)
        logging.error(f"Search on twitch for {search} has failed")
        driver.quit()


#print(profile_search("Emmanuel macron"))
