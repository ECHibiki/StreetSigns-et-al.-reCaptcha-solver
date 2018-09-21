import os

os.system('tsc -v')
print("Enter to start build loop...")
input()
loops = 0
while True:
	os.system('tsc --project tsconfig.json')
	print("fin\nEnter to loop #" +  str(loops) + "...")
	loops += 1
	input()