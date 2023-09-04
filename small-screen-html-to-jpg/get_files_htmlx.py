import os
## book
location_htmlx = r"file:///C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"
location_htmlx_pure = r"C:/Users/kk/Documents/GitHub/python_projects/small-screen-html-to-jpg/atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml"

# atomic-habits/OEBPS/xhtml/06_Introduction_My_Story.xhtml
# print(os.listdir(os.path.join(os.getcwd(), r"atomic-habits/OEBPS/xhtml/")))
# print(os.listdir(location_htmlx_pure))


xhtml_path_list = os.listdir(os.path.join(os.getcwd(), r"atomic-habits/OEBPS/xhtml/"))

for path_loc in xhtml_path_list:
    os.makedirs(os.path.join(os.getcwd(), 'atomic_habits', path_loc))