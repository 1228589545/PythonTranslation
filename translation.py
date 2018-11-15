from flask import Flask, render_template
from flask import send_file
from flask import request
from  flask import json
app = Flask(__name__)
import requests
import json
import random
import time

@app.route('/')
def hello_world():
    return send_file(r"D:\PC\translation\templates\html.html")
    # return render_template(r"D:\PC\translation\templates\html.html")
def md5_my(need_str):
    import hashlib
    # 创建md5对象
    md5_o = hashlib.md5()
    # 需要有bytes, 作为参数
    # 由str, 转换成 bytes encode-------str.encode('utf-8')
    # 由bytes转换成 str, decode---------bytes.decode('utf-8')
    sign_bytes = need_str.encode('utf-8')
    # print(type(sign_bytes))#<class 'bytes'>
    # 更新md5 object的值
    md5_o.update(sign_bytes)
    sign_str = md5_o.hexdigest()
    return sign_str
@app.route('/login', methods=['POST'])
def login():
    data = json.loads(request.form.get('data'))
    contents = data["content"]
    first=data["first"]
    second=data["second"]
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
               'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
               'Connection': 'keep-alive',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Cookie': 'OUTFOX_SEARCH_USER_ID=-493176930@10.168.8.63; OUTFOX_SEARCH_USER_ID_NCOO=38624120.26076847; SESSION_FROM_COOKIE=unknown; JSESSIONID=aaabYcV4ZOU-JbQUha2uw; ___rl__test__cookies=1534210912076',
               'Host': 'fanyi.youdao.com', 'Origin': 'http://fanyi.youdao.com',
               'Referer': 'http://fanyi.youdao.com/',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
               'X-Requested-With': 'XMLHttpRequest', }

    salt = int(time.time() * 1000 + random.randint(0, 10))
    salt_str = str(salt)
    S = "fanyideskweb"
    D = "ebSeFb%=XZ%T[KZ)c(sy!"
    sign_str = S + contents + salt_str + D
    # md5 加密的方法
    sign_md5_str = md5_my(sign_str)
    form = {'i': contents,
            'from': first,
            'to': second,
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': salt_str,#加盐
            'sign': sign_md5_str,#标记,只有拥有了标记和加盐，才能让浏览器知道是那个语言之间的翻译
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_REALTIME',
            'typoResult': 'false',
            'ue': 'UTF-8'}  # 设置翻译支持中文
    res = requests.post(url, data=form, headers=headers)
    jd = json.loads(res.content.decode())

    return  jd['translateResult'][0][0]['tgt']
if __name__ == '__main__':
    app.run(host='127.0.0.1',port='5000'
    )

