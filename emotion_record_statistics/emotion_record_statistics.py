"""
Notes on Emotion values:

Positive and negative moods correspond to negative and positive integers.
The magnitude of the integer represents the "level of caution" AKA how bad it is.
Currently anxiety and depression are both -10, which is the lowest.

Notes on marks:

"好" - End of a month
"适中" - End of the record
"差" - (Vacant style used for debug)
"""
# import xlrd
import openpyxl as xl
import logging

# workbook = xlrd.open_workbook(path)
# sheet = workbook.sheet_by_index(0)
# test_cell = sheet.cell(0,0)
# assert type(test_cell) is xlrd.sheet.Cell
# assert type(workbook) is xlrd.book.Book
# xf_index = test_cell.xf_index
# print(xf_index)
# xf_style = workbook.xf_list[xf_index]
# xf_background = xf_style.background
#
# fill_pattern = xf_background.fill_pattern
# pattern_colour_index = xf_background.pattern_colour_index
# background_colour_index = xf_background.background_colour_index
# print(background_colour_index)

PATH = 'emotion_record.xlsx'
PATH_ = 'D://情绪记录表.xlsx'
START_MONTH = 4
START_DATE = 16
LOGGING_LEVEL = logging.DEBUG


class Emotion(object):
    def __init__(self, style_name, color_name, value:int):
        self.style_name = style_name
        self.emotion_name = color_name
        self.value = value

    def __repr__(self):
        return self.emotion_name


class Day(object):
    def __init__(self, date:int, *emotions):
        self.date = date
        self.emotions = list(emotions) if emotions else []
        self.emotions_with_no_value = 0

    @property
    def avg_emotion(self):
        return sum((e.value for e in self.emotions)) / (len(self.emotions)-self.emotions_with_no_value)

    def add_emotion(self, emotion):
        assert isinstance(emotion, Emotion)
        self.emotions.append(emotion)
        if emotion.value == 0:
            self.emotions_with_no_value += 1

    def __repr__(self):
        return f'Day {self.date} with average {self.avg_emotion}'


class Month(object):  # It's too similar with Day!
    def __init__(self, month:int, *days):
        self.month = month
        self.days = list(days) if days else []
        self.days_with_no_value = 0

    @property
    def avg_emotion(self):
        return sum((day.avg_emotion for day in self.days)) / (len(self.days) - self.days_with_no_value)

    def add_day(self, day):
        assert isinstance(day, Day)
        self.days.append(day)
        if day.avg_emotion == 0:
            self.days_with_no_value += 1

    def __repr__(self):
        return f'Month {self.month} with days {tuple(self.days)} averaging {self.avg_emotion}'


MATCH_COLOR = {"着色 3": Emotion("着色 3", "numb", -2), "20% - 着色 6": Emotion("20% - 着色 6", "chilling out", 1), "常规": Emotion("常规", '(none)', 0),
          "着色 4": Emotion("着色 4", "anxious", -10), "60% - 着色 4": Emotion("60% - 着色 4", "nervous", -5),
          "着色 1": Emotion("着色 1", "depressed", -10), "60% - 着色 1": Emotion("60% - 着色 1", "frustrated", -5), "40% - 着色 1": Emotion("40% - 着色 1", "sad", -3),
          "着色 6": Emotion("着色 6", 'Ecstasy', 10), "60% - 着色 6": Emotion("60% - 着色 6", 'excited', 5), "40% - 着色 6": Emotion("40% - 着色 6", 'happy', 3),
          "着色 2": Emotion("着色 2", 'rage', 7), "60% - 着色 2": Emotion("60% - 着色 2", 'offended', 3)}


def main(test=True):
    """
    :param test: Use the demo file
    """
    global LOGGER

    default_ch = logging.StreamHandler()
    default_ch.setLevel(LOGGING_LEVEL)
    LOGGER = logging.getLogger('Emotion_record')
    LOGGER.setLevel(logging.DEBUG)
    LOGGER.addHandler(default_ch)

    workbook = xl.load_workbook(PATH) if test else xl.load_workbook(PATH_)
    sheet = workbook.active

    current_month_no = START_MONTH
    current_date_no = START_DATE
    current_month = Month(current_month_no)
    months = []
    LOGGER.debug('  '.join((str(x) for x in range(36))))
    for i, row in enumerate(sheet.iter_rows(min_row=2, max_col=36)):
        LOGGER.debug(str(i+2)+' '.join([c.style for c in row]))
        current_day = Day(current_date_no)
        for cell in row[4:]:
            current_day.add_emotion(MATCH_COLOR[cell.style])
        day_type = row[0].style
        if day_type == '好':  # Start of a month
            months.append(current_month)
            current_month_no += 1
            current_month = Month(current_month_no)
        elif day_type == '适中':  # End of the record
            current_month.add_day(current_day)
            months.append(current_month)
            break
        current_month.add_day(current_day)
        current_date_no += 1
    print(months)


if __name__ == '__main__':
    main(False)
