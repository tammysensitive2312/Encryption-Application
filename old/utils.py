import os

file_path = "data.data"
dt = ''
if not os.path.exists(file_path):
    with open('data.data', 'w', encoding='utf-32') as file:
        file.write('')
else:
    with open('data.data', 'r', encoding='utf-32') as file:
        dt = file.read()
data = []

public = []
private = []
dts = dt.split('\n')
for item in dts:
    if item != "":
        items = item.split('~')
        if items[0] == 'Public':
            public.append(items)
        else:
            private.append(items)


def add_data(type_, name, key):
    global data
    data.append({'Loại': type_, "Tên": name, "Khóa": key})


def insert_data(data_):
    with open('data.data', 'a', encoding='utf-32') as file_:
        file_.write(data_)


def set_link(link):
    res = ""
    for i in link:
        if i == "\\":
            res += "/"
        else:
            res += i
    return res


def get_keyname(link, bit):
    res = " ( " + bit + " )"
    for i in range(len(link) - 1, -1, -1):
        if link[i] == "/":
            break
        res = link[i] + res
    return res
