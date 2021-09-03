import gurobipy as grb
import time, itertools
import leitura as rd
import estdados
import modelo as mod
import numpy as np

# G1 = ["2","4","6"]
# L1 = ["A","G"]
# L2 = ["A","C"]
# N1 = ["1","2","3"]
# N2 = ["1","2"]
# N3 = ["1","2","3","4","5"]
# N4 = ["1","2"]

# G1 = ["2"]      # padrao
#G1 = ["4"]      #2496 itens
# G1 = ["6"]      #365 itens demanda 5
G1 = ["8"]      #365 itens demanda 1
L1 = ["A"]

L2 = ["A"]
N1 = ["1"]
N2 = ["1"]
N3 = ["1"]
N4 = ["1"]

comb = list(itertools.product(G1,L1,L2,N1,N2,N3,N4))
for inst in comb:
	dirc = "./data/class"+inst[0]+"/"
	dat = inst[0]+inst[1]+inst[2]+".dat"
	dem = inst[0]+inst[1]+"_"+inst[3]+".dem"
	sco = inst[0]+inst[1]+"_"+inst[3]+inst[4]+".sco"
	setup = inst[0]+"_____"+inst[6]+".set"
	cap = inst[0]+inst[1]+inst[2]+inst[3]+"_"+inst[5]+inst[6]+".cap"
	instance = inst[0]+inst[1]+inst[2]+inst[3]+inst[4]+inst[5]+inst[6]
	cmd = [instance,dirc,dat,dem,sco,setup,cap]

	time_limit = 3600
	d = estdados.Par()
	v = estdados.Var()
	rd.leitura(cmd, d)
	
# 	print("d.S_j")
# 	print(*d.S_j, sep = "\n")
# 	print(a, sep = "\n")
# 	a = np.array(d.S_j)
# 	b = np.where(a)[1]
# 	a = np.sum(a[:,1],0)
# 	print("d.d_jt", a)

# 	print(*d.beta, sep = "\n")
# 	print(*d.itemRec, sep = "\n")
# 	for i in range(len(d.itemRec)):
# 		if(d.itemRec[i][0] ==1 and d.itemRec[i][1]==1):
# 			print(d.itemRec[i][2]) 
# 	
# 	print("Comprimento d.d_jt: " + str(len(d.d_jt)))


	model = grb.Model("lot sizing")
	mod.variables(model,d,v)
	mod.cost_function(model,d,v)
	mod.constraints(model, d, v)
	model.setParam('TimeLimit', time_limit)
	model.optimize()

# 	print(*v.b_jk, sep = ", ")

	mod.printsolution(cmd,model,d,v)
	estdados.Var.del_v(v)
	estdados.Par.del_d(d)
