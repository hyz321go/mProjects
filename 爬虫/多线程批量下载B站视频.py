import os
import queue
import threading
import time

# 多线程批量下载B站视频!!
# 这里用了一个线程优先级队列来实现多线程下载视频，真香。我用了6个Thread，在PyCharm显示的时候，可以看到最下面的那个进度条每2秒更新一次不同视频的下载进度条，
# 不能同时更新下载进度条，这是因为直接用的you-get自带的进度条导致的。真的是多线程，用python自带的IDLE运行时可以看到会弹出6个cmd窗口同时下载

exitFlag = 0


class myThread(threading.Thread):
    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        print("开始线程：" + self.name)
        downloading_video(self.name, self.q)
        print("退出线程：" + self.name)


def downloading_video(threadName, q):
    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            videoUrl = q.get()
            queueLock.release()
            # print("%s downloading %s" % (threadName, videoUrl))
            # 第一种方法用os调用you-get
            # cmd = "you-get -o E://Videos/ " + videoUrl
            # 注意！！！这里添加的--playlist适用于B站分P视频下载，这样就可以直接打包下载了
            cmd = "you-get --playlist -o E://Videos/ " + videoUrl
            os.system(cmd)
            # 第二种方法用sys调用you-get ...我觉得没上面的方便
            # path = 'E:\\video\'   #设置下载目录
            # sys.argv = ['you-get','-o',path,videoUrl]   #sys传递参数执行下载
            # you_get.main()
        else:
            queueLock.release()
        time.sleep(2)


threadList = ["Thread-1", "Thread-2", "Thread-3", "Thread-4", "Thread-5", "Thread-6"]  # 线程个数
videoList = [
    "https://www.bilibili.com/video/BV1fe4y1n7K6",
    # "https://www.bilibili.com/video/BV1rt4y1z7fo"
]  # 待下载的视频列表

queueLock = threading.Lock()
workQueue = queue.Queue(30)
threads = []
threadID = 0

if __name__ == '__main__':
    # 创建新线程
    for tName in threadList:
        thread = myThread(threadID, tName, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1
    # 填充队列
    queueLock.acquire()
    for word in videoList:
        workQueue.put(word)
    queueLock.release()
    # 等待队列清空
    while not workQueue.empty():
        pass
    # 通知线程是时候退出
    exitFlag = 1
    # 等待所有线程完成
    for t in threads:
        t.join()
    print("退出主线程")
