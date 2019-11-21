#!/usr/bin/env python3
import re

HUC6_patterns = {
	"⠿…⠄":  (0x000000, 0x00FFFF),
	"⠿…⠠":  (0x010000, 0x01FFFF),
	"⠿…⠤⠇": (0x020000, 0x02FFFF),
	"⠿…⠤⠍": (0x030000, 0x03FFFF),
	"⠿…⠤⠝": (0x040000, 0x04FFFF),
	"⠿…⠤⠕": (0x050000, 0x05FFFF),
	"⠿…⠤⠏": (0x060000, 0x06FFFF),
	"⠿…⠤⠟": (0x070000, 0x07FFFF),
	"⠿…⠤⠗": (0x080000, 0x08FFFF),
	"⠿…⠤⠎": (0x090000, 0x09FFFF),
	"⠿…⠤⠌": (0x0A0000, 0x0AFFFF),
	"⠿…⠤⠜": (0x0B0000, 0x0BFFFF),
	"⠿…⠤⠖": (0x0C0000, 0x0CFFFF),
	"⠿…⠤⠆": (0x0D0000, 0x0DFFFF),
	"⠿…⠤⠔": (0x0E0000, 0x0EFFFF),
	"⠿…⠤⠄": (0x0F0000, 0x0FFFFF),
	"⠿…⠤⠥": (0x100000, 0x10FFFF),
}

HUC8_patterns = {
	'⣥':  (0x000000, 0x00FFFF),
	'⣭':  (0x010000, 0x01FFFF),
	'⣽':  (0x020000, 0x02FFFF),
	"⣵⠾": (0x030000, 0x03FFFF),
	"⣵⢾": (0x040000, 0x04FFFF),
	"⣵⢞": (0x050000, 0x05FFFF),
	"⣵⡾": (0x060000, 0x06FFFF),
	"⣵⣾": (0x070000, 0x07FFFF),
	"⣵⣞": (0x080000, 0x08FFFF),
	"⣵⡺": (0x090000, 0x09FFFF),
	"⣵⠺": (0x0A0000, 0x0AFFFF),
	"⣵⢺": (0x0B0000, 0x0BFFFF),
	"⣵⣚": (0x0C0000, 0x0CFFFF),
	"⣵⡚": (0x0D0000, 0x0DFFFF),
	"⣵⢚": (0x0E0000, 0x0EFFFF),
	"⣵⠚": (0x0F0000, 0x0FFFFF),
	"⣵⣡": (0x100000, 0x10FFFF)
}

hexVals = {
	'0': "245", '1': '1', '2': "12", '3': "14",
	'4': "145", '5': "15", '6': "124", '7': "1245",
	'8': "125", '9': "24", 'A': "4",
	'B': "45", 'C': "25", 'D': "2", 'E': '5', 'F': '0'
}


def cellDescToChar(cell):
	if not re.match("^[0-8]+$", cell):
		return '?'
	toAdd = 0
	for dot in cell:
		toAdd += 1 << int(dot) - 1 if int(dot) > 0 else 0
	return chr(0x2800 + toAdd)


def cellDescriptionsToUnicodeBraille(t):
	return re.sub(r'([0-8]+)\-?', lambda m: cellDescToChar(m.group(1)), t)


def getPattern(c, HUC6=False):
	ord_ = ord(c)
	patterns = HUC6_patterns if HUC6 else HUC8_patterns
	for pattern in patterns.items():
		if pattern[1][1] >= ord_:
			return pattern[0]
	return '?'


def HUC8DotsToHUC6Dots(s, debug=False):
	o = []
	s = s.split('-')
	for i, s_ in enumerate(s):
		if i % 2:
			o.append(changeDotLevels(s_, True, debug))
		isEven = bool(i % 2)
		curPos = -1
		for j, c in enumerate(s_):
			curPos = -1
			if c in "78":
				curPos = j
				break
		if curPos == -1: o.insert(curPos, s[i])
		else: o.append(s_[0:j] + '-' + changeDotLevels(s_[j:], True, debug))
	if debug: print(":HUC8DotsToHUC6Dots: %s" % s, "->", o)
	return '-'.join(o)


def changeDotLevels(dots, HUC6=False, debug=False):
	out = ""
	newDots = {
		'0': '0',
		'1': '2' if HUC6 else '3',
		'2': '3' if HUC6 else '7',
		'3': '1' if HUC6 else '7',
		'4': '5' if HUC6 else '6',
		'5': '6' if HUC6 else '8',
		'6': '4' if HUC6 else '8',
		'7': '1' if HUC6 else '2',
		'8': '4' if HUC6 else '5'
	}
	for dot in dots:
		out += newDots[dot]
	out = '-'.join([''.join(sorted(out_)) for out_ in out.split('-')])
	if debug: print(":changeDotLevels:", dots, "->", out)
	return out


def convertChar(c, HUC6=False, debug=False):
	out = ""
	pattern = getPattern(c, HUC6)
	ord_ = ord(c)
	hexVal = hex(ord_)[2:][-4:].upper()
	if len(hexVal) < 4: hexVal = ("%4s" % hexVal).replace(' ', '0')
	if debug: print(":convertChar:0:", c, hexVal)
	for i, l in enumerate(hexVal):
		out_ = changeDotLevels(
			hexVals[l], debug=debug) if i % 2 else (
			'-' if i > 0 else '') + hexVals[l]
		out += out_
		if debug: print(":convertChar:1: %s -> %s" % (l, out_))
	if HUC6:
		out = HUC8DotsToHUC6Dots(out, debug=debug)
	out = cellDescriptionsToUnicodeBraille(out)
	if '…' not in pattern:
		pattern += '…'
	out = pattern.replace('…', out)
	if debug: print(":convertChar:3:", out)
	return out


def convert(s, HUC6=False, debug=False): return ''.join([convertChar(c, HUC6, debug) for c in s])


if __name__ == "__main__":
	t = input("Text to convert: ")
	print("HUC8: %s" % convert(t))
	print("HUC6: %s" % convert(t, True))
