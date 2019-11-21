#!/usr/bin/env python3
import re

HUC6_patterns = {
	"⠿…⠄": (0x0000, 0xFFFF),
	"⠿…⠠": (0x10000, 0x1FFFF),
	"⠿…⠤⠇": (0x20000, 0x2FFFF),
	"⠿…⠤⠍": (0x30000, 0x3FFFF),
	"⠿…⠤⠝": (0x40000, 0x4FFFF),
	"⠿…⠤⠕": (0x50000, 0x5FFFF),
	"⠿…⠤⠏": (0x60000, 0x6FFFF),
	"⠿…⠤⠟": (0x70000, 0x7FFFF),
	"⠿…⠤⠗": (0x80000, 0x8FFFF),
	"⠿…⠤⠎": (0x90000, 0x9FFFF),
	"⠿…⠤⠌": (0xA0000, 0xAFFFF),
	"⠿…⠤⠜": (0xB0000, 0xBFFFF),
	"⠿…⠤⠖": (0xC0000, 0xCFFFF),
	"⠿…⠤⠆": (0xD0000, 0xDFFFF),
	"⠿…⠤⠔": (0xE0000, 0xEFFFF),
	"⠿…⠤⠄": (0xF0000, 0xFFFFF),
	"⠿…⠤⠥": (0x100000, 0x10FFFF),
}

HUC8_patterns = {
	'⣥': (0x0000,   0xFFFF),
	'⣭': (0x10000, 0x1FFFF),
	'⣽': (0x20000, 0x2FFFF),
	"⣵⠾": (0x30000, 0x10FFFF),
	"⣵⢾": (0x40000, 0x4FFFF),
	"⣵⢞": (0x50000, 0x5FFFF),
	"⣵⡾": (0x60000, 0x6FFFF),
	"⣵⣾": (0x70000, 0x7FFFF),
	"⣵⣞": (0x80000, 0x8FFFF),
	"⣵⡺": (0x90000, 0x9FFFF),
	"⣵⠺": (0xA0000, 0xAFFFF),
	"⣵⢺": (0xB0000, 0xBFFFF),
	"⣵⣚": (0xC0000, 0xCFFFF),
	"⣵⡚": (0xD0000, 0xDFFFF),
	"⣵⢚": (0xE0000, 0xEFFFF),
	"⣵⠚": (0xF0000, 0xFFFFF),
	"⣵⣡": (0x100000, 0x10FFFF)
}

hexVals = {
	'0': "245", '1': '1', '2': "12", '3': "14",
	'4': "145", '5': "15", '6': "124", '7': "1245",
	'8': "125", '9': "24", 'A': "4",
	'B': "45", 'C': "25", 'D': "2", 'E': '5', 'F': '0'
}

def cellDescToChar(cell):
	if not re.match("^[0-8]+$", cell): return '?'
	toAdd = 0
	for dot in cell: toAdd += 1 << int(dot)-1 if int(dot) > 0 else 0
	return chr(10240+toAdd)

def cellDescriptionsToUnicodeBraille(t):
	return re.sub('([0-8]+)\-?', lambda m: cellDescToChar(m.group(1)), t)

def getPattern(c, HUC6=False):
	ord_ = ord(c)
	patterns = HUC6_patterns if HUC6 else HUC8_patterns
	for pattern in patterns.items():
		if pattern[1][1] >= ord_: return pattern[0]
	return '?'

def HUC8DotsToHUC6Dots(s, debug=False):
	o = []
	s = s.split('-')
	for i, s_ in enumerate(s):
		if i%2:
			o.append(changeDotLevels(s_, True))
		curPos = -1
		for j, c in enumerate(s_):
			curPos = -1
			if c in "78":
				curPos = j
				break
		if curPos == -1: o.insert(curPos, s[i])
		else: o.append(s_[0:j]+'-'+changeDotLevels(s_[j:], True))
	if debug: print(s, o)
	return '-'.join(o)


def changeDotLevels(dots, HUC6=False, debug=False):
	out = ""
	newDots = {
		'0': '0',
		'1': '2' if HUC6 else '3',
		'2': '3' if HUC6 else '7',
		'3': '7' if HUC6 else '1',
		'4': '5' if HUC6 else '6',
		'5': '6' if HUC6 else '8',
		'6': '8' if HUC6 else '4',
		'7': '1' if HUC6 else '2',
		'8': '4' if HUC6 else '5'
	}
	for dot in dots: out += newDots[dot]
	if debug: print(":%s, %s, %s" % (dots, HUC6, out))
	return out


def convertChar(c, HUC6=False):
	out = ""
	pattern = getPattern(c, HUC6)
	ord_ = ord(c)
	hexVal = hex(ord_)[2:][-4:].upper()
	if len(hexVal) < 4: hexVal = ("%4s" % hexVal).replace(' ', '0')
	for i, l in enumerate(hexVal):
		out += changeDotLevels(hexVals[l]) if i%2 else ('-' if i > 0 else '')+hexVals[l] 
	out = '-'.join([''.join(sorted(out_)) for out_ in out.split('-')])
	if HUC6: out = HUC8DotsToHUC6Dots(out)
	out = cellDescriptionsToUnicodeBraille(out)
	if not '…' in pattern: pattern += '…'
	return pattern.replace('…', out)

convert = lambda s, HUC6=False: ''.join([convertChar(c, HUC6) for c in s])

if __name__ == "__main__":
	t = input("Text to convert: ")
	print("HUC8: %s" % convert(t))
	print("HUC6: %s" % convert(t, True))