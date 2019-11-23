#!/usr/bin/env python3
import re

HUC6_patterns = {
	"⠿…":  (0x000000, 0x00FFFF),
	"⠿…":  (0x010000, 0x01FFFF),
	"⠿…⠇": (0x020000, 0x02FFFF),
	"⠿…⠍": (0x030000, 0x03FFFF),
	"⠿…⠝": (0x040000, 0x04FFFF),
	"⠿…⠕": (0x050000, 0x05FFFF),
	"⠿…⠏": (0x060000, 0x06FFFF),
	"⠿…⠟": (0x070000, 0x07FFFF),
	"⠿…⠗": (0x080000, 0x08FFFF),
	"⠿…⠎": (0x090000, 0x09FFFF),
	"⠿…⠌": (0x0A0000, 0x0AFFFF),
	"⠿…⠜": (0x0B0000, 0x0BFFFF),
	"⠿…⠖": (0x0C0000, 0x0CFFFF),
	"⠿…⠆": (0x0D0000, 0x0DFFFF),
	"⠿…⠔": (0x0E0000, 0x0EFFFF),
	"⠿…⠄": (0x0F0000, 0x0FFFFF),
	"⠿…⠥": (0x100000, 0x10FFFF),
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

hexVals = [
	"245", '1', "12", "14",
	"145", "15", "124", "1245",
	"125", "24", "4", "45",
	"25", "2", '5', '0'
]

print_ = print

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
		if pattern[1][1] >= ord_: return pattern[0]
	return '?'

def convertHUC6(dots, debug=False):
	ref1 = "1237"
	ref2 = "4568"
	data = dots.split('-')
	offset = 0
	linedCells1 = []
	linedCells2 = []
	for cell in data:
		for dot in "12345678":
			if dot not in cell:
				if dot in ref1: linedCells1.append("0")
				if dot in ref2: linedCells2.append("0")
			else:
				dotTemp = "0"
				if dot in ref1:
					dotIndexTemp = (ref1.index(dot) + offset) % 3
					dotTemp = ref1[dotIndexTemp]
					linedCells1.append(dotTemp)
				elif dot in ref2:
					dotIndexTemp = (ref2.index(dot) + offset) % 3
					dotTemp = ref2[dotIndexTemp]
					linedCells2.append(dotTemp)
		offset = (offset + 1) % 3
	result = ""
	i = 0
	for l1, l2 in zip(linedCells1, linedCells2):
		if i % 3 == 0 and i != 0: result += "-"
		cellTemp = (l1 if l1 != '0' else '') + (l2 if l2 != '0' else '')
		result += cellTemp
		i += 1
	while "--" in result: result = result.replace("--", "-0-")
	if result.startswith('-'): result = '0'+result
	if result.endswith('-'): result += '0'
	return result

def convertHUC8(dots, debug=False):
	out = ""
	newDots = "037768825"
	for dot in dots: out += newDots[int(dot)]
	out = '-'.join([''.join(sorted(out_)) for out_ in out.split('-')])
	if debug: print_(":convertHUC8:", dots, "->", out)
	return out


def convert(t, HUC6=False, debug=False):
	out = ""
	for c in t:
		pattern = getPattern(c, HUC6)
		ord_ = ord(c)
		hexVal = hex(ord_)[2:][-4:].upper()
		if len(hexVal) < 4: hexVal = ("%4s" % hexVal).replace(' ', '0')
		if debug: print_(":hexVal:", c, hexVal)
		out_ = ""
		for i, l in enumerate(hexVal):
			j = int(l, 16)
			out_ += convertHUC8(hexVals[j], debug) if i % 2 else ('-' if i > 0 else '') + hexVals[j]
		if debug: print_(":convertChar: %s -> %s" % (hexVal, out_))
		if HUC6:
			out_ = convertHUC6(out_, debug)
			if ord_ <= 0x00FFFF: out_ += '3'
			elif ord_ <= 0x01FFFF: out_ += '6'
			else: out_ += "36"
		out_ = cellDescriptionsToUnicodeBraille(out_)
		if '…' not in pattern: pattern += '…'
		out_ = pattern.replace('…', out_)
		out += out_
	return out


if __name__ == "__main__":
	t = input("Text to convert: ")
	print_("HUC8: %s" % convert(t))
	print("HUC6: %s" % convert(t, True))
