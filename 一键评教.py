import requests
from bs4 import BeautifulSoup
import getpass
import random


postUrl = 'http://zhjw.scu.edu.cn/loginAction.do'
id = input('请输入你的学号: ')
psw = getpass.getpass('请输入你的教务系统密码（没有回显）: ')


postData = {'zjh': id ,'mm': psw}
loginResponse = requests.post(url = postUrl, data = postData)
if len(loginResponse.text) > 1000:
    print('登录失败！')
    exit(1)
cookieHeaders = {'Cookie' : loginResponse.headers['Set-Cookie'], 'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'}
searchUrl = 'http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=listWj'
queryResponse = requests.get(url = searchUrl, headers = cookieHeaders)

listSoup = BeautifulSoup(queryResponse.text, 'html.parser')

judgeCount = 0

for tr in listSoup.find_all('tr', attrs = {'class' : 'odd'}):
    curImg = tr.img
    attrsDict = curImg.attrs
    if attrsDict['title'] == '查看':
        continue
    name = attrsDict['name']
    paramList = name.split('#@')
    #print(paramList)
    wjbm = paramList[0]
    bpr = paramList[1]
    teacher = paramList[2]
    courseName = paramList[4]
    pgnr = paramList[5]
    choice = random.randint(1,3)
    if choice == 1:
        zgpj = 'Very Good!'
    elif choice == 2:
        zgpj = 'Excellent!'
    elif choice == 3:
        zgpj = '666666666'
    judgePageUrl = 'http://zhjw.scu.edu.cn/jxpgXsAction.do'
    judgePageParams = {
        'wjbm' : wjbm,
        'bpr' : bpr,
        'pgnr' : pgnr,
        'oper' : 'wjShow'
    }
    judgePage = requests.post(url = judgePageUrl, headers = cookieHeaders, data = judgePageParams)
    judgePageSoup = BeautifulSoup(judgePage.text, 'html.parser')

    judgeParams = {
        'wjbm' : wjbm,
        'bpr' : bpr,
        'pgnr' : pgnr,
        'zgpj' : zgpj
    }
    radios = judgePageSoup.find_all('input', attrs = {'type' : 'radio', 'value' : '10_1'})
    for radio in radios:
        judgeParams[radio.attrs['name']] = '10_1'
    
    judgeUrl = 'http://zhjw.scu.edu.cn/jxpgXsAction.do?oper=wjpg'
    judgeResult = requests.post(url = judgeUrl, headers = cookieHeaders, data = judgeParams)
    
    if '成功' in judgeResult.text:
        message = techer + '的' + courseName + '评教成功！'
        judgeCount += 1
    elif '失败' in judgeResult.text:
        message = techer + '的' + courseName + '评教失败！'
    print(message)

print('评教完成，共成功完成了' + str(judgeCount) + '次评教！')
input()
