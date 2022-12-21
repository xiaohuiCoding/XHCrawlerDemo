import re  # 正则表达式，提取html网页信息
import requests  # 网页请求
import os  # 保存文件
from bs4 import BeautifulSoup  # 解析html网页


def getHtml(url):  # 固定格式，获取html内容
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    }  # 模拟用户操作
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        print('网络状态错误')


def getUrlList(url):  # 获取图片链接
    url_list = []  # 存储每张图片的url，用于后续内容爬取
    demo = getHtml(url)
    soup = BeautifulSoup(demo, 'html.parser')
    # class='list'在全文唯一，因此作为锚，获取唯一的div标签；注意，这里的网页源代码是class，但是python为了和class（类）做区分，在最后面添加了_
    sp = soup.find_all('div', class_="list")
    nls = re.findall(r'a href="(.*?)"', str(sp))  # 用正则表达式提取链接
    for i in nls:
        if 'https' in i:  # 因所有无效链接中均含有'https'字符串，因此直接剔除无效链接（对应第3条的分析）
            continue
        if 'pic' in i:
            continue
        url_list.append('http://www.netbian.com' + i)  # 在获取的链接中添加前缀，形成完整的有效链接
    return url_list
    print(url_list)


def fillPic(url, page):
    pic_url = getUrlList(url)  # 调用函数，获取当前页的所有图片详情页链接

    path = './resource_images'  # 保存路径
    for p in range(len(pic_url)):
        pic = getHtml(pic_url[p])
        soup = BeautifulSoup(pic, 'html.parser')
        psoup = soup.find('div', class_="pic")
        picUrl = re.findall(r'src="(.*?)"', str(psoup))[0]
        pic = requests.get(picUrl).content
        image_name = '第{}页'.format(page) + '第' + str(p+1) + '张' + '.jpg'
        image_path = path + '/' + image_name
        with open(image_path, 'wb') as f:
            f.write(pic)
            print(image_name, '下载完毕！！！')


def main():
    n = input('请输入要爬取的页数：')
    url = 'http://www.netbian.com/meinv/'
    if not os.path.exists('./resource_images'):
        os.mkdir('./resource_images/')
    page = 1
    fillPic(url, page)
    if int(n) >= 2:
        ls = list(range(2, 1 + int(n)))
        url = 'http://www.netbian.com/meinv/'
        for i in ls:
            page = str(i)
            url_page = 'http://www.netbian.com/meinv/'
            url_page += 'index_' + page + '.htm'
            fillPic(url_page, page)


main()
