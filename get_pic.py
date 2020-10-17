# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 01:13:25 2020

@author: Admin
"""


import re
import urllib
import requests
import os
import time

search_tag = '尤妮丝'
url = r'https://www.mzitu.com/search/' + search_tag + '/'
root_path =  r'C:\Users\Admin\Pictures\mzitu' #save_path

def get_img(url,path,headers):
    img_src = url
  # print(img_src)
    req = urllib.request.Request(url=img_src, headers=headers)
    response = urllib.request.urlopen(req)
    filename = path
    with open(filename, "wb") as f:
      content = response.read()
      f.write(content)
      response.close()

name_list = []
url_list = []
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Referer':url
    }
req = requests.get(url,headers=headers)
req.encoding = 'utf-8'
content = req.text
pattern = re.compile(r'<ul id="pins">.*</ul>',re.S)
content = re.findall(pattern,content)
pattern1 = re.compile(r'<li><a href=".*" target="_blank">')
pattern2 = re.compile(r'alt=.* width')
result1 = re.findall(pattern1,content[0])
result2 = re.findall(pattern2,content[0])
for result in result2:
    name_list.append(result.split('\'')[1])
for result in result1:
    url_list.append(result.split('\"')[1])
    
for i in range(len(url_list)):
    url = url_list[i]
    name = name_list[i]
    os.makedirs(root_path + '\\' + name.split(': ')[-1])
    x = 1
    while True:
        headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
    'Accept-Language':'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'Referer':url
    }
        req = requests.get(url,headers=headers)
        req.encoding = 'utf-8'
        content = req.text
        page_pattern = re.compile(r'<div class="pagenavi">.*</span></a>      </div>',re.S)
        page_result = re.findall(page_pattern,content)
        pattern = re.compile(r'<div class="main-image">.*</a></p>')
        result = re.findall(pattern,content)
        img_pattern = re.compile(r'src=\"[\w\W]+\" alt')
        img_url = re.findall(img_pattern,result[0])[0].split('\"')[1]
        path = root_path + '\\' + name.split(': ')[-1] + '\\' + str(x) + '.jpg'
        get_img(img_url,path,headers)
        x += 1
        if '下一组' in page_result[0]:
            break
        else:
            pattern = re.compile(r'<a href=.*><img')
            next_page = re.findall(pattern,result[0])[0].split('\"')[1]
            url = next_page
        time.sleep(1)
    
     
     
     
   