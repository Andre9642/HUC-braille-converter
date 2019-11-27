#!/usr/bin/env python3
import sys
import huc

tests_unicodeBraille = {
	'0': ("⣥⣺⣩", "⠿⠺⠛⠞"),  # Digit Zero
	"00": ("⣥⣺⣩⣥⣺⣩", "⠿⠺⠛⠞⠿⠺⠛⠞"),  # 2 × Digit Zero
	'♯': ("⣥⡧⠋", "⠿⠧⠗⠄"),  # Music Sharp Sign
	'⠃': ("⣥⣇⠾", "⠿⠇⠽⠍"),  # Braille Pattern Dots-12
	'本': ("⣥⣯⣃", "⠿⠯⠏⠖"),  # CJK Unified Ideograph-672C (book)
	'𝄞': ("⣭⠆⢁", "⠿⠆⠂⠰"),  # Musical Symbol G Clef
	'📀': ("⣭⢤⣲", "⠿⠤⠬⠺"),  # DVD
	'😀': ("⣭⡤⣺", "⠿⠤⠵⠺"),  # Grinning Face
	'\uffff': ("⣥⠀⠀", "⠿⠀⠀⠄"),
	chr(0xffff0): ("⣵⠚⠀⣠", "⠿⠀⠀⠾⠄")
}

tests_braillePatterns = {
	'\u12c3': ("13678-137-2356", "123456-13-136-134"),
	"\u12c3\u12c3": ("13678-137-2356-13678-137-2356", "123456-13-136-134-123456-13-136-134"),
	chr(0xfffe5): ("135678-245-0-358", "123456-0-6-1356-3"),
	chr(0x409e0): ("135678-234568-24567-5678", "123456-2456-16-23456-1345"),
	chr(0x0010febf): ("135678-1678-8-45", "123456-0-456-36-136")
}

tests_HUC8SwitchDotLevels = {
	"1245": "3678",
	"3678": "1245",
}

nbTest = len(tests_unicodeBraille)
err = 0.0
f = open("res.txt", "wb")


def printAndWriteFile(*args, **kwargs):
	global f
	if "end" not in kwargs.keys(): kwargs["end"] = '\n'
	if "sep" not in kwargs.keys(): kwargs["sep"] = ' '
	f.write((kwargs["sep"]).join(args).encode())
	if kwargs["end"]: f.write(kwargs["end"].encode())
	try: print(*args, **kwargs)
	except UnicodeEncodeError:
		print(*[arg.encode().decode(sys.stdout.encoding, "backslashreplace") for arg in args], **kwargs)

huc.print_ = printAndWriteFile

printAndWriteFile("== Unicode braille tests ==")
for i, (s, (expectedHUC8, expectedHUC6)) in enumerate(tests_unicodeBraille.items(), 1):
	testHUC8 = huc.convert(s, HUC6=False)
	testHUC6 = huc.convert(s, HUC6=True)
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
			huc.convert(s, HUC6=False, debug=True)
		if testHUC6 != expectedHUC6:
			printAndWriteFile(
				"! Invalid HUC 6 result\n - Excepted: %s\n - Received: %s" %
				(expectedHUC6, testHUC6)
			)
			huc.convert(s, HUC6=True, debug=True)

printAndWriteFile("\n== Braille patterns tests ==")

nbTestsAlreadyDone = nbTest
nbTest += len(tests_braillePatterns)

for i, (s, (expectedHUC8, expectedHUC6)) in enumerate(tests_braillePatterns.items(), 1):
	testHUC8 = huc.convert(s, unicodeBraille=False, HUC6=False)
	testHUC6 = huc.convert(s, unicodeBraille=False, HUC6=True)
	printAndWriteFile("Test #%d (#%d): %s -> " % (i, (nbTestsAlreadyDone+i), s), end="")
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
		if testHUC6 != expectedHUC6:
			printAndWriteFile(
				"! Invalid HUC 6 result\n - Excepted: %s\n - Received: %s" %
				(expectedHUC6, testHUC6)
			)

printAndWriteFile("\n== HUC8 switch level dots tests ==")

nbTestsAlreadyDone = nbTest
nbTest += len(tests_HUC8SwitchDotLevels)

for i, (s, expectedOut) in enumerate(tests_HUC8SwitchDotLevels.items(), 1):
	res = huc.convertHUC8(s)
	printAndWriteFile("Test #%d (#%d): %s -> " % (i, (nbTestsAlreadyDone+i), s), end="")
	if res == expectedOut:
		printAndWriteFile("PASS")
	else:
		printAndWriteFile("FAIL")
		err += 1
		printAndWriteFile(
				"! Invalid result\n - Excepted: %s\n - Received: %s" %
				(expectedOut, res)
			)

printAndWriteFile("\nGrade: %.2f %%" % ((nbTest - err) / nbTest * 100))
f.close()
sys.exit(int(err))