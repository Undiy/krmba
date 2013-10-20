#!c:/Python27/python.exe -u
# -*- coding: utf-8 -*-
import os
import sys
from xml.dom.minidom import *
from decimal import Decimal, ROUND_DOWN

TDL_FILE = len(sys.argv) == 2 and sys.argv[1] or "C:\Dropbox\My Projects.tdl"
CATEGORY_PRICE = dict()

node_text = lambda node: node.childNodes[0].nodeValue
def attend():
	_ = raw_input("\n\nPress any key to finish it.")

def main_func():
	with open(
		os.path.join("C:\Program files\krmba", "categories.conf"),	"r") as cat_conf:
		CATEGORY_PRICE = dict(
			reduce(lambda x, y: x + [y],
				   map(lambda x: x.rstrip('\n').split(":"),
						 cat_conf.readlines()),
				   []))

	xml = parse(TDL_FILE)
	result_price = Decimal(0)

	for task in xml.getElementsByTagName("TASK"):
		cost = task.getAttributeNode("COST")
		category_list = task.getElementsByTagName("CATEGORY")
		if not len(category_list) or cost is None:
			continue
		category = node_text(category_list[0])
		try:
			price = CATEGORY_PRICE[category]
		except KeyError:
			print(
			"There is no such category: %s in the config file" % category)
			attend()

		result_price += Decimal(cost.value) * Decimal(price)
		
	print result_price.quantize(
		Decimal('.01'),
		rounding=ROUND_DOWN)
try:
	main_func()
except Exception,e:
	print(e)
attend()