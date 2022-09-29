import pint.errors
from pint import UnitRegistry, Unit


TO_METRIC_UNIT = {
    # Lengths
    Unit('inch'): Unit('centimeter'),
    Unit('hand'): Unit('centimeter'),
    Unit('foot'): Unit('meter'),
    Unit('yard'): Unit('meter'),
    Unit('mile'): Unit('kilometer'),
    Unit('nautical_mile'): Unit('kilometer'),
    # Areas
    Unit('inch ** 2'): Unit('centimeter ** 2'),
    Unit('foot ** 2'): Unit('meter ** 2'),
    Unit('acre'): Unit('meter ** 2'),
    Unit('yard ** 2'): Unit('meter ** 2'),
    Unit('mile ** 2'): Unit('kilometer ** 2'),
    # Weights
    Unit('grain'): Unit('milligram'),
    Unit('ounce'): Unit('gram'),
    Unit('pound'): Unit('kilogram'),
    Unit('quarter'): Unit('kilogram'),
    Unit('ton'): Unit('metric_ton'),
    # Volumes
    Unit('fluid_ounce'): Unit('milliliter'),
    Unit('cup'): Unit('milliliter'),
    Unit('pint'): Unit('liter'),
    Unit('quart'): Unit('liter'),
    Unit('gallon'): Unit('liter'),
    # Temperatures
    Unit('degree_Fahrenheit'): Unit('degree_Celsius')
}
# Based on https://en.wikipedia.org/wiki/Imperial_units#Units
# and https://www.splashlearn.com/math-vocabulary/measurements/customary-units


class NumberSegment:
    def __init__(self, number_as_str, start_index):
        self.number_as_str = number_as_str
        self.start_index = start_index

    def __len__(self):
        return len(self.number_as_str)

    def __int__(self):
        return int(self.number_as_str)

    def __float__(self):
        return float(self.number_as_str)

    def __add__(self, other):
        assert isinstance(other, int) or isinstance(other, float) or isinstance(other, str), f'You may not add an' \
                                                                                             f'instance of {type(other)}' \
                                                                                             f'to a NumberSegment instance.'
        return self.number_as_str + str(other)

    def __getitem__(self, item):
        assert -3 < item < 2, IndexError(f'No more than 2 items are present in a NumberSegment instance. {item} required.')
        return (self.number_as_str, self.start_index)[item]

    def append(self, char):
        self.number_as_str += char

    @property
    def end_index(self):
        return self.start_index + len(self)

    @property
    def is_int(self):
        return int(self.number_as_str) == float(self.number_as_str)


def main():
    ureg = UnitRegistry()
    input_string = input('Enter string to be processed: ')

    unit_from = get_unit_from(input_string, ureg)
    if unit_from is None:
        raise ValueError(f'Seriously? Your string {unit_from} doesn\'t even have a unit!')

    number_segments, numbers_end_at = get_number_segments(input_string)
    if number_segments is []:
        raise ValueError(f'Seriously? You need to at least provide a number value. There\'s none in {input_string}.')

    try:
        unit_to = TO_METRIC_UNIT[unit_from]
    except KeyError:
        raise ValueError(f'No (US-customary) imperial units found in the string! Please check again, there is also a list of available units in the source.')

    print(translate_string(number_segments, input_string, numbers_end_at, unit_from, unit_to, ureg))


def get_number_segments(s: str):
    number_segments = []
    start_new_segment = True
    number_ends_at = -1
    for i, char in enumerate(s):
        if char.isdigit() or char in '.':
            if start_new_segment:
                # print('start new segment,', char, i)
                number_segments.append(NumberSegment(char, i))
                start_new_segment = False
            else:
                # print('no start new segment,', char, i)
                number_segments.append(char)
        else:
            if not start_new_segment:
                # print('end of segment', char, i)
                start_new_segment = True
                number_ends_at = i
    return number_segments, number_ends_at


def get_unit_from(s: str, ureg: UnitRegistry):
    with ureg.Quantity as Q_:
        for word in s.split():
            try:
                value_with_unit = Q_(word)
                if value_with_unit.units == Unit('dimensionless'):
                    continue
                return value_with_unit.units
            except (ValueError, pint.errors.UndefinedUnitError, AttributeError):
                continue
        return None


def translate_string(number_segments: list, original_string: str, end_of_numbers: int, unit_from: Unit, unit_to: Unit, ureg: UnitRegistry):
    with ureg.Quantity as Q_:
        translated_string = ''
        last_segment_end = 0
        for segment, index in number_segments:
            segment_as_number = int(segment) if segment.is_int else float(segment)
            translated_string += original_string[last_segment_end:index]
            translated_string += (Q_(segment_as_number) * Q_(unit_from)).to(unit_to)
            last_segment_end = index + len(segment)
        translated_string += original_string[end_of_numbers:]
        return f'{translated_string} {unit_to}'


def skeleton_main():
    input_string = input('Enter string to be processed: ')
    number_segments = []
    number_ends_at = -1
    start_new_segment = True
    unit_from = None
    for i, char in enumerate(input_string):
        if char.isdigit() or char in '.':
            if start_new_segment:
                # print('start new segment,', char, i)
                number_segments.append([char, i])
                start_new_segment = False
            else:
                # print('no start new segment,', char, i)
                number_segments[-1][0] += char
        else:
            if not start_new_segment:
                # print('end of segment', char, i)
                start_new_segment = True
                number_ends_at = i
            # else:
                # print('not a digit', char, i)
    if any([imp_unit in input_string for imp_unit in ('inches', 'in', 'inch', "''")]):
        unit_from = 'inches'
        input_string = input_string.strip('inches').strip('in').strip('inch').strip("''")
        input_string = input_string.rstrip(' ')
    if unit_from == 'inches':
        translated_string = ''
        last_segment_end = 0
        for segment, index in number_segments:
            # print(segment, index)
            translated_string += input_string[last_segment_end:index]
            # print(translated_string, 'midprocess')
            translated_string += str(float(segment) * 2.54)
            # print(translated_string)
            last_segment_end = index + len(segment)
        translated_string += input_string[number_ends_at:]
        print(translated_string, 'cm')


skeleton_main()
