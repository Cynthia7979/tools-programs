import pint.errors
from pint import UnitRegistry

ROUND_TO_DIGITS = 3

TO_METRIC_UNIT = {
    # Length
    'inch': 'centimeter',
    'hand': 'centimeter',
    'foot': 'meter',
    'yard': 'meter',
    'mile': 'kilometer',
    'nautical_mile': 'kilometer',
    # Area
    'inch ** 2': 'centimeter ** 2',
    'foot ** 2': 'meter ** 2',
    'acre': 'meter ** 2',
    'yard ** 2': 'meter ** 2',
    'mile ** 2': 'kilometer ** 2',
    # Weight
    'grain': 'milligram',
    'ounce': 'gram',
    'pound': 'kilogram',
    'quarter': 'kilogram',
    'ton': 'metric_ton',
    # Volume
    'fluid_ounce': 'milliliter',
    'cup': 'milliliter',
    'pint': 'liter',
    'quart': 'liter',
    'gallon': 'liter',
    # Temperature
    'degree_Fahrenheit': 'degree_Celsius'
}
# Based on https://en.wikipedia.org/wiki/Imperial_units#Units
# and https://www.splashlearn.com/math-vocabulary/measurements/customary-units

UNIT_ALIAS = {
    # Length
    'inch': ('inch', 'inches', 'in', 'in.', "''"),
    'foot': ('foot', 'feet', 'ft', 'ft.', "'"),
    'yard': ('yard', 'yards', 'yd', 'yd.'),
    'mile': ('mile', 'miles', 'mi', 'mi.'),
    # Weight
    'ounce': ('ounce', 'ounces', 'oz', 'oz.'),
    'pound': ('pound', 'pounds', 'pd', 'pd.'),
    'ton': ('ton', 'tons', 't'),
    # Volume
    'fluid_ounce': ('fluid ounce', 'fluid_ounce', 'fluid ounces', 'fl ounce', 'fl ounces', 'fl. ounce', 'fl. ounces', 'floz', 'floz.', 'fl oz', 'fl. oz', 'fl.oz', 'fl oz.', 'fl. oz.', 'fl', 'fl.'),
    'pint': ('pint', 'pints', 'pt', 'pt.'),
    'quart': ('quart', 'quarts', 'qt', 'qt.'),
    'gallon': ('gallon', 'gallons', 'gal', 'gal.'),
    # Temperature
    'degree_Fahrenheit': ('degree Fahrenheit', 'degree_Fahrenheit', 'degree Fahrenheits', 'Fahrenheit', 'Fahrenheits', '°F', 'oF', '^F', '.F', 'F')
}


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
        assert isinstance(other, int) or isinstance(other, float) or isinstance(other, str), \
            f'You may not add an instance of {type(other)} to a NumberSegment instance.'
        return self.number_as_str + str(other)

    def __getitem__(self, item):
        if not -3 < item < 2:
            raise IndexError(f'No more than 2 items are present in a NumberSegment instance. {item} required.')
        return (self.number_as_str, self.start_index)[item]

    def append(self, char):
        # TODO: Check if char is digit or int or float or "." Typically just checking for str is okay, maybe need to
        # change __add__
        self.number_as_str += char

    @property
    def end_index(self):
        return self.start_index + len(self)

    @property
    def is_int(self):
        return int(float(self.number_as_str)) == float(self.number_as_str)


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
                number_segments.append(NumberSegment(char, i))
                start_new_segment = False
            else:
                number_segments[-1].append(char)
        else:
            if not start_new_segment:
                start_new_segment = True
                number_ends_at = i
    return number_segments, number_ends_at


def get_unit_from(s: str, ureg: UnitRegistry):
    Q_ = ureg.Quantity
    for word in s.split():
        try:
            value_with_unit = Q_(word)
            if value_with_unit.dimensionless:
                continue
            unit_name = str(value_with_unit.units)
            if unit_name == 'femtoliter':
                return 'fluid_ounce'
            else:
                return str(value_with_unit.units)
        except (ValueError, pint.errors.UndefinedUnitError, AttributeError):
            continue
    return None


def translate_string(number_segments: list, original_string: str, end_of_numbers: int, unit_from: str, unit_to: str, ureg: UnitRegistry):
    unit_ = ureg.__getattr__  # Alias for getting appropriate Unit instance from string
    translated_string = ''
    last_segment_end = 0
    for nseg in number_segments:
        segment, index = nseg
        segment_as_number = float(segment)
        translated_string += original_string[last_segment_end:index]
        segment_as_quantity = segment_as_number * unit_(unit_from)
        converted_segment = segment_as_quantity.to(unit_(unit_to)).magnitude
        if nseg.is_int:
            converted_segment = int(converted_segment)
        else:
            converted_segment = round(converted_segment, ROUND_TO_DIGITS)
        translated_string += str(converted_segment)
        last_segment_end = index + len(segment)
    translated_string += original_string[end_of_numbers:]
    return f'{string_without_unit(translated_string, unit_from, ureg).rstrip(" ")} {unit_to}'  # TODO: Add s if none of the numbers are plural


def string_without_unit(s: str, unit_standard_name: str, ureg: UnitRegistry):
    try:
        ureg.__getattr__(unit_standard_name)
    except pint.errors.UndefinedUnitError:
        raise ValueError(f'{unit_standard_name} is not a unit.')

    if unit_standard_name not in UNIT_ALIAS.keys():
        alias_to_look_for = (unit_standard_name,)
    else:
        alias_to_look_for = UNIT_ALIAS[unit_standard_name]

    for alias in alias_to_look_for:
        s_stripped = s.rstrip(alias)
        if s_stripped != s:
            return s_stripped
    return s


if __name__ == '__main__':
    main()
