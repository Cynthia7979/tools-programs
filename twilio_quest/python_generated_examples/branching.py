import sys
a, b = [int(i) for i in sys.argv[1:3]]
if a+b <= 0: print("You have chosen the path of destitution.")
elif a+b > 1 and a+b <= 100: print("You have chosen the path of plenty.")
else: print("You have chosen the path of excess")