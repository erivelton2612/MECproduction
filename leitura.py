#import numpy as np

def leitura(argv, d):

	#DAT------------------------------------------------------------
	arqv = open (str(argv[1]+argv[2]))
	#1  # of items
	#2  # of resources
	#3  # of periods
	d.J = int(arqv.readline())
	d.M = int(arqv.readline())
	d.T = int(arqv.readline())
	    
    #3.1 #de linhas a ler a seguir
	lines = int(arqv.readline())
	#4  items
	#5  number of ressource that produces the item
	#6  production time per unit
	#7	tempo de setup do produto na maquina
	for i in range(lines):
		e = arqv.readline().split()
		d.itemRec.append([int(e[0]),int(e[1]),float(e[2]),float(e[3]),float(e[4])])


	#8  product ID component
	#9  product ID parent
	#10 units of component needed to produce one unit of parent
	#11 lead time
	lines = int(arqv.readline())
	for i in range(lines):
		e = arqv.readline().split()
		d.S_j.append([int(e[0]) , int(e[1]) , float(e[2])] )
		
	#print(*d.S_j, sep = ", ")

	arqv.close()
# 	#DEM------------------------------------------------------------
	arqv = open (str(argv[1]+'dem/'+argv[3]))
	
	#qtd demandas
	#[periodo, item, demanda]
	lines = int(arqv.readline())
	
	for l in range(lines):
		e = arqv.readline().split()
		d.d_jt.append([int(e[0]), int(e[1]), float(e[2])])
		
	for i in range(d.J):
		e = arqv.readline().split()
		d.stk_j.append(int(e[1]))


	arqv.close()


# 	#CAP------------------------------------------------------------
	arqv = open (str(argv[1]+'cap/'+argv[6]))
	for i in range(d.M):
		d.cap_kt.append([])
		e = arqv.readline().split()
		for t in range(d.T):
 			d.cap_kt[i].append(int(e[t+1]))

	arqv.close()


# 	#calc BIGM

	for j in range(d.J):
		d.beta.append([])
		for t in range(d.T):
			d.beta[j].append(0)
			for k in range(t,d.T):
				d.beta[j][t] = 0
				for x in range(len(d.d_jt)):
				   if (d.d_jt[x][0] == k+1 and d.d_jt[x][1])==j+1:
					   d.beta[j][t] += float(d.d_jt[x][2])
					   break

			
	for j in range(d.J):
		for t in range(d.T):
 			for i in range(d.J):
				 for x in range(len(d.S_j)):
					 if(d.S_j[x][1] == j+1 and d.S_j[x][0]== i+1):
						  d.beta[j][t] += d.S_j[x][2]*d.beta[i][t]
						  break
# O custo do estoque será zero inicialmente[
	
		d.h_j= [1] * d.J