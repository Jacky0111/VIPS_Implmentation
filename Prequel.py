import re
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Prequel:
    url = None
    browser = None
    url_list = []
    filter_list = []

    def __init__(self, url):
        self.url = url
        self.setDriver()
        self.url_list = self.retrievePageUrl()
        self.url_list = self.filterUrl()
        print(f'Final Length: {len(self.url_list)}')

    '''
    Set driver
    '''
    def setDriver(self):
        option = Options()
        option.add_argument('--headless')
        option.add_argument('--disable-gpu')
        option.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
        self.browser = webdriver.Chrome(options=option)

    '''
    Get URL - Get href from <a> tag and store to list
    @return crawled
    '''
    def retrievePageUrl(self):
        self.browser.get(self.url)
        self.browser.set_window_size(1920, self.browser.execute_script('return document.body.parentNode.scrollHeight'))
        time.sleep(10)

        crawled = []
        links = self.browser.find_elements_by_tag_name('a')

        for link in links:
            crawled.append(link.get_attribute('href'))

        self.browser.close()
        self.browser.quit()

        return crawled

    '''
    Filter URL
    @return cleaned
    '''
    def filterUrl(self):
        print(f'No. of ori link: {len(self.url_list)}')
        clean1 = self.removeDuplicates()
        clean2 = self.websiteUrl(clean1)
        cleaned = self.newsContentUrl(clean2)
        return cleaned

    '''
    URLs Must be unique / Remove duplicates
    @return unique
    '''
    def removeDuplicates(self):
        unique = []
        [unique.append(x) for x in self.url_list if x not in unique]
        print(unique)
        print(f'No. of unique link: {len(unique)}')
        return unique

    '''
    The URL format must be matched with website format
    @param urls
    @return website
    '''
    def websiteUrl(self, urls):
        website = []
        for x in urls:
            try:
                if x.startswith(self.url) or (x.startswith('https://' + urlparse(self.url).netloc) and not x.endswith('home')):
                    website.append(x)
            except AttributeError:
                continue
        print(website)
        print(f'No. of website link: {len(website)}')
        return website

    '''
    The URL must be news content URL
    @param urls
    @return news_content
    '''
    def newsContentUrl(self, urls):
        path_urls = self.retrievePath(urls)
        news_content = []
        for (a, b) in zip(urls, path_urls):
            if len(re.findall('/', b)) > 3:
                news_content.append(a)
        print(news_content)
        print(f'No. of news content link: {len(news_content)}')
        return news_content

    '''
    Retrieve the path of URL
    For example: 'https://www.thestar.com.my/sport', path = '/sport'
    @param urls
    @return path
    '''
    @staticmethod
    def retrievePath(urls):
        path = []
        for x in urls:
            path.append(urlparse(x).path)
        return path


# def main():
#     # pre = Pre(unquote('https://www.thestar.com.my/sport', 'encoding="utf-8'))
#     # pre = Pre(unquote('https://www.malaymail.com/news/sports', 'encoding="utf-8'))
#     pre = Pre(unquote('https://www.nst.com.my/sports', 'encoding="utf-8'))
#     # pre = Pre(unquote('https://sea.mashable.com/science/', 'encoding="utf-8'))
#     # pre = Pre(unquote('https://www.bernama.com/bm/sukan/index.php', 'encoding="utf-8'))
#     # content = pre.url_list
#     # for i, ele in enumerate(content):
#     #     if i > 4:
#     #         break
#     #     print(ele)
#     # print(f'length: {len(content)}')
#
#
# if __name__ == '__main__':
#     main()
