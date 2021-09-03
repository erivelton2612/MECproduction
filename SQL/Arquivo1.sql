use [DataWarehouse]



declare @periodos int = (
select max(t2.Qt_Dias_Uteis_Mes) from DataWarehouse.dbo.Dia_Util t2 
where month(t2.Dt_Referencia) = 6  and YEAR(t2.Dt_Referencia) = 2021 
)

declare @recursoPadrao int = (select MAX(t0.IDRecurso) + 1 from nroRecursos t0)


--select distinct * from dbo.ItemMaquinasEstrutura t0
--where CODIGO is not null and t0.Tipo=290


select count(*) --'#itens'
from dbo.nroitens t0

union all

select count(*) --'#recursos'
from dbo.nroRecursos t0

union all

select @periodos --'#periodos'--8 horas por dia 22 dias por semana




--#3.1 #de linhas a ler a seguir
--#4  items
--#5  number of ressource that produces the item
--#6  production time per unit
--#7	tempo de setup do produto na maquina

--select Iditem '--Iditem',
--	isnull((select top 1 a0.ID from OPEstruturaId a0 where a0.Pai = t0.IDItem and a0.tipo = 290),0) as 'number of ressource that produces the item',
--	'1' 'holding costs', 
--	isnull((select sum(a0.QTD) from OPEstruturaId a0 where a0.Pai = t0.IDItem and a0.tipo = 290),1) as 'production time per unit'
--	--into ##tmp
--from dbo.nroItens t0

select count(*)
from dbo.nroItens t0 left join OPEstruturaId t1 on t0.IDItem=t1.Pai and t1.tipo = 290

select t0.IDItem, isnull(t1.ID,@recursoPadrao) 'Recurso', isnull(t1.qtd,1) 'qtd','0.1' 'tempo de setup','1' 'custo de setup'
from dbo.nroItens t0 left join OPEstruturaId t1 on t0.IDItem=t1.Pai and t1.tipo = 290


--select count(*)
--from OPEstruturaId 
--where tipo = 290

--select pai, id, qtd, '1' 'production time per unit','0.1' 'tempo de setup do produto na maquina',*
--from OPEstruturaId 
--where tipo = 290

--IF (EXISTS (SELECT * FROM OPEstruturaId ))
--BEGIN
--   drop table OPEstruturaId
--END

select count(*) from OPEstruturaId t0 where t0.tipo = 4

--#7  number of ressource that produces the item
--#8  product ID component
--#9  product ID parent
--#10 units of component needed to produce one unit of parent
--#11 lead time

select t0.id'--id', t0.pai, replace(t0.qtd,',','.') qtd, '1' 'Lead-time' from OPEstruturaId t0
where t0.id is not null
order by t0.id