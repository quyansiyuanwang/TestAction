#!/usr/bin/env python3

import sys

from time import sleep
from requests import get, post
from bs4 import BeautifulSoup

DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0"
DEFAULT_JESSIONID = "A56B51ECBDB53E1131A731A5F627A5FE"


def login(usr, encrypted_pwd, user_agent, jessionid):
    pre_request = get("http://10.88.108.100")

    soup = BeautifulSoup(pre_request.text, 'html.parser')
    script_tag = soup.find('script', string=lambda t: t and 'top.self.location.href' in t)
    url_by_get = script_tag.string.split("'")[1]

    url = "http://10.88.108.101/eportal/InterFace.do?method=login"

    cookies = {
        "EPORTAL_COOKIE_OPERATORPWD": "",
        "EPORTAL_COOKIE_SERVER": "",
        "EPORTAL_COOKIE_DOMAIN": "",
        "EPORTAL_COOKIE_SERVER_NAME": "",
        "EPORTAL_AUTO_LAND": "",
        "EPORTAL_COOKIE_USERNAME": "",
        "EPORTAL_COOKIE_PASSWORD": "",
        "EPORTAL_COOKIE_SAVEPASSWORD": "false",
        "EPORTAL_COOKIE_NEWV": "",
        "EPORTAL_USER_GROUP": "%E5%AD%A6%E7%94%9F",
        "JSESSIONID": "078B0B6382D897D813D7B90AAD8558EF"
    }

    form_datas = {
        'userId': usr,
        'password': encrypted_pwd,
        'service': "",
        'queryString': url_by_get.replace("=", "%3D").replace("&", "%26"),
        'operatorPwd': "",
        'operatorUserId': "",
        'validcode': "",
        'passwordEncrypt': "true"
    }

    headers = {
        'User-Agent': user_agent,
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN",
        'Referer': url_by_get,
        'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
        'Origin': "http://10.88.108.101",
        'Cookie': f"EPORTAL_COOKIE_PASSWORD=; EPORTAL_COOKIE_USERNAME=; EPORTAL_COOKIE_SERVER=; EPORTAL_COOKIE_NEWV=; EPORTAL_AUTO_LAND=false; EPORTAL_COOKIE_SAVELANINFO=false; EPORTAL_COOKIE_SERVER_NAME=; EPORTAL_COOKIE_OPERATORPWD=; EPORTAL_COOKIE_SAVEPASSWORD=false; EPORTAL_COOKIE_DOMAIN=; JSESSIONID={jessionid}"
    }

    response = post(
        url=url,
        headers=headers,
        data=form_datas,
        cookies=cookies,
        allow_redirects=False
    )

    response.encoding = 'GBK'

    htmls = response.content.decode('utf-8')
    eval_responseText = {}
    if htmls.startswith('{"userIndex":'):
        eval_responseText = eval(htmls.replace("null", "None"))

    if eval_responseText:
        print("visit success: ")
        print(f"login usr_idx: {eval_responseText.get('userIndex')}")
        print(f"login result: {eval_responseText.get('result')}")
        print(f"login message: {eval_responseText.get('message')}")


def is_campus_jumper(content):
    if content.startswith("Connect Test"):
        return False
    return True


def loop_login(usr, encrypted_pwd, user_agent=DEFAULT_UA, jessionid=DEFAULT_JESSIONID):
    while True:
        try:
            resp = get("http://www.qysyw.cn/ConnectTest")
            if is_campus_jumper(resp.text):
                login(usr, encrypted_pwd, user_agent, jessionid)
            else:
                print("Connect to the Internet success!")
        except Exception as e:
            print(e)
            login(usr, encrypted_pwd, user_agent, jessionid)

        sleep(300)


if __name__ == '__main__':
    loop_login(*(sys.argv[1:]))
