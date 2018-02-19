##################################### Method 1
import mechanize
import cookielib
import argparse
from bs4 import BeautifulSoup, SoupStrainer

parser = argparse.ArgumentParser(description='Scrape thesis website')
parser.add_argument('--user', required=True, dest='username')
parser.add_argument('--pass', required=True, dest='password')
args = parser.parse_args()


# Browser
br = mechanize.Browser()

# Cookie Jar
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

# The site we will navigate into, handling it's session
br.open('https://itp.nyu.edu/thesis/journal2018/wp-login.php')

# View available forms
for f in br.forms():
    print f

# Select the second (index one) form (the first form is a search query box)
br.select_form(nr=0)

# User credentials
br.form['log'] = args.username
br.form['pwd'] = args.password

# Login
response = br.submit()

data = br.open('https://itp.nyu.edu/thesis/journal2018/').read()

page = BeautifulSoup(data,'html.parser')

urls = []
text_file = open('results.txt', 'w')
for link in page.findAll('a'):
    l = link.get('href')
    if 'thesis-statement' in l:
        urls.append(l)

for url in urls:
  html = br.open(url).read()
  soup = BeautifulSoup(html, 'html.parser')
  result = soup.find("div", {"class": "itpThesisSummaryMain"})
  text_file.write(result.text.encode('utf-8'))

text_file.close()