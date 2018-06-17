# -*- coding: UTF-8 -*-

import sys
import numpy as np

# tratar B NEGATIVO

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

		b = [0.0]*2
		sinal = []
		za = [0.0]*n
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
				b.append(float(parse[n+1]))
				sinal.append(parse[n])


		contArtf = 0
		faseUm = False
		for i in xrange(m):
			criou = False
			if(sinal[i] == "<="):
				r[i].append(1.0)
				criou = True
			elif(sinal[i] == ">="):
				r[i].append(-1.0)
				contArtf += 1
				criou = True
			else:
				contArtf+=1

			if(criou):
				za.append(0.0)
				z.append(0.0)
				for i2 in xrange(m):
					if(i2 != i):
						r[i2].append(0.0)

		for i in xrange(m):
			if(sinal[i] == ">=" or sinal[i] == "="):
				r[i].append(1.0)
				z.append(0.0)
				za.append(-1.0)
				if(contArtf > 0):
					faseUm = True
					for i2 in xrange(m):
						if(i2 != i):
							r[i2].append(0.0)
				contArtf-=1
	
		tableau = []
		
		if faseUm:
			for i in xrange(m+2):
				tableau.append([])
				tableau[i].append(b[i])

			for i in xrange(len(za)):
				tableau[0].append(za[i])
				tableau[1].append(z[i])

			for i in xrange(m):
				tableau[i+2] += (r[i])
		else:
			b = b[1:]
			for i in xrange(m+1):
				tableau.append([])
				tableau[i].append(b[i])
			for i in xrange(len(z)):
				tableau[0].append(z[i])

			for i in xrange(m):
				tableau[i+1] += (r[i])

		print "Tableau inicial:"
		print np.matrix(tableau)
		print ""

		return tableau, m, n, faseUm

def verificaZ(tableau):
	for i in xrange(1, len(tableau)):
		if(tableau[i] > 0):
			return False
	return True

def verificaBase(tableau, j, m):
	cont0=0
	cont1=0
	bi = -1
	for i in xrange(m+1):
		if(tableau[i][j] == 0):
			cont0+=1
		elif(tableau[i][j] == 1):
			cont1+=1
			bi = i
	return (cont1+cont0 == m+1), bi if (cont1==1) else -1

def simplex(tableau, m, n):
	qtdFolga = len(tableau[0])-n-1
	nQuadro = 1
	while not verificaZ(tableau[0]):
		print "Quadro " + str(nQuadro) + " - 2ª fase:"
		print np.matrix(tableau)
		print ""
		nQuadro += 1

		pivoj = np.argmax(tableau[0][1:])
		pivoj+=1

		if(tableau[0][pivoj] <= 0):
			print "conjunto de solucoes viaveis vazio"
			return

		divisoes = np.full(m, float("Inf"))

		for i in xrange(1, m+1):
			if(tableau[i][pivoj] > 0):
				divisoes[i-1] = tableau[i][0]/tableau[i][pivoj]

		pivoi = np.argmin(divisoes)

		if np.count_nonzero(divisoes == float("Inf")) == len(divisoes):
			print "conjunto de solucoes viaveis vazio"
			print "z -> infinito"
			return

		for i in xrange(len(tableau[0])):
			tableau[pivoi+1] = [x/tableau[pivoi+1][pivoj] for x in tableau[pivoi+1]]

		for i in xrange(m+1):
			if i!=(pivoi+1):
				tableau[i] = np.subtract(tableau[i], [tableau[i][pivoj]*x for x in tableau[pivoi+1]])

	print "Quadro final da 2ª fase:"
	print np.matrix(tableau)
	print ""

	degenerada = False
	for i in xrange(1, m+1): #testar
		if(tableau[i][0] == 0):
			degenerada = True
	x = []


	if degenerada:
		print "Solução degenerada"
	if (np.count_nonzero(tableau[0] == 0) > m):
		print "Solução multipla"
		print "z*= ", "%0.3f" % tableau[0][0]
		print "x*= (", 
		for j in xrange(1, len(tableau[0])):
			verif, i = verificaBase(tableau, j, m)
			if(verif):
				print "%0.3f" % tableau[i][0], " " if j == len(tableau[0]) -1 else ", ",
			else:
				print 0.0, " " if j == len(tableau[0]) -1 else ", ",
		print ")"
	else:
		print "Solução única"
		print "z*= ", "%0.3f" % tableau[0][0]
		print "x*= (", 
		for j in xrange(1, len(tableau[0])):
			if(tableau[0][j] == 0):
				for i in xrange(1, m+1):
					if(tableau[i][j] == 1):
						print "%0.3f" % tableau[i][0], " " if j == len(tableau[0]) -1 else ", ",
			else:
				print 0.0, " " if j == len(tableau[0]) -1 else ", ",
		print ")"


def verificaZa(tableau, cont):
	for i in xrange(cont):
		if(tableau[len(tableau)-1-i] != -1):
			return False
	return True

def ajustaMatriz(tableau, m, contArtf):
	tableau = tableau[1:]
	for i in xrange(m+1):
		tableau[i] = tableau[i][:-contArtf]
	return tableau

def simplexDuasFases(tableau, m, n):
	contArtf = tableau[0].count(-1)

	aux = 0
	for i in xrange(m+1, 1, -1):
		if (tableau[i][-1-aux] == 1):
			tableau[0] = np.add(tableau[0], tableau[i])
			aux+=1
		if(aux>= contArtf):
			break

	nQuadro = 1
	while not verificaZa(tableau[0], contArtf):
		print "Quadro " + str(nQuadro) + " - 1ª fase:"
		print np.matrix(tableau)
		print ""
		nQuadro += 1

		pivoj = np.argmax(tableau[0][1:])
		pivoj+=1

		if(tableau[0][pivoj] <= 0):
			print "conjunto de solucoes viaveis vazio"
			return

		divisoes = np.full(m, float("Inf"))

		for i in xrange(2, m+2):
			if(tableau[i][pivoj] > 0):
				divisoes[i-2] = tableau[i][0]/tableau[i][pivoj]

		pivoi = np.argmin(divisoes)

		if np.count_nonzero(divisoes == float("Inf")) == len(divisoes):
			print "conjunto de solucoes viaveis vazio"
			print "z -> infinito"
			return

		for i in xrange(len(tableau[0])):
			tableau[pivoi+2] = [float(x/tableau[pivoi+2][pivoj]) for x in tableau[pivoi+2]]

		for i in xrange(m+2):
			if i!=(pivoi+2):
				tableau[i] = np.subtract(tableau[i], [tableau[i][pivoj]*x for x in tableau[pivoi+2]])

	print "Quadro final da 1ª fase:"
	tableau = ajustaMatriz(tableau, m, contArtf)
	print np.matrix(tableau)
	print ""
	simplex(tableau, m, n)


def main(args):
	np.set_printoptions(precision=3)

	tableau, m, n, faseUm = geraTableauInicial(args)
	if faseUm:
		simplexDuasFases(tableau, m, n)
	else:
		simplex(tableau, m, n)

if __name__ == '__main__':
	main(sys.argv)