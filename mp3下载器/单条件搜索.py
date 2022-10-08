from tkinter import *
import requests
import jsonpath


# 二 、 功能实现
# 获取VIP音乐资源的方法：
# 1 、通过试听音乐逆向，难度较高，且违法
# 2 、通过第三方的VIP会员的资源分发网站 例如 https://music.liuzhijin.cn/ 音乐直链搜索 ，解析这种网站来获取资源
# 这里我们采用第2种方法


def song_load(url, title):
    path = "{}.mp3".format(title)
    text.insert(END, '歌曲：{}，正在下载...'.format(title))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()
    # 下载
    # urlretrieve(url, path)
    mp3 = requests.get(url).content
    with open("{}.mp3".format(title), "wb") as f:
        f.write(mp3)
    text.insert(END, '下载完毕：{},请试听'.format(title))
    # 文本框滚动
    text.see(END)
    # 更新
    text.update()


def get_music_name():
    name = entry.get()
    platform = var.get()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        # 该网站特性!!!!!，带着这个去请求，判断请求是异步ajax还是同步。只有是异步ajax请求，才能返回我们需要的json数据,否则会报错或者仅返回静态源代码
        # 如果为了保险起见，可以把抓包得到的headers全部复制，然后通过网站的转换工具转为headers，全部放入代码中
    }
    data = {
        "input": name,
        "filter": "name",
        "type": platform,
        "page": "1"
    }
    url = 'https://music.liuzhijin.cn/'
    # 这里的请求并不是对首页的请求，而是在搜索框中输入歌曲名称后，点击搜索按钮之后的请求，类型为post请求
    json_text = requests.post(url, data=data, headers=headers).json()
    title = jsonpath.jsonpath(json_text, '$..title')[0]  # 这里我们为了简单取的是第一个,所以是[0]。如果想挑选指定歌手的歌曲，可以把json转为字典，遍历字典选取指定歌手的歌曲
    url = jsonpath.jsonpath(json_text, '$..url')[0]
    author = jsonpath.jsonpath(json_text, '$..author')[0]
    # print(title, url, author)
    song_load(url=url, title=title)


# get_music_name()   #  这里仅供编写过程中测试，最终需要把这个函数绑定到下载按钮上


# 一、界面 GUI
# 1 、创建一个画布
root = Tk()  # 此时运行窗口会一闪而逝
# 2 、设置窗口标题
root.title("音乐下载器")
# 3 、设置窗口的大小固定以及出现的位置居中
root.geometry("560x450+500+200")

# 4 、添加标签组件
label = Label(root, text="请输入下载歌曲：", font=('华文行楷', 20))
# 5 、给标签组件 定位 布局
label.grid()
# 6 、 添加输入框组件
entry = Entry(root, font=("华文行楷", 20))
entry.grid(row=0, column=1)  # 第一行，第一列，也就是 在上面创建的的标签组件的右边

# 7 、单选按钮组件
var = StringVar()
r1 = Radiobutton(root, text='网易云', variable=var, value='netease')  # 这里的值需要和网站的请求头form date中type的值一致
r1.grid(row=1, column=0)
r1.select()     # 让这个单选按钮默认被选中
r2 = Radiobutton(root, text='QQ', variable=var, value='qq')
r2.grid(row=1, column=1)

# 8 、列表框组件
text = Listbox(root, font=("华文行楷", 16), width=50, height=15)
text.grid(row=2, columnspan=2)  # columnspan=2 代表占两列的位置

# 9 、 下载按钮
button1 = Button(root, text='开始下载', command=get_music_name)
button1.grid(row=3, column=0)
# 10 、 退出程序按钮
button2 = Button(root, text='退出程序', command=root.quit)  # 这里如果写成 command=root.quit() 是错误的
button2.grid(row=3, column=1)

# 让界面一直显示
root.mainloop()
