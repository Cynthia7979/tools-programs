from bs4 import BeautifulSoup
import jieba
from wordcloud import WordCloud


class Person(object):
    def __init__(self, name, school):
        self.name = name
        self.school = school
        self.spoken = []

    def add_line(self, sentence):
        self.spoken.append(sentence)

    def __repr__(self):
        return f'Person{{{self.name}({self.school}): {self.spoken}}}'


def main():
    analyze(*process())


def process(path='record.txt'):
    f = open(path, encoding='utf-8')
    talk_record = f.read()
    soup = BeautifulSoup(talk_record, "html.parser")
    people = {}
    all_sentences = []
    for i in soup.find_all('div', class_='box_right_frame_li_right_name'):  # Get names and corresponding schools
        nm,scl = i.text[:-1].strip().split('(')
        line = i.find_next_sibling('div', class_='box_right_frame_li_right_text').text.strip().strip(' ').strip('   ')
        if nm in people.keys():
            people[nm].add_line(line)
        else:
            this_person = Person(nm, scl)
            this_person.add_line(line)
            people[nm] = this_person
        all_sentences.append(line)
    print(people)
    print(all_sentences)
    # for i in soup.find_all('div', class_='box_right_frame_li_right_text'):
    #     all_sentences.append(i.text.strip().strip("\n"))
    # print(all_sentences)
    return people, all_sentences


def analyze(names, sentences):
    most_frequent_chatting = {}
    for p in names.values():
        number_of_lines = len(p.spoken)
        if number_of_lines in most_frequent_chatting:
            most_frequent_chatting[number_of_lines].append(p.name)
        else:
            most_frequent_chatting[number_of_lines] = [p.name]
    print([[f'{s}({k})' for s in most_frequent_chatting[k]] for k in reversed(sorted(most_frequent_chatting))])

    # Rough statistics
    most_frequently_said = rough_statistics(lst=sentences)
    print([[f'{s}({k})' for s in most_frequently_said[k]] for k in reversed(sorted(most_frequently_said))])

    # Cut words
    # jieba.add_word('肖战')
    # jieba.add_word('6', freq=1000)
    # jieba.add_word('牛逼')
    # jieba.add_word('肖 战 必 糊', freq=1000)

    words = []
    for s in sentences:
        words.extend(jieba.cut(s.strip(' ')))
    print(words)
    most_frequently_used = rough_statistics(lst=words, filter=True)
    print([[f'{s}({k})' for s in most_frequently_used[k]] for k in reversed(sorted(most_frequently_used))])
    # words.extend(list('38xm3m9jejerxwerh2384u\'噢欸软媒软件而绝非是开发商开门方式可能让她'))
    wordcloud = WordCloud(font_path="C:\Windows\Fonts\msyhl.ttc",
                          collocations=False,
                          background_color="white",
                          colormap='Dark2',
                          height=728,
                          width=1024).generate(' '.join(words))
    image_produce = wordcloud.to_image()
    wordcloud.to_file('result.png')
    image_produce.show()


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


if __name__ == '__main__':
    main()