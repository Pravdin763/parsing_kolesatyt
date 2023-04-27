
import requests



def downloadim(x):
    try:
        res = requests.get(x, stream=True)
    except Exception:
        del_x = '/'.join(x.split('/')[1:])
        x = 'https://tolyatti.kolesatyt.ru/' + del_x
        res = requests.get(x, stream=True)
    with open('E:\\python\\parser wheels\\data\\' + ''.join(x.split('/')[-2:]), 'wb') as file:
        for value in res.iter_content(1024*1024):
            file.write(value)



