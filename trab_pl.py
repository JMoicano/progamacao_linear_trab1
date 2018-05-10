# -*- coding: UTF-8 -*-

import sys

def main(args):
	with open(args[1], "r+") as file:
		limite = file.readline().strip()


		m, n = file.readline().strip().split(" ")
		m = int(m) # restricoes
		n = int(n) # variaveis

		parse = file.readline().strip().split(" ")
		if limite == "max" :
			z = [-1*int(x) for x in parse]
		else:
			z = [int(x) for x in parse]
			
		r = []
		for i in xrange(m):
			parse = file.readline().strip().split(" ")
			r.append(parse)

		print limite
		print m, n
		print z
		print r

if __name__ == '__main__':
	main(sys.argv)
