import sys
responses = []
for num in sys.argv[1:]: responses.append(f"{'fizz' if int(num) % 3 == 0 else ''}{'buzz' if int(num) % 5 == 0 else ''}")
for i, r in enumerate(responses): print(f"{r if r!='' else sys.argv[i+1]}")