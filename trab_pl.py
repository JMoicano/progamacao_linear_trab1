# -*- coding: UTF-8 -*-

import sys
import numpy as np 

def geraTableauInicial(args):
	with open(args[1], "r+") as file:
		limite = file.readline().strip()

		m, n = file.readline().strip().split(" ")
		m = int(m) # restricoes
		n = int(n) # variaveis

		parse = file.readline().strip().split(" ")
		if limite == "min" :
			z = [-1*float(x) for x in parse]
		else:
			z = [float(x) for x in parse]
			
		r = []
		for i in xrange(m):
			r.append([])

		b = [0]*2
		sinal = []
		za = [0]*n
		for i in xrange(m):
			parse = file.readline().strip().split(" ")
			for j in xrange(n):
				r[i].append(float(parse[j]))

			if(parse[n+1] < 0):
				b.append(-1*float(parse[n+1]))
				r[i] = [-1*x for x in r[i]]
				if(parse[n] == "<="):
					sinal.append(">=")
				elif(parse[n] == ">="):
					sinal.append("<=")
				else:
					sinal.append(parse[n])
			else:
				b.append(float(float(parse[n+1])))
				sinal.append(parse[n])


		contArtf = 0
		for i in xrange(m):
			criou = False
			if(sinal[i] == "<="):
				r[i].append(1.0)
				criou = True
			elif(sinal[i] == ">="):
				r[i].append(-1.0)
				contArtf += 1
				criou = True
			if(criou):
				za.append(0.0)
				z.append(0.0)
				for i2 in xrange(m):
					if(i2 != i):
						r[i2].append(0.0)

		for i in xrange(m):
			if(sinal[i] == ">="):
				r[i].append(1.0)
				z.append(0.0)
				za.append(-1.0)
				if(contArtf > 0):
					for i2 in xrange(m):
						if(i2 != i):
							r[i2].append(0.0)
				contArtf-=1
	
		tableau = []
		for i in xrange(m+2):
			tableau.append([])
			tableau[i].append(b[i])

		for i in xrange(len(za)):
			tableau[0].append(za[i])
			tableau[1].append(z[i])

		for i in xrange(m):
			tableau[i+2] += (r[i])

		print "Tableau inicial:"
		print np.matrix(tableau)
		print ""

		return tableau, m, n

def verificaZa(tableau, cont):
	for i in xrange(cont):
		if(tableau[len(tableau)-1-i] != -1):
			return False
	return True

def verificaZ(tableau):
	for i in xrange(len(tableau)):
		if(tableau[i] > 0):
			return False
	return True

def simplexDuasFases(args):
	tableau, m, n = geraTableauInicial(args)
	contArtf = tableau[0].count(-1)

	for i in xrange(contArtf):
		tableau[0] = np.add(tableau[0], tableau[m+1-i])

	while not verificaZa(tableau[0], contArtf):
		print np.matrix(tableau)
		print ""

		pivoj, = np.unravel_index(tableau[0].argmax(), tableau[0].shape)

		divisoes = np.full(m, float("Inf"))

		for i in xrange(2, m+2):
			if(tableau[i][pivoj] > 0):
				divisoes[i-2] = tableau[i][0]/tableau[i][pivoj]

		pivoi, = np.unravel_index(divisoes.argmin(), divisoes.shape)

		if np.count_nonzero(divisoes == float("Inf")) == len(divisoes):
			print "break", pivoi+2, pivoj
			break

		for i in xrange(len(tableau[0])):
			tableau[pivoi+2] = [x/tableau[pivoi+2][pivoj] for x in tableau[pivoi+2]]

		for i in xrange(m+2):
			if i!=pivoi+2:
				tableau[i] = np.subtract(tableau[i], [tableau[i][pivoj]*x for x in tableau[pivoi+2]])

	print np.matrix(tableau)



def main(args):
	np.set_printoptions(precision=4)
	simplexDuasFases(args)

if __name__ == '__main__':
	main(sys.argv)