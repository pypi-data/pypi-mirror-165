import requests


# 下载视频
def download(url):
    with requests.get(url, stream=True) as r:
        print('开始下载。。。')
        with open('v.mp4', 'wb')as f:
            for i in r.iter_content(chunk_size=1024):
                f.write(i)
    print('下载结束')


# 带下载进度下载视频
def download_level2(url):
    with requests.get(url, stream=True) as r:
        print('开始下载。。。')
        content_size = int(r.headers['content-length'])
        with open('v.mp4', 'wb')as f:
            n = 1
            for i in r.iter_content(chunk_size=1024):
                loaded = n * 1024.0 / content_size
                print(loaded)
                f.write(i)
                print('已下载{0:%}'.format(loaded))
                n += 1
    print('下载结束')


if __name__ == '__main__':
    URL = 'http://tb-video.bdstatic.com/tieba-smallvideo-transcode/3853363_adac7ec8907890797b3970e570aba43a_140b8b74a014_3.mp4'
    # 下载视频
    # download(URL)
    # 带下载进度
    download_level2(URL)