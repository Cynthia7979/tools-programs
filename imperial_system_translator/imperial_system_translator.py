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
