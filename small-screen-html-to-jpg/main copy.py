import time
from PIL import Image
import os
from html2image import Html2Image
from bs4 import BeautifulSoup
import requests

# blank photo
# location_htmlx = r"file:///C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/blank-image.jpg"

## book
# location_htmlx_file = r"file:///C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"
# location_htmlx_file_pure = r"C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"

# location_htmlx = r"file:///C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"
# location_htmlx_pure = r"C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"


hti = Html2Image()

hti = Html2Image(size=(500, 750))

css = "body {background: white; font-size: 40px; margin-top: 35px;}"
# Dark Mode CSS
# css = "body {background: black; color: white; font-size: 40px;}"




xhtml_path_list = os.listdir(os.path.join(os.getcwd(), r"atomic-habits/OEBPS/xhtml/"))

for individual_chapter in xhtml_path_list:
    os.makedirs(os.path.join(os.getcwd(), 'atomic_habits_book', individual_chapter))

    current_htmx_file = os.path.join(os.getcwd(), "atomic-habits/OEBPS/xhtml/", individual_chapter)
 
    f=open(current_htmx_file ,'r', encoding="utf8")
    # f.read()



    # html_content = requests.get(url).text
    html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    text = soup.get_text()
    text_array = text.split(' ')

    # print(text_array)


    # for i in range(70):
        # chunk = text_array[0:70]
    # chunk = text_array[0:70]
    # print(chunk)


    num = 50
    counter = 0
    chunk = ""
    for i in range(int(len(text_array)/num)+1):
        for j in range(num):
            if j+counter >= len(text_array):
                break
            chunk+= text_array[j+counter] + " "
        hti.screenshot(html_str=chunk, css_str=css, save_as=f'sample_page_light.png')
        chunk = ""
        counter += num
        Image.open('sample_page_light.png').convert('RGB').save(f'sample_page_light.jpg')
        # time.sleep(3)
        # os.rename("sample_page.jpg", f"atomic/sample_page_{int(counter/num)}.jpg")


        # try:
            # os.replace("sample_page.jpg", f"atomic/06/subpage{1000+int(counter/num)}.jpg")
        # except FileNotFoundError as e:
        #     directory = 'atomic\\06'
        #     # os.mkdir('atomic/06')
        #     path_dir = os.path.abspath('')
        #     os.mkdir(os.path.join(path_dir, directory))
        #     print("atomic\\06 directory created")

        os.replace("sample_page_light.jpg", os.path.join(os.getcwd(), 'atomic_habits_book', individual_chapter, f"subpage{1000+int(counter/num)}.jpg"))

        print(f"created subpage{int(1000+counter/num)}.jpg")


    print(f"\n{individual_chapter} complete")
    f.close()

