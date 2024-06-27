from selenium import webdriver

class Webdriver:
    def __init__(self, download_directory, width = 1220, height = 2600, view_browser = True) -> None:
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless=new')

        chrome_options.add_argument('window-size=1200x1000')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-notifications')
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.set_window_size(width, height)
    def getDriver(self):
        return self.driver