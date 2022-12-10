#步骤2开始Star
import time, os, json
import re
import urllib.parse
import demjson
import requests



def log(content):
    this_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print("[" + str(this_time) + "]" + content)


class QQ_like:
    def __init__(self, qq_number):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        self.qq_number = qq_number
        self.get_preparameter()
        self.run_tolike()

    def get_preparameter(self):
        self.search_cookie()
        self.get_g_tk()
        self.get_space()

    def run_tolike(self):
        if os.path.exists('time_out2.txt'):
            with open('time_out.txt2', 'r') as f:
                self.time_out = f.read()
        else:
            self.time_out = None
        while True:#进入死循环状态,每隔几秒获取好友列表,开始Star
            self.get_friends_list()
            time.sleep(__import__('random').randint(0, 5))

    def search_cookie(self):#搜寻步骤1生成的cookie2文件
        with open('cookie_dict2.txt', 'r') as f:
            self.cookie = json.load(f)
        return True

    def get_g_tk(self):
        p_skey = self.cookie['p_skey']
        h = 5381
        for i in p_skey:
            h += (h << 5) + ord(i)
            self.g_tk = h & 2147483647

    def get_space(self):
        your_url = 'https://user.qzone.qq.com/' + str(self.qq_number)
        html = requests.get(your_url, headers=self.headers, cookies=self.cookie)
        if html.status_code == 200:
            self.qzonetoken = re.findall('window.g_qzonetoken =(.*?);', html.text, re.S)[0].split('"')
        return True

    def get_friends_list(self):
        times = ""
        url = "https://user.qzone.qq.com/proxy/domain/ic2.qzone.qq.com/cgi-bin/feeds/feeds3_html_more?"
        data = {
            'uin': self.qq_number,
            'scope': '0',
            'view': '1',
            'daylist': '',
            'uinlist': '',
            'gid': '',
            'flag': '1',
            'filter': 'all',
            'applist': 'all',
            'refresh': '0',
            'aisortEndTime': '0',
            'aisortOffset': '0',
            'getAisort': '0',
            'aisortBeginTime': '0',
            'pagenum': '1',
            'externparam': 'undefined',
            'firstGetGroup': '0',
            'icServerTime': '0',
            'mixnocache': '0',
            'scene': '0',
            'begintime': 'undefined',
            'count': '10',
            'dayspac': 'undefined',
            'sidomain': 'qzonestyle.gtimg.cn',
            'useutf8': '1',
            'outputhtmlfeed': '1',
            'rd': '0.9311604844249088',
            'usertime': str(round(time.time() * 1000)),
            'windowId': '0.51158950324406',
            'g_tk': self.g_tk,
            'qzonetoken': self.qzonetoken,
        }
        url = url + urllib.parse.urlencode(data) + '&g_tk=' + str(self.g_tk)
        html = requests.get(url, headers=self.headers, cookies=self.cookie)
        if html.status_code == 200:
            text = html.text[10:-2].replace(" ", "").replace('\n', '')
            json_list = demjson.decode(text)['data']['data']
            qq_spaces = json_list[0]
            with open('intxt2.txt', 'w', encoding='utf-8') as f5:
                html = qq_spaces['html']
                f5.write(str(html))

            content = str(qq_spaces['html'])
            try:
                zanshu = re.findall('<spanclass="f-like-cnt">(.*?)</span>人觉得很赞</div>', content, re.S)[0]
            except:
                zanshu = '0'
            try:
                people = re.findall('"visitor">浏览(.*?)</a>', content, re.S)[0]
            except:
                people = '0'
            try:
                txt = str(re.findall('"f-info">(.*?)<', content, re.S))
            except:
                txt = '0'  # None
            time_out = str(qq_spaces['feedstime'])
            print(str(qq_spaces['feedstime']))
            log("名字:" + str(qq_spaces['nickname']))
            log("QQ号:" + str(qq_spaces['opuin']))
            log("时间:" + time_out)
            log('赞数:' + zanshu)
            log('浏览次数:' + people)
            log('说说内容:' + txt)
            times = qq_spaces['abstime']
            his_url = re.findall('data-curkey="(.*?)"', content, re.S)[0]
            if not self.time_out or self.time_out != time_out:
                self.time_out = time_out
                self.get_zan(times, his_url)
                return True
            else:
                log('说说无更新,等待中...')
        else:
            log(html.status_code)

    def get_zan(self, times, his_url):
        data = {'g_tk': self.g_tk, 'qzonetoken': self.qzonetoken}
        post_data = {
            'qzreferrer': 'https://user.qzone.qq.com/' + str(qq_number),
            'opuin': str(qq_number),
            'unikey': str(his_url),
            'curkey': str(his_url),
            'from': '1',
            'appid': '311',
            'typeid': '0',
            'abstime': str(times),
            'fid': str(his_url).split('/')[-1],
            'active': '0',
            'fupdate': '1'
        }
        url = 'https://user.qzone.qq.com/proxy/domain/w.qzone.qq.com/cgi-bin/likes/internal_dolike_app?'
        url = url + urllib.parse.urlencode(data)
        html = requests.post(url, headers=self.headers, cookies=self.cookie, data=post_data)
        if html.status_code == 200:
            log("点赞成功" if len(html.text) == 493 else "点赞失败")
            # print(html.status_code)
            # print(html.text)
            # print(len(html.text)) #linux可能长度不是493,改一下即可
        else:
            log('点赞失败')
        with open('time_out2.txt', 'w') as f:
            f.write(str(times))


if __name__ == "__main__":
    qq_number = "账号"
    QQ_like(qq_number)
