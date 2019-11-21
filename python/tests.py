#!/usr/bin/env python3
import huc

tests = {
	'0': ("⣥⣺⣩", "⠿⠺⠛⠞"),  # Digit Zero
	"00": ("⣥⣺⣩⣥⣺⣩", "⠿⠺⠛⠞⠿⠺⠛⠞"),  # 2 × Digit Zero
	'♯': ("⣥⡧⠋", "⠿⠧⠗⠄"),  # Music Sharp Sign
	'⠃': ("⣥⣇⠾", "⠿⠇⠽⠍"),  # Braille Pattern Dots-12
	'本': ("⣥⣯⣃", "⠿⠯⠏⠖"),  # CJK Unified Ideograph-672C (book)
	'𝄞': ("⣭⠆⢁", "⠿⠆⠂⠰"),  # Musical Symbol G Clef
	'📀': ("⣭⢤⣲", "⠿⠤⠬⠺"),  # DVD
	'😀': ("⣭⡤⣺", "⠿⠤⠵⠺"),  # Grinning Face
}

nbTest = len(tests)
err = 0.0
f = open("res.txt", "wb")


def printAndWriteFile(*args, **kwargs):
	global f
	f.write(''.join(args).encode())
	if "end" not in kwargs.keys():
		kwargs["end"] = '\n'
	if kwargs["end"]:
		f.write(kwargs["end"].encode())
	print(*args, **kwargs)

huc.print_ = printAndWriteFile
for i, (s, (expectedHUC8, expectedHUC6)) in enumerate(tests.items(), 1):
	testHUC8 = huc.convert(s)
	testHUC6 = huc.convert(s, True)
	printAndWriteFile("Test #%d: %s -> " % (i, s), end="")
	if testHUC8 == expectedHUC8 and testHUC6 == expectedHUC6:
		printAndWriteFile("PASS")
	else:
		if testHUC8 != expectedHUC8 and testHUC6 != expectedHUC6:
			printAndWriteFile("FAIL")
			err += 1
		else:
			printAndWriteFile("HALF FAIL")
			err += 0.5
		if testHUC8 != expectedHUC8:
			printAndWriteFile(
				"! Invalid HUC 8 result\n - Excepted: %s\n - Received: %s" %
				(expectedHUC8, testHUC8)
			)
			huc.convert(s, False, True)
		if testHUC6 != expectedHUC6:
			printAndWriteFile(
				"! Invalid HUC 6 result\n - Excepted: %s\n - Received: %s" %
				(expectedHUC6, testHUC6)
			)
			huc.convert(s, True, True)

printAndWriteFile("\nGrade: %.2f %%" % ((nbTest - err) / nbTest * 100))
f.close()
