import contextlib
from selenium import webdriver
import time
from selenium.webdriver.common.by import By


def add_extension(list_of_strings, prefix="https://", suffix=".tumblr.com"):
    """
    > It takes a list of strings, and returns a new list of strings with a prefix and suffix added to
    each string
    
    :param list_of_strings: a list of strings
    :param prefix: the prefix to add to the beginning of each string, defaults to https:// (optional)
    :param suffix: the string to add to the end of each string in the list, defaults to .tumblr.com
    (optional)
    :return: A list of strings
    """
    return [f"{prefix}{string}{suffix}" for string in list_of_strings]

def build_dict(data):
    """
    It takes a list of four elements and returns a dictionary with four keys and four values
    
    :param data: a list of lists, each list containing the data for a single row
    :return: A dictionary with the keys "username", "description", "image", and "url"
    """
    return dict(zip(["username", "description", "image", "url"], data))

def profile_search(
    name,
    remote_url="http://54.36.177.119:4450",
    credentials=None,
):
    """
    It takes a name as an input, searches for it on tumblr, and returns a dictionary of the profiles
    that it finds
    
    :param name: The name of the person that you want to search for
    :param remote_url: The url of the remote webdriver, defaults to http://54.36.177.119:4450 (optional)
    :param credentials: a dictionary with the keys "email" and "password"
    :return: A dictionary with the keys being the profile number and the values being the dictionary of
    the user, description, image and url.
    """
    
    # Checking if the credentials are None, if they are, it is assigning the default credentials to the
    # variable credentials.
    if credentials is None:
        credentials = {"email": "interndata@mailfence.com", "password": "AbdoAbdo123@"}

    try:
        # Creating empty lists to store the results of the search.
        results_users = []
        results_descriptions = []
        results_images = []
        users = []
        descriptions = []
        images = []

        # Creating a remote webdriver instance.
        chrome_options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor=remote_url, options=chrome_options)

      # Opening the login page of tumblr and waiting for 5 seconds.
        driver.get("https://www.tumblr.com/login")
        time.sleep(5)

      # Finding the element with the name "email" and then it is sending the email to the element.
        username = driver.find_element_by_name("email")
        username.send_keys(credentials["email"])


      # Finding the element with the name "password" and then it is sending the password to the
      # element.
        password = driver.find_element_by_name("password")
        password.send_keys(credentials["password"])

        # Clicking on the "Connexion" button.
        driver.find_element_by_class_name("EvhBA").click()
        time.sleep(3)

       # Creating a url with the name of the person that we want to search for and then it is opening
       # the url.
        url = f"https://www.tumblr.com/search/{name}?v=blog"
        driver.get(url)
        time.sleep(3)

        for _ in range(4):
            with contextlib.suppress(Exception):
                # Appending the results of the search to the list `results_users` and then it is extending the list `users` with the text of the results.
                results_users.append(driver.find_elements_by_class_name("UulOO"))
                users.extend(user.text for user in results_users[-1])

                # Appending the results of the search to the list `results_descriptions` and then it is extending the list `descriptions` with the text of the results.
                results_descriptions.append(driver.find_elements_by_class_name("fTJAC"))
                descriptions.extend(
                    description.text for description in results_descriptions[-1]
                )
                
                # Appending the results of the search to the list `results_images` and then it is extending the list `images` with the text of the results.
                results_images.append(driver.find_elements_by_class_name("RoN4R.tPU70"))
                images.extend(image.get_attribute("srcset").split()[-2] for image in results_images[-1])

                # Clicking on the "Afficher plus de blogs" button.
                driver.find_element_by_xpath(
                    "//span[normalize-space()='Afficher plus de blogs']"
                ).click()
                time.sleep(1)

            # Creating a dictionary with the keys being the profile number and the values being the
            # dictionary of the user, description, image and url.
            urls = add_extension(users)
            keys = [f"profile {str(index+1)}" for index, _ in enumerate(urls)]
            values = [
                build_dict([user, description, image, url])
                for user, description, image, url in zip(users, descriptions, images, urls)
            ]
            
        # Closing the driver.
        driver.quit()

        # build a dictionary from the list of keys and values
        return users, urls, images, descriptions, dict(zip(keys, values))

    # Catching any exception that might occur and then it is printing the error and then it is closing
    # the driver.
    except Exception as e:
        print(f"An error has occurred {e}")
        if driver:
            driver.quit()

#print(profile_search("Emmanuel macron"))