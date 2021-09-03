declare @recursoPadrao int = (select MAX(t0.IDRecurso) + 1 from nroRecursos t0)

SELECT T1.IDRecurso, T0.IDItem,
    CAST(left(ABS(checksum(newid())), 5) % 15000 AS numeric(18,2))/1000 'setup costs'

FROM nroItens T0, nroRecursos T1

UNION ALL

SELECT @recursoPadrao, T0.IDItem,
    CAST(left(ABS(checksum(newid())), 5) % 15000 AS numeric(18,2))/1000 'setup costs'

FROM nroItens T0, nroRecursos T1
WHERE T1.IDRecurso = 1