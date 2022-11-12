import re
import requests
from tqdm import tqdm


# 先F12， 再点击某一个标签，选择“XHR”，再“预览”标签下寻找id


tag_url = "https://api.ys297.com/api/getrandomvideobytagid?page=1&id=113"
json_data = requests.get(url=tag_url).json()
json_data = json_data['data']
# print(len(json_data))
# 得到tag_url中的关键数字例如上面的283
for i in range(0, len(json_data)):  # 包头不包尾
    num_str = json_data[i].get('video_img').split('/')[-3]
    url_m3u8 = "https://video.ys297.com/" + num_str + ".m3u8"
    resp = requests.get(url=url_m3u8)
    # print(resp)
    ts_list = re.sub('#E.*', '', resp.text).split()
    # print(ts_list)
    # print(len(ts_list))
    for ts in tqdm(ts_list):  # tqdm 进度条
        ts_data = requests.get(ts).content
        # 这里模式选择'ab'，是因为ts_list中的地址下载到的全部是.ts文件，需要把它们拼接起来，所以用a，append，b这里值二进制
        with open('E:\\Videos\\ys297\\' + num_str + '.mp4', mode='ab') as f:
            f.write(ts_data)
