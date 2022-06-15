import os

print(os.listdir())
file = open("init_page.html", "r")
html_code=file.read()
print(html_code.replace("\n",""))
file.close()
print()
print(html_code.partition(':')[0])