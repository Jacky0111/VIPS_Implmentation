import urllib.request as ur
from bs4 import BeautifulSoup

page = ur.urlopen('https://www.thestar.com.my/news/nation/2021/06/18/high-spikes-in-registration-as-vaccinations-revved-up')
soup = BeautifulSoup(page, 'html.parser')

f = open("sample.html", "w")
f.write(str(soup))
f.close()

