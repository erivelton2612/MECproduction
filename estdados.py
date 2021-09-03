class Par:
	#INDICES
	J: int 			#DAT - numero de produtos
	M: int 			#DAT - numero de máquinas
	T: int			#DAT - numero de periodos

	itemRec = [] 
	#[item, recurso, tempoProducao, tempoSetup, CustoSetup]
	
	#CUSTOS
	h_j = []		#DAT - custo de estoque dos produtos
	#cs_j = []		#SCO - custo de setup
	cs_jk = []      #SPM - custo setup do produto/maquina 

	#PRODUCAO
	#b_j = []		#DAT - tempo de producao
	s_j = []		#SET - tempo de setup
	b_jk = []		#DAT - tempo de producao do produto/maquina
	s_jk = []		#SET - tempo de setup do produto/maquina
	cap_kt = []		#CAP - capacidade das maquinas por periodo
	K_m = []		#DAT - conjunto de maquinas que processa o produto

	#PRECEDENCIA
	S_j = []		#DAT - conjunto de listas de precedencia de produtos

	#DEMANDA
	d_jt = []		#DEM - conjunto de listas de demandas no periodo

	#ESTOQUE
	stk_j = []		#DEM - estoque inicial

	#bigm
	beta = []

	def del_d(d):
		d.J = None	
		d.M = None	
		d.T = None	
		d.itemRec.clear()
		d.h_j.clear()	
		d.cs_jk.clear()	
		d.b_jk.clear()	
		d.s_jk.clear()	
		d.cap_kt.clear()	
		d.K_m.clear()	
		d.S_j.clear()	
		d.d_jt.clear()	
		#d.stk_j.clear()	

		d.beta.clear()	

class Var:
	#Contínuas
	I_jt = {}		#estoque de j em t #com idade k
	Q_jtk = {}		#qtd produzida de j em t na máquina k
	
	#Binárias
	Y_jtk = {}		#setup pra j em t na máquina k


	def del_v(v):
		v.I_jt.clear()
		v.Q_jtk.clear()
		v.Y_jtk.clear()
