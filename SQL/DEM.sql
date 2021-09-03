--select t0.itemcode,month(t0.DueDate) , YEAR(t0.DueDate),COUNT(t0.PlannedQty)
--from owor t0
--where OriginNum < 9000000 and YEAR(t0.DueDate)=2021
--group by t0.itemcode,  month(t0.DueDate) , YEAR(t0.DueDate)
--order by 4 desc


--select t0.itemcode,month(t0.DueDate) , YEAR(t0.DueDate),COUNT(t0.PlannedQty)
--from owor t0
--where OriginNum < 9000000 and YEAR(t0.DueDate)=2021

select count(*)
from OWOR t0
where ItemCode = '69168'  and YEAR(t0.DueDate)=2021 and  month(t0.DueDate)=6


select t2.IDItem, Qt_Dias_Uteis_Mes,sum(t0.PlannedQty) 'Qtd'
from OWOR t0 inner join DataWarehouse.dbo.Dia_Util t1 on t0.DueDate = t1.Dt_Referencia
	inner join DataWarehouse.dbo.nroItens t2 on t0.itemcode=t2.codigo
where ItemCode = '69168'  and YEAR(t0.DueDate)=2021 and  month(t0.DueDate)=6
group by ItemCode, --DueDate,
	Qt_Dias_Uteis_Mes , t2.IDItem


select IDItem, '0','0'
from DataWarehouse.dbo.nroItens