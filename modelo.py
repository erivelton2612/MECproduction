from gurobipy import *
import estdados

#-------------Criação de Variáveis

def variables(model,d,v):
	#estoque
	v.I_jt = model.addVars(d.J,d.T+1,vtype=GRB.CONTINUOUS,lb=0.0)		
	#producao
	v.Q_jtk = model.addVars(d.J,d.T,d.M,vtype=GRB.CONTINUOUS,lb=0.0)		
	#setup
	v.Y_jtk = model.addVars(d.J,d.T, d.M,vtype=GRB.BINARY,lb=0.0)	
	model.update()

#-------------Criação da FO

def cost_function(model,d,v):
	
	inventory = sum(v.I_jt[j,t+1] *d.h_j[j] 
                 for j in range(d.J) for t in range(d.T))
	
	setup=0
	for j in range(d.J): 
		for t in range(d.T): 
			for k in range(d.M):
				for i in range(len(d.itemRec)):
					if(d.itemRec[i][0] ==j+1 and d.itemRec[i][1]==k+1):
						setup += v.Y_jtk[j,t,k] * d.itemRec[i][4] *100
						break
	
# 	setup = sum(v.Y_jtk[j,t,k]*
# 			 
# 			 for i in range(len(d.itemRec)):
# 				 if(d.itemRec[i][0] ==j+1 and d.itemRec[i][1]==k+1):
# 				 d.itemRec[i][4]
# 				  *100 
#                   for j in range(d.J) 
#                   for t in range(d.T) 
#                   for k in range(d.M)
#                  )
	total = inventory + setup
	model.setObjective(total, GRB.MINIMIZE)
	model.update()

#-------------Criação de Restrições

def constraints(model, d, v):
	#INDICES DO ESTOQUE JOGADOS 1 PRA FRENTE
		#0 = ESTOQUE NO FINAL DE 0 USADO EM 1
		#1 = ESTOQUE NO FINAL DE 1
		#d.T = ESTOQUE NO FINAL DE TUDO QUE VAI SER ZERO

	#Estoque inicial produto
	for j in range(d.J):
		model.addConstr(v.I_jt[j,0] == d.stk_j[j])	

	#Fluxo de estoque produto
	for j in range(d.J):
		for t in range(d.T):
			rhs = v.I_jt[j,t+1]
			for x in range(len(d.d_jt)):
				if(d.d_jt[x][0] == t+1 and d.d_jt[x][1] == j+1):
					rhs += d.d_jt[x][2]
					break
			lhs = v.I_jt[j,t]
			for k in range(d.M):
				lhs += v.Q_jtk[j,t,k] 
				for i in range(d.J):
					for x in range(len(d.S_j)):
						if(d.S_j[x][0] == j+1 and d.S_j[x][1] == i+1):
							rhs += d.S_j[x][2] *v.Q_jtk[i,t,k]
							break

			model.addConstr(lhs == rhs)
	#Capacidade
	for k in range(d.M):
		for t in range(d.T):
			usage = 0
			for j in range(d.J):
				for i in range(len(d.itemRec)): 
					if(d.itemRec[i][0] ==j+1 and d.itemRec[i][1]==k+1):
						usage += d.itemRec[i][2] * v.Q_jtk[j,t,k] + d.itemRec[i][3]
						break
			model.addConstr(usage <= d.cap_kt[k][t])
	#Setup
	for j in range(d.J):
		for t in range(d.T):
			for k in range(d.M):
				model.addConstr(v.Q_jtk[j,t,k] <= d.beta[j][t]*v.Y_jtk[j,t,k])

	model.update()

def printsolution(argv,model,d,v):
	
	
	solt = open(str(argv[0])+".txt","w") 

	solt.write("Solucao\tGap\tTempo\tStatus Gurobi\n")
	solt.write(str(round(model.objVAl))+"\t"+str(round(100*model.MIPGap,2))+"\t")
	solt.write(str(round(model.Runtime,2))+"\t"+str(model.Status)+"\n")


	inv_prod = sum(v.I_jt[j,t+1].X#*d.h_j[j] 
				for j in range(d.J) for t in range(d.T))
	setup = sum(v.Y_jtk[j,t,k].X#*d.cs_jk[j,k]
			 *100 for j in range(d.J) for t in range(d.T) for k in range(d.M))

	solt.write("Custos\nEstoque\tSetup\n")
	solt.write(str(round(inv_prod))+"\t"+str(round(setup))+"\n")

	solt.write("J\tT\tM\n")
	solt.write(str(d.J)+"\t"+str(d.T)+"\t"+str(d.M)+"\n\n")
	
	solt.write("Ocupacao de Maquinas Por Periodo\n")
	
	for k in range(d.M):
		for t in range(d.T):
			a = 0
			for j in range(d.J):
				for x in range(len(d.itemRec)):#otimizar para sair depois q encontrar
					if (d.itemRec[x][0] == j+1 and d.itemRec[x][1] == k+1):
						a += d.itemRec[x][2]*v.Q_jtk[j,t,k].X + d.itemRec[x][3]*v.Y_jtk[j,t,k].X
						break
						
						
			a = a/d.cap_kt[k][t]
			solt.write(str(round(100*a,2))+"\t")
		solt.write("\n")
	solt.write("\n")

	solt.write("Custos Estoque Por Periodo\n")
	for t in range(d.T):
		a = sum(v.I_jt[j,t+1].X#*d.h_j[j] 
		  for j in range(d.J))
		solt.write(str(round(a))+"\t")
	solt.write("\n\n")
	

	solt.write("Item\tT\tMaq\tProd\tInv\tDem E\tDem I\n")
	for j in range(d.J):
		for t in range(d.T):
			for k in range(d.M):
				a = sum(d.S_j[x][2]*v.Q_jtk[i,t,k].X 
					for i in range(d.J)
					for x in range(len(d.S_j)) 
					if type(d.S_j[x][2]) == float and d.S_j[x][0]==j and d.S_j[x][1]==i) 
				solt.write(str(j+1)+"\t"+str(t+1)+"\t"+str(k+1)+"\t"+str(round(v.Q_jtk[j,t,k].X))+"\t"+
					   str(round(v.I_jt[j,t+1].X))+"\t"+
                  str(round(
					  sum(d.d_jt[x][2] for x in range(len(d.d_jt)) 
						 if(d.d_jt[x][0] == t+1 and d.d_jt[x][1] == j+1))
					  ))+"\t"+str((a))+"\n")
# 				solt.write("\n")

	solt.close()

