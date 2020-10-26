from colorama import init; init()
print("\033[=19h")
for i in range(256):
	print(f"\033[{i}m{i}")
while 1:1