word_list = []
f = open('verbs.txt')
removed = 0
for line in f.readlines():
    if line not in word_list:
        word_list.append(line)
    else:
        print('removed:', line.strip('\n'))
        removed += 1
print('Total removed:', removed)
f.close()
f = open('verbs.txt', 'w')
f.write(''.join(word_list))
