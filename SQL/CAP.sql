
declare @recursoPadrao int = (select MAX(t0.IDRecurso) + 1 from nroRecursos t0)

select IDRecurso, 8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8
from nroRecursos

union all

select @recursoPadrao, 99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999,99999
--select t2.Qt_Dias_Uteis_Mes 
--from DataWarehouse.dbo.Dia_Util t2 
--where month(t2.Dt_Referencia) = 6  and YEAR(t2.Dt_Referencia) = 2021 and t2.Fl_Dia_Util = 1