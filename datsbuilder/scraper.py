import requests
from bs4 import BeautifulSoup
import re
# Use requests to get access to the page
result = requests.get('https://www.frdr.ca/repo/handle/doi:10.20383/101.0170')
# check if the content is present
# extract content of the page
src = result.content

# turn to bs4 to use content
soup = BeautifulSoup(src, 'lxml')
# find all links on the page
for headlines in soup.find_all(re.compile('^h[1-6]$')):
    print(headlines.text.strip())

# print(soup.prettify())
for tag in soup.find_all("meta"):
    print(tag.get("content", None))
