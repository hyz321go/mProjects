import re
import requests
from tqdm import tqdm


# 爱奇艺，赘婿第7集
# 在抓包工具中搜索m3u8或者#EXTM3U（主要是要有#EXTM3U）: 左上角点放大镜，刷新网页，左边找到dash，查看预览，再复制请求头的网址
# ['data']['program']['video']下面找到第几项有['m3u8']，例如如果是第0项，就  m3u8_text = json_data['data']['program']['video'][0]['m3u8']

# 这url会变化
url = "https://cache.video.iqiyi.com/dash?tvid=5095858818866900&bid=600&vid=e3b7ffaaba1f6420a8a56e41e13640db&src=01010031010000000000&vt=0&rs=1&uid=1689959768&ori=pcw&ps=1&k_uid=4f26285a077b6a0f626969debe979057&pt=0&d=0&s=&lid=&cf=&ct=&authKey=664f77858515cd1093362dce58bcb1dd&k_tag=1&dfp=a0d6a3c16a77b6413092864b1230fdda001a9d88cdc3c6bc42716cd09488d9ca58&locale=zh_cn&prio=%7B%22ff%22%3A%22f4v%22%2C%22code%22%3A2%7D&pck=d6iqtgluUvQhqxQlRBm2b8JlCXWfnm1A14he9ym2lopGn5woSZI1QjsR1Fe2U9pforuksa7&k_err_retries=0&up=&sr=1&qd_v=5&tm=1668171667694&qdy=u&qds=0&k_ft1=706436220846084&k_ft4=1161084347621380&k_ft5=262145&k_ft7=4&bop=%7B%22version%22%3A%2210.0%22%2C%22dfp%22%3A%22a0d6a3c16a77b6413092864b1230fdda001a9d88cdc3c6bc42716cd09488d9ca58%22%7D&ut=1&vf=3f666e5af4202b4ac87ec1162fd2ea7a"
json_data = requests.get(url=url).json()
# 这里[0]会变化
m3u8_text = json_data['data']['program']['video'][0]['m3u8']
# print(m3u8_text)
ts_list = re.sub('#E.*', '', m3u8_text).split()
# print(ts_list)
# print(len(ts_list))
for ts in tqdm(ts_list):
    ts_data = requests.get(ts).content
    with open('E:\\Videos\\赘婿第7集.mp4', mode='ab') as f:
        f.write(ts_data)
