import requests  # 倒入请求模块
import re       # 倒入解析模块

# 确定网址，这里是百度图片搜索
url = 'https://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&ie=utf-8&rn=10&word=风景'

form_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36",
               "Host": "image.baidu.com",
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}

res = requests.get(url, headers=form_header).text
print(res)

# 正则表达式筛选数据
image_urls = re.findall('"objURL":"(.*?)",', res)

for image_url in image_urls:
    print(image_url)

    # 定义图片名称
    image_name = image_url.split('/')[-1]
    print(image_name)
    image_end = re.search('(.jpg/.png/.jpeg/.gif/.webp)＄', image_name)
    if image_end == None:
        image_name = image_name + '.jpg'

    # 保存图片到本地文件夹
    image = requests.get(image_url).content
    with open('./resource_images/%s' % image_name.split("&")[0], 'wb')as file:
        file.write(image)
