from string import ascii_lowercase

alphabet = list(ascii_lowercase)

encoded = [1,12,6,15,14,19,15]

for i in range(-1, 26):
    print(''.join([alphabet[(num+i)%26] for num in encoded]))

