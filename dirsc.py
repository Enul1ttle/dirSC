#coding=utf-8
# python3.6
import sys
import imp
imp.reload(sys)

import os
import os.path
import requests
from urllib.parse import unquote

x= '/'
#排除不要的uri
ignore =['png','jpg','gif','css']

suffixList = ['.rar','.zip','.sql','.gz','.tar','.ba2','.tar.bz2','.bak','.dat','.txt','.mdb','.doc','.lst','.tmp','.temp','.xml']

keyList = ['web','webroot','WebRoot','website','www','wwww','www1','www2','www3','www4','www5','default','log','elk','weblog',
'mysql','ftp','FTP','MySQL','redis','Redis','sa','cig','access','error','logs','data','database','sql','vpn','proxy','temp',]


def run(url):
	# 根据URL，推测一些针对性的文件名
	num1 = url.find('.')
	num2 = url.find('.', num1 + 1)
	keyList.append(url[num1 + 1:num2])
	keyList.append(url[num1 + 1:num2].upper())
	keyList.append(url)  # 如www.t00ls.com
	keyList.append(url.upper())
	keyList.append(url.replace('.', '_'))  # www_t00ls_com
	keyList.append(url.replace('.', '_').upper())
	keyList.append(url.replace('.', ''))  # wwwt00lscom
	keyList.append(url.replace('.', '').upper())
	keyList.append(url[num1 + 1:])  # t00ls.com
	keyList.append(url[num1 + 1:].upper())
	keyList.append(url[num1 + 1:].replace('.', '_'))  # t00ls_com
	keyList.append(url[num1 + 1:].replace('.', '_').upper())
	
#返回/在URL中第3次出现的位置
def findSubStr(substr,str,i):
	count = 0
	while i>0:
		index =str.find(substr)
		if index == -1:
			return -1
		else:
			str = str[index+1:]
			i-=1
			count = count+index+1
	return count -1
		

print ("Please input (e.g:www.t00ls.com):")
url = input()
script = int(input("输入数字选择脚本 1 asp、2 aspx、3 php、4、jsp: "))
run(url)

tempList = []

for key in keyList:
	for suff in suffixList:
		tempList.append(key + suff)
#添加高效目录字典
fobj = open(url+".txt" , 'w')
for each in tempList:
    fobj.write('%s%s' % (each,'\n'))
    fobj.flush()
if script == 1:
	f= open('./dic/asp.txt','r',encoding='gbk')
	for s in f.readlines():
		fobj.write(s)
if script == 2:
	f= open('./dic/aspx.txt','r',encoding='gbk')
	for s in f.readlines():
		fobj.write(s)
if script == 3:
	f= open('./dic/php.txt','r',encoding='gbk')
	for s in f.readlines():
		fobj.write(s)
if script == 4:
	f= open('./dic/jsp.txt','r',encoding='gbk')
	for s in f.readlines():
		fobj.write(s)

f= open('./dic/dir.txt','r',encoding='gbk')
for s in f.readlines():
	fobj.write(s)

#获取web.archive.com 结果
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '

           'AppleWebKit/537.36 (KHTML, like Gecko) '

           'Chrome/56.0.2924.87 Safari/537.36'}
#总所周知的原因，使用sock5代理
proxies = {'http': 'socks5://127.0.0.1:1080'}
wayurl= "http://web.archive.org/cdx/search/cdx?url={}/*&output=text&fl=original&collapse=urlkey"
res = requests.get(wayurl.format(url,proxies=proxies), stream=True)
with open('wayurl.txt', 'w', encoding='utf-8') as f1:
    f1.write(unquote(res.text))

#提取URI
f= open('wayurl.txt','r',encoding='gbk')
for s in f.readlines():
	y = findSubStr(x,s,3)
	temp = s[y+1:]
	uri = temp.strip('\n')  # 去掉每行最后的换行符'\n'
	#排除图片等URI
	if uri[-3:] not in ignore:
		fobj.write(uri+'\n')
		
	
print('OK!')