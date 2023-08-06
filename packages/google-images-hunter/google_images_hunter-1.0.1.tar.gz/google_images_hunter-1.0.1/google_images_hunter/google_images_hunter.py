from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pandas as pd
from time import sleep


''' Generates a Searcher class to perform web scraping.It is highly recommended to use a profile 
    so you go easily through Google cookies advertisement or other login-based problems. Although,
    it is not required.
'''

class Searcher:

    def __init__(self, navigator = 'firefox', profile: str = None, driver_path='.'):
        global browser, profile_flag
        profile_flag = False

        if navigator == 'firefox':
            if profile is not None:
                profile_up = webdriver.FirefoxProfile(profile)
                profile_flag = True
                browser = webdriver.Firefox(executable_path=driver_path, firefox_profile=profile_up)
            else:
                browser = webdriver.Firefox(executable_path=driver_path)

        elif navigator == 'chrome':
            if profile is not None:
                options = webdriver.ChromeOptions()
                options.add_argument(profile)
                profile_flag = True
                browser = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
            else:
                browser = webdriver.Chrome(executable_path=driver_path)

        elif navigator == 'edge':
            if profile is not None:
                options = webdriver.EdgeOptions()
                options.add_argument(profile)
                profile_flag = True
                browser = webdriver.Edge(executable_path=driver_path, options=options)
            else:
                browser = webdriver.Edge(executable_path=driver_path)
        else:
            raise AttributeError('Navigator argument should be one of this list: firefox, chrome, edge',
                                'Also, check the driver path if needed.
                                )


    def scroll_to_end(self):
        '''Scroll down the browser looking for the "Load more results" button'''
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)

    def load_more(self, loadmore):
        '''This function will look for more results using "loadmore" as iterator'''
        for i in range(loadmore):
            self.scroll_to_end()
            # If it finds the button, it clicks.
            load_more_button = browser.find_element(By.CSS_SELECTOR, ".mye4qd")

            if load_more_button:
                browser.execute_script("document.querySelector('.mye4qd').click();")
                sleep(1)
                load_more_button = False

    def scrap(self, max_images : int = 100, download_url_lists : bool = False, concept : str = None, loadmore : int = 10):
        '''Scrapes for images with a given concept. It will scroll down the "Load more results button" as many times
         as loadmore argument says. If there's no more, it will still try to scroll down those times, and then
          start to parse the image URLs.'''

        research = f'https://www.google.com/search?q={concept}&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
        browser.get(research)
        if not profile_flag: # Skip cookies
            try:
                sleep(1)
                refuse_cookies = browser.find_element(By.XPATH, '/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[1]/div/div/button/span')
                refuse_cookies.click()
            except:
                pass
        print('Scrolling down the page...')
        self.load_more(loadmore)

        if concept: # Checks if there's some topic to search images.

            self.image_urls = set()
            self.image_count = 0
            self.results_start = 0
            self.scrapflag = True

            while self.scrapflag:
                thumbnail_results = browser.find_elements(By.CSS_SELECTOR, "img.Q4LuWd")
                self.number_results = len(thumbnail_results)
                sleep(0.5)
                print(
                    f"Found: {self.number_results} search results. Extracting links from {self.results_start}:{self.number_results}"
                )

                for img in thumbnail_results[self.results_start:self.number_results]:
                    # Try to click every thumbnail such that we can get the real image behind it.
                    try:
                        img.click()
                        sleep(1)
                    except Exception:
                        continue

                    # Extract image urls
                    actual_images = browser.find_elements(By.CSS_SELECTOR, "img.n3VNCb")
                    for actual_image in actual_images:
                        if actual_image.get_attribute("src") and "http" in actual_image.get_attribute("src"):
                            self.image_urls.add(actual_image.get_attribute("src"))
                            self.image_count += 1
                            print(f'{self.image_count} url parsed. Only non-repeated will remain.')

                        if self.image_count >= max_images:
                            self.scrapflag = False
                            break

                    # If the number images found exceeds our `num_of_images`, end the search.
                    if self.image_count >= max_images:
                        print(f"Found: {len(self.image_urls)} image links, done!")
                        scrapflag = False
                        break
                # Flag for a possible download of the URLs list.
                if download_url_lists:
                    url_to_excel = pd.DataFrame(self.image_urls, columns=['Image Url'])
                    url_to_excel.to_csv('urllist.csv')
                print('Image URL list ready to use as downloader input.')
                return self.image_urls
        else:
            raise AttributeError('You should fill "concept" attribute with something to find images of!')

'''This class generates a downloader object that takes a URl list of images previously scraped
        and a path (would be better if the path ends with "/" if you don't want to download it on
        our python script folder.'''

