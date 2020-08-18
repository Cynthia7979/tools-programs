f = open('essay_material_word_sources.txt', encoding='utf-16-le')
fw = open('essay_material_word_sources_.txt', 'w', encoding='utf-8')
output = []

for l in f.readlines():
    print(l)
    if l and (l != ' ') and (l != '\n') and ('【' not in l) and ('】' not in l):
        fw.write(l.strip(' '))
        # print(output[-1])
    else: print('no')

# print(''.join(output))
