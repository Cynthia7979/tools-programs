# 算是博客？
所以，因为看到了USAD Super Quiz“广场”的乱象，加之正式测评时显示了发言人的姓名和学校，就想到了要做这样一个项目。

**需求**：
* 统计谁发言最多
* 统计哪个学校的发言最多
* 统计哪一句话被频繁发出
* 分词并制作词云

可惜的是，我没发现本地一次只保存400多条消息，导致最后救回来的只有500条消息不到。不过对于入门来说已经够了！（大概）

![图1](https://raw.githubusercontent.com/Cynthia7979/images/master/square.jpg)   
广场乱象：哪怕显示了学校和真名，选手们还是在刷屏、刷烂梗。

## 第一步：处理文件
Ctrl+I发现聊天框部分大约是这样一个架构：
```html
<div data-v-3911b543="" id="box-scrollTarget" class="box_right_frame_ul">
    <div data-v-3911b543="" class="box_right_frame_li">
        <div data-v-3911b543="" class="box_right_frame_li_img"><img data-v-3911b543="" src="//img.webloom.cn/img/logo/default-user.png" onerror="this.src='//img.webloom.cn/img/logo/default-user.png';this.onerror=null">
        </div> 
        <div data-v-3911b543="" class="box_right_frame_li_right"><div data-v-3911b543="" class="box_right_frame_li_right_name">
            <姓名>(<学校>)
        </div> 
        <div data-v-3911b543="" class="box_right_frame_li_right_text">
            <发言内容>
        </div>
    </div>
    <div data-v-3911b543="" class="box_right_frame_li">
        （同样格式的第二条发言）
    </div>
    以此类推
</div>
```

也就是说，通过查找`class`为`box_right_frame_li_right`的div可以获得发言人的学校和姓名；查找`class`为`box_right_frame_li_right_text`的div则可以获得发言内容。

因为~~懒得~~不会写爬虫，我的数据是直接拷贝下来的（）因为前面的意外导致只剩下了500条左右的消息。

那么现在就可以上手提取数据了，用的是`BeautifulSoup`。这里为了简洁（真的吗）定义了一个Person类：

```python
class Person(object):
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.spoken = []  # 这个人发过的所有消息

    def add_line(self, sentence):
        self.spoken.append(sentence)

    def __repr__(self):
        return f'Person{{{self.name}({self.school}): {self.spoken}}}'
```

后来事实证明这里用类是非常好的选择。

剩下的就是用好看的汤处理html了，贴一下我用来copy的[官方中文文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc.zh)
```python
def process(path='record.txt'):
    f = open(path, encoding='utf-8')  # 默认gbk读中文会出错
    talk_record = f.read()
    soup = BeautifulSoup(talk_record, "html.parser")
    people = {}
    all_sentences = []
    for i in soup.find_all('div', class_='box_right_frame_li_right_name'):  # Get names and corresponding schools
        nm,scl = i.text[:-1].strip().split('(')  # [:-1]去掉括回，split切分姓名和学校。我真没想骂人
        line = i.find_next_sibling('div', class_='box_right_frame_li_right_text').text.strip().strip(' ').strip('   ')
        if nm in people.keys():
            people[nm].add_line(line)
        else:
            this_person = Person(nm, scl)
            this_person.add_line(line)
            people[nm] = this_person
        all_sentences.append(line)
    return people, all_sentences
```
最后返回的就是所有说过话的人名，对应的学校以及消息，还有一个包含所有消息的列表。

## 数据分析
我对数据分析的认识仅限于最大最小中位数etc……所以这里就做一些比较低端的统计好了。

（以及我现在才知道还可以这么写……知识增加.jpg）  
```python
def main():
    analyze(*process())
```
\* analyze的参数和process的返回值相对应

注：以下三级标题内的代码都写在`analyze(names, sentences)`里面

### 谁发言最多
```python
    most_frequent_chatting = {}
    for p in names.values():
        number_of_lines = len(p.spoken)  
        # 上文的Person类就用在这里。好处是可以简单地处理很多相关联的数据，坏处是没法像下面那样封装。
        if number_of_lines in most_frequent_chatting:
            most_frequent_chatting[number_of_lines].append(p.name)
        else:
            most_frequent_chatting[number_of_lines] = [p.name]
    print([[f'{s}({k})' for s in most_frequent_chatting[k]] for k in reversed(sorted(most_frequent_chatting))])
```
其实就是一个简单且没有任何优化的想法的统计……

最后一句代码拆分解释一下~~怕我自己忘掉~~：`reversed(sorted(most_frequent_chatting))`返回一个整数（“发言次数”）列表，大小由高到低。
我需要的是爱说话的人名而不是说话次数，所以我以发言次数为次序，获取说了那么多次话的人名们：`most_frequent_chatting[k]`。
最后，在`f'{s}({k})'`中，s是人名，k是作为`most_frequent_chatting`字典键的发言次数。

现在看来这个方法有用是因为大部分人说话次数都一样（1-2次）。如果对于运营时间较久的论坛，这个*大概*就会跑得慢一点，因为键更多，会花更多的时间排序（

因为涉及人名和校名就不粘结果了，想看可以自己去跑。

PS这里for循环就是下面用到的`rough_statistics()`的原型：
```python
def rough_statistics(lst=[], ocrence=[], return_ocrence=False, filter=False):
    if not ocrence:
        ocrence = {}
        for s in lst:
            if filter and s in (' ', '️', '\n', '的', '你', '了', '我', '，', ''):continue
            if s in ocrence:
                ocrence[s].append(s)
            else:
                ocrence[s] = [s]
    most_frequent = {}
    for s, l in ocrence.items():
        number_of_occurrence = len(l)
        if number_of_occurrence in most_frequent:
            most_frequent[number_of_occurrence].append(s)
        else:
            most_frequent[number_of_occurrence] = [s]
    if return_ocrence: return most_frequent, ocrence
    return most_frequent
```
我爱封装.jpg

### 哪个学校的人最爱说话
纯娱乐，非地图炮。

这东西我忘写了再见（喂

### 哪一条消息大家最爱说？
这里用到了上文的`rough_statistics()`，两行完事：
```python
    most_frequently_said = rough_statistics(lst=sentences)
    print([[f'{s}({k})' for s in most_frequently_said[k]] for k in reversed(sorted(most_frequently_said))])
```
结果（截止到频数2）
```
[['冲(4)'], ['肖 战 必 糊 肖 战 必 糊 肖 战 必 糊(3)', '日你大坝(3)'], ['刘昊晟别搞刘昊晟别搞刘昊晟别搞刘昊晟别搞刘昊晟别搞刘昊晟别搞(2)', 'ijo 的地盘！！！ijo 的地盘！！！ijo 的地盘！！！(2)', '有1吗(2)', '卢本伟卢本伟卢本伟卢本伟卢本伟卢本伟卢本伟卢本伟卢本伟卢本伟(2)', '大坝(2)', '冲冲冲！！！(2)', '海音瘫！海音瘫！海音瘫！海音瘫！海音瘫！海音瘫！海音瘫！(2)', 'bilibili- ( ゜- ゜)つロ 乾杯~！！！(2)', '害怕(2)', '10(2)', '冲冲冲(2)', '5(2)', '*(2)']```
```

### 在？热词？
抱着顺便学一下结巴分词的心态，我学了结巴分词（？
其实是个特别简单的模块，我是直接看它[repo](https://github.com/fxsjy/jieba)的README学的（（

把分出来的词装到列表里
```python
    words = []
    for s in sentences:
        words.extend(jieba.cut(s.strip(' ')))
```

频率统计
```python
    most_frequently_used = rough_statistics(lst=words, filter=True)
    print([[f'{s}({k})' for s in most_frequently_used[k]] for k in reversed(sorted(most_frequently_used))])
```

输出（取最靠前的一些）
```
[['！(144)'], ['❤(47)'], ['？(42)'], ['鎩(40)'], ['。(36)'], ['卢本伟(24)'], ['鼊(19)'], ['!(16)'], ['*(15)'], ['海音(14)', '瘫(14)'], ['刘昊晟(12)', '别搞(12)'], ['肖(11)', '战(11)'], ['冲(10)'], ['必(9)', '糊(9)', '表白(9)'],
```

词云用的是`wordcloud`，参考的是[~~维基~~文档](https://amueller.github.io/word_cloud/index.html)和[这篇博文](https://blog.csdn.net/ydydyd00/article/details/80665028)
```python
wordcloud = WordCloud(font_path="C:\Windows\Fonts\msyhl.ttc",
                          collocations=False,
                          background_color="white",
                          colormap='Dark2',
                          height=728,
                          width=1024).generate(' '.join(words))
    image_produce = wordcloud.to_image()
    image_produce.show()
```
大概就是把刚分好的词用一种易 于 阅 读的方式接回去，然后调试一下创建WordCloud对象并生成图像就可以了。

那么，结果：
![图2](https://raw.githubusercontent.com/Cynthia7979/tools-programs/master/square_chat_analyzer/result.png)

emm我也不知道这种发在公共空间的姓名应不应该打码……如果有影响请私信我或者开issue！

## ……你是不是忘了什么？
接下来要做的事：
* 按学校统计发消息频率
* ~~成功~~安装并学习`matplotlib`，制作学校和个人说话频率的饼图
