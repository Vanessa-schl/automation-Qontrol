from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class YouTubeScraper:
    def _init_(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)
    
    def open_youtube(self):
        self.driver.get("https://www.youtube.com/")
    
    def search_channel(self, channel_name: str):
        search_bar = self.driver.find_element(By.NAME, "search_query")
        search_bar.send_keys(channel_name)
        search_bar.send_keys(Keys.ENTER)
    
    def open_channel(self, channel_name: str):
        channel_name_xpath = f"//yt-formatted-string[@id='text' and contains(text(), '{channel_name}')]"
        self.wait.until(EC.presence_of_element_located((By.XPATH, channel_name_xpath))).click()
    
    def open_video_tab(self):
        open_video_tab = "//yt-tab-shape[2]/div"
        self.wait.until(EC.presence_of_element_located((By.XPATH, open_video_tab))).click()
        
    def open_latest_video(self):
        latest_video_xpath = '//*[@id="video-title-link"]'
        self.wait.until(EC.presence_of_element_located((By.XPATH, latest_video_xpath))).click()
    
    
    def get_video_views(self) -> str:
        view_count_xpath = '//*[@id="info"]/span[1]'
        view_count_element = self.wait.until(EC.presence_of_element_located((By.XPATH, view_count_xpath)))
        return view_count_element.text
    
    def get_video_tags(self) -> str:
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="info"]/span[1]'))).click()
        self.driver.implicitly_wait(10)
        tag_elements = self.driver.find_elements(By.XPATH, "//a[contains(@href, '/hashtag/')]")
        tags = " ".join([tag.text for tag in tag_elements if tag.text])
        return tags
    
    def close(self):
        self.driver.quit()


def main():
    scraper = YouTubeScraper()
    channelName = "Qontrol Alt"
    try:
        scraper._init_()
        scraper.open_youtube()
        scraper.search_channel(channelName)
        scraper.open_channel(channelName)
        scraper.open_video_tab()
        scraper.open_latest_video()
        
        view_count = scraper.get_video_views()
        print("Quantidade de pessoas que assistiram o video: ", view_count)
        
        tags = scraper.get_video_tags()
        print("Tags: ", tags)
    
    finally:
        scraper.close()

if __name__ == "__main__":
    main()