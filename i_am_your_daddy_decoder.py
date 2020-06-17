from string import ascii_lowercase

alphabet = list(ascii_lowercase)

encoded = [1,12,6,15,14,19,15]

print(''.join([alphabet[num-1] for num in encoded]))

