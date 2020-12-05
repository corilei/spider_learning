import pandas as pd
import requests
from bs4 import BeautifulSoup


# <li>
# <div class="box">
# <div class="img">
# <a class="sort znyj" date-category="40" href="https://www.leiphone.com/category/weiwu">智能硬件</a>
# <a href="https://www.leiphone.com/news/202010/2TevhxwiaF7SV7sX.html" target="_blank">
# <img alt="" class="lazy" data-original="https://static.leiphone.com/uploads/new/article/pic/202010/5f867c6872b52.jpg?imageMogr2/thumbnail/!480x290r/gravity/Center/crop/480x290/quality/90" src="https://www.leiphone.com/resWeb/images/article/miss-main-pic.jpg" title="苹果99美元的HomePod mini，其实是台家庭“对讲机”"/>
# </a>
# </div>
# <div class="word">
# <h3>
# <a class="headTit" href="https://www.leiphone.com/news/202010/2TevhxwiaF7SV7sX.html" target="_blank" title="苹果99美元的HomePod mini，其实是台家庭“对讲机”">
# 				苹果99美元的HomePod mini，其实是台家庭“对讲机”                			</a>
# </h3>
# <div class="des">
# 				一台家庭对讲机？			</div>
# <div class="msg clr">
# <a class="aut" href="https://www.leiphone.com/author/wangjinwang620" rel="nofollow" target="_blank">
# <img alt="" height="50" src="https://www.leiphone.com/uploads/new/avatar/author_avatar/5b7e9d44ddfe4_100_100.jpeg" width="50"/>王金旺				</a>
# <div class="time">3小时前</div>
# <div class="tags">
# <em></em>
# <a href="https://www.leiphone.com/tag/%E8%8B%B9%E6%9E%9C" target="_blank" title="苹果">苹果</a><a href="https://www.leiphone.com/tag/HomePod+mini" target="_blank" title="HomePod mini">HomePod mini</a> </div>
# </div>
# </div>
# </div>
# </li>

# <li>
# <div class="box">
# <div class="img">
# <a class="sort qt" date-category="137" href="https://www.leiphone.com/category/yanxishe">人工智能开发者</a>
# <a href="https://www.leiphone.com/news/202010/nBw1rUusEedxxs4x.html" target="_blank">
# <img alt="" class="lazy" data-original="https://static.leiphone.com/uploads/new/article/pic/202010/5f866c5226283.png?imageMogr2/thumbnail/!480x290r/gravity/Center/crop/480x290/quality/90" src="https://www.leiphone.com/resWeb/images/article/miss-main-pic.jpg" title="谷歌AI:推进实例级别识别 (ILR)研究"/>
# </a>
# </div>
# <div class="word">
# <h3>
# <a class="headTit" href="https://www.leiphone.com/news/202010/nBw1rUusEedxxs4x.html" target="_blank" title="谷歌AI:推进实例级别识别 (ILR)研究">
# 				谷歌AI:推进实例级别识别 (ILR)研究                			</a>
# </h3>
# <div class="des">
# 				实例级识别（ILR）是识别一个物体的特定实例而不是简单识别出所属类别的计算机视觉任务。			</div>
# <div class="msg clr">
# <a class="aut" href="https://www.leiphone.com/author/leifengzimuzu2326" rel="nofollow" target="_blank">
# <img alt="" height="50" src="https://www.leiphone.com/uploads/new/avatar/05/03/40/38_avatar_pic_100_100.jpg?updateTime=1" width="50"/>雷锋字幕组				</a>
# <div class="time">5小时前</div>
# <div class="tags">
# <em></em>
# <a href="https://www.leiphone.com/tag/%E5%9B%BE%E5%83%8F%E8%AF%86%E5%88%AB" target="_blank" title="图像识别">图像识别</a><a href="https://www.leiphone.com/tag/%E8%AE%A1%E7%AE%97%E6%9C%BA%E8%A7%86%E8%A7%89" target="_blank" title="计算机视觉">计算机视觉</a> </div>
# </div>
# </div>
# </div>
# </li>

def get_data(ui):
    try:
        ri = requests.get(url=ui)
        soupi = BeautifulSoup(ri.text, 'lxml')
        # 访问页面 + 页面解析
        infors = soupi.find('div', class_="lph-pageList index-pageList").find_all('div', class_="box")
        lst = []
        for i in infors:
            dic = {}
            dic['分类'] = i.find('div', class_="img").a.text.replace('\n', '')
            dic['图片url'] = i.find('div', class_="img").find('a', target="_blank").attrs['href']
            dic['标题'] = i.find('div', class_="word").find('a').attrs['title']
            dic['描述'] = i.find('div', class_="word").find('div', class_="des").text.strip()
            dic['作者'] = i.find('div', class_="word").find('a', class_="aut").text.strip()
            dic['发布时间'] = i.find('div', class_="word").find('div', class_="time").text.strip()
            # 获取标签
            tags = i.find('div', class_="word").find('div', class_="tags").find_all('a')
            lst_tags = []
            for j in tags:
                lst_tags.append(j.text.strip())
            dic['标签'] = lst_tags
            lst.append(dic)
        return lst

    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    url = "https://www.leiphone.com/"
    # 获取数据，未解决翻页问题
    data = []
    for page_num in range(3001, 4540):
        url = "https://www.leiphone.com/page/{}".format(page_num)
        print(url)
        data_temp = get_data(url)
        if data_temp is not None:
            data = data + data_temp
    # 转换格式
    df = pd.DataFrame(data)
    # 保存csv文件
    fileName = './lei_feng_data_3001_4539.csv'
    df.to_csv(fileName, index=False, encoding='UTF-8')
    print('Save data success!')

#
# 2、np数组储存
