from tkinter import *
import requests
import jsonpath


# 1 、在上一个版本的基础上，增加输入歌手的列表框，来精确定位具体哪位歌手的歌曲，如果不指定歌手，则提示“请输入歌手:”
# 2 、 修正单选按钮默认都被选中的BUG 解决方法：  r1.select()     # 让这个单选按钮默认被选中


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
    author_name = entry_1.get()
    # print(author_name)
    if not name:
        text.insert(END, '请输入歌曲名！！！')
        # 文本框滚动
        text.see(END)
        # 更新
        text.update()
        return
    if not author_name:
        text.insert(END, '请输入歌手名！！！')
        # 文本框滚动
        text.see(END)
        # 更新
        text.update()
        return
    platform = var.get()
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
        # 该网站特性!!!!!，带着这个去请求，判断请求是异步ajax还是同步。只有是异步ajax请求，才能返回我们需要的json数据,否则会报错或者仅返回静态源代码
    }
    data = {
        "input": name,
        "filter": "name",
        "type": platform,
        "page": "1"
    }
    url = 'https://music.liuzhijin.cn/'
    json_text = requests.post(url, data=data, headers=headers).json()
    # print(json_text)
    authors = jsonpath.jsonpath(json_text, '$..author')  # 这里返回的是一个列表，包含所有的author
    titles = jsonpath.jsonpath(json_text, '$..title')    # 这里返回的是一个列表，包含所有的title
    # print(authors)
    # 判断是否有这首歌曲或者这个歌手
    if name not in titles:
        text.insert(END, '没有找到歌曲！！！')
        # 文本框滚动
        text.see(END)
        # 更新
        text.update()
        return
    if author_name not in authors:
        text.insert(END, '没有找到歌手！！！')
        # 文本框滚动
        text.see(END)
        # 更新
        text.update()
        return
    for i, author in enumerate(authors):
        # 找到匹配的歌手，开始下载
        if author == author_name:
            title = jsonpath.jsonpath(json_text, '$..title')[i]
            url = jsonpath.jsonpath(json_text, '$..url')[i]
            song_load(url=url, title=title)
            break  # 如果有多个同名歌手，只下载第一个即可

# get_music_name()   #  这个程序仅供编写过程中测试，最终需要把这个函数绑定到下载按钮上


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

# 此处增加一个输入歌手名字的标签组件和输入框组件，类似于上面的输入歌曲名称组件
# 4_1 、添加标签组件
label_1 = Label(root, text="请输入演唱歌手：", font=('华文行楷', 20))
# 5_1 、给标签组件 定位 布局
label_1.grid(row=1, column=0)
# 6_1 、 添加输入框组件
entry_1 = Entry(root, font=("华文行楷", 20))
entry_1.grid(row=1, column=1)  # 第一行，第一列，也就是 在上面创建的的标签组件的右边

# 7 、单选按钮组件
var = StringVar()
r1 = Radiobutton(root, text='网易云', variable=var, value='netease')  # 这里的值需要和网站的请求头form date中type的值一致
r1.grid(row=2, column=0)
r1.select()  # 让这个单选按钮默认被选中
r2 = Radiobutton(root, text='QQ', variable=var, value='qq')
r2.grid(row=2, column=1)

# 8 、列表框组件
text = Listbox(root, font=("华文行楷", 16), width=50, height=14)
text.grid(row=3, columnspan=2)  # columnspan=2 代表占两列的位置

# 9 、 下载按钮
button1 = Button(root, text='开始下载', command=get_music_name)
button1.grid(row=4, column=0)
# 10 、 退出程序按钮
button2 = Button(root, text='退出程序', command=root.quit)  # 这里如果写成 command=root.quit() 是错误的
button2.grid(row=4, column=1)

# 让界面一直显示
root.mainloop()
