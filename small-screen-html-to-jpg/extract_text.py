from bs4 import BeautifulSoup
import requests
url = "https://www.geeksforgeeks.org/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "html.parser")
print(soup.get_text())









# Assign URL
url = "https://www.geeksforgeeks.org/"

# Fetch raw HTML content
html_content = requests.get(url).text

# Now that the content is ready, iterate
# through the content using BeautifulSoup:
soup = BeautifulSoup(html_content, "html.parser")

# similarly to get all the occurrences of a given tag
# print(soup.find('div').text)
print(soup.get_text())
