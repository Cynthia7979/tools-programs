import pint.errors
from colorama import Fore, Style
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
    'degree_Fahrenheit': 'degree_Celsius',
    # Speed
    'mile_per_hour': 'meter / second',
    'mile / hour': 'meter / second',
    'mile / second': 'meter / second'
}
# Based on https://en.wikipedia.org/wiki/Imperial_units#Units
# and https://www.splashlearn.com/math-vocabulary/measurements/customary-units

UNIT_ALIAS = {
    # Order tuple items from the longest to the shortest
    # Length
    'inch': ('inches', 'inch', 'in.', 'in', "''"),
    'foot': ('foot', 'feet', 'ft.', 'ft', "'"),
    'yard': ('yards', 'yard', 'yd.', 'yd'),
    'mile': ('miles', 'mile', 'mi.', 'mi'),
    # Weight
    'ounce': ('ounces', 'ounce', 'oz.', 'oz'),
    'pound': ('pounds', 'pound', 'pd.', 'pd', 'lb.s', 'lbs.', 'lbs', 'lb.', 'lb'),
    'ton': ('tons', 'ton', 't'),
    # Volume
    'fluid_ounce': (
        'fluid ounces', 'fluid ounce', 'fluid_ounce', 'fl ounces', 'fl ounce', 'fl. ounces', 'fl. ounce', 'floz.', 'floz',
        'fl. oz.', 'fl. oz', 'fl.oz', 'fl oz.', 'fl oz', 'fl.', 'fl'),
    'pint': ('pints', 'pint', 'pt.', 'pt'),
    'quart': ('quarts', 'quart', 'qt.', 'qt'),
    'gallon': ('gallons', 'gallon', 'gal.', 'gal'),
    # Temperature
    'degree_Fahrenheit': (
        'degree Fahrenheits', 'degree Fahrenheit', 'degree_Fahrenheit', 'deg Fahrenheits', 'deg Fahrenheit',
        'degFahrenheits', 'degFahrenheit', 'Fahrenheits', 'Fahrenheit', 'degF', '°F', 'oF', '^F', '.F', 'F.', 'F'
    ),
    # Speed
    'mile_per_hour': ('mile / hour', 'mph'),
    'mile / hour': ('miles / hour', 'miles / h', 'mis/hour', 'mis/h', 'mi./hour', 'mi./h', 'mi/hour', 'mi/h', 'mi / h', 'mi/ h', 'mi /h')
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

    def __eq__(self, other):
        assert isinstance(other, int) or isinstance(other, float), \
            f'You may only compare a number to the number in a NumberSegment instance. Got {type(other)}.'
        return other == float(self)

    def __add__(self, other):
        assert isinstance(other, int) or isinstance(other, float), \
            f'You may only add a number to the number in a NumberSegment instance. Got {type(other)}.'
        if isinstance(other, int) and self.is_int:
            return int(self) + other
        else:
            return float(self) + other

    def __getitem__(self, item):
        if not -3 < item < 2:
            raise IndexError(f'No more than 2 items are present in a NumberSegment instance. {item} required.')
        return (self.number_as_str, self.start_index)[item]

    def append(self, char: str):
        assert isinstance(char, str), \
            f'You may not append an instance of {type(char)} to a NumberSegment instance.'
        assert char.isdigit() or char == '.', \
            'You may not append a non-numerical and non-period character to a NumberSegment instance.'
        self.number_as_str += char

    @property
    def end_index(self):
        return self.start_index + len(self)

    @property
    def is_int(self):
        return int(float(self.number_as_str)) == float(self.number_as_str)


def main():
    ureg = UnitRegistry()
    while True:
        try:
            input_string = input('Enter string to be processed, ctrl+C to exit: \n> ').lower()

            for deliminator in (';', '\n', '\\n', ',', '|'):
                if deliminator in input_string:
                    if input(f'You included "{deliminator}" in your input. '
                        f'Do you want to enter the sections as separate inputs? (Y/n)') in ('Y', ''):
                        for substring in input_string.split(deliminator):
                            handle_string(substring, ureg)
                        break
                    else:
                        break
            handle_string(input_string, ureg)
        except Exception as e:
            print(Fore.RED, e, Style.RESET_ALL)
        finally:
            print('---------------------')


def handle_string(s, ureg):
    if s.startswith(' '):
        s = s.lstrip(' ')
    if s.endswith(' '):
        s = s.rstrip(' ')

    unit_from = get_unit_from(s, ureg)
    if unit_from is None:
        raise ValueError(f'Seriously? Your string {unit_from} doesn\'t even have a unit!')

    number_segments, numbers_end_at = get_number_segments(s)
    if number_segments is []:
        raise ValueError(f'Seriously? You need to at least provide a number value. There\'s none in {s}.')

    try:
        unit_to = TO_METRIC_UNIT[unit_from]
    except KeyError:
        raise ValueError(
            f'No (US-customary) imperial units found in the string! Please check again, there is also a list of available units in the source.')

    print(translate_string(number_segments, s, numbers_end_at, unit_from, unit_to, ureg))


def get_number_segments(s: str):
    number_segments = []
    start_new_segment = True
    number_ends_at = -1
    for i, char in enumerate(s):
        if char.isdigit() or (char in '.' and s[i-1].isdigit()):  # Account for "." in unit abbreviations.
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
    q_eval_ = ureg.Quantity
    for word in s.split():
        try:
            value_with_unit = q_eval_(word)
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


def translate_string(number_segments: list, original_string: str, end_of_numbers: int, unit_from: str, unit_to: str,
                     ureg: UnitRegistry):
    q_eval_ = ureg.Quantity
    unit_ = ureg.__getattr__  # Alias for getting appropriate Unit instance from string
    translated_string = ''
    last_segment_end = 0
    has_plural = False

    for nseg in number_segments:
        segment, segment_start = nseg
        segment_as_float = float(segment)
        translated_string += original_string[last_segment_end:segment_start]
        segment_as_quantity = q_eval_(segment_as_float, unit_(unit_from))
        converted_segment = segment_as_quantity.to(unit_(unit_to)).magnitude
        if converted_segment == int(converted_segment):  # Check if it's a whole number
            converted_segment = int(converted_segment)
        else:
            converted_segment = round(converted_segment, ROUND_TO_DIGITS)
        translated_string += str(converted_segment)
        last_segment_end = segment_start + len(segment)
        has_plural = (nseg != 1)
    
    translated_string += original_string[end_of_numbers:]
    translated_string = string_without_unit(translated_string, unit_from, ureg).rstrip(" ")

    if has_plural and unit_to == 'meter / second':  # Special plural rule
        return f'{translated_string} meters / second'
    else:
        return f'{translated_string} {unit_to + "s" if has_plural else unit_to}'   


def string_without_unit(s: str, unit_standard_name: str, ureg: UnitRegistry):
    try:
        ureg.__getattr__(unit_standard_name)
    except pint.errors.UndefinedUnitError:
        raise ValueError(f'{unit_standard_name} is not a unit.')

    if unit_standard_name not in UNIT_ALIAS.keys():
        alias_to_look_for = (unit_standard_name,)
    else:
        alias_to_look_for = UNIT_ALIAS[unit_standard_name]

    s_stripped = s
    for alias in alias_to_look_for:
        s_stripped = s_stripped.replace(alias, '')
    return s_stripped


if __name__ == '__main__':
    main()
