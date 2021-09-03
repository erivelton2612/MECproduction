
	
			--estrutura de produtos

			WITH MENULEVEL(CODIGO, NIVEL, PAI, QTD,QTDpadrao,Tipo)
			AS 
			(
				SELECT T0.[ITEMCODE] AS CODIGO, 
				1 AS NIVEL, 
					T0.[ITEMCODE] AS PAI, 
					CAST('1' AS FLOAT) AS QTD, t0.onhand as QTDpadrao, 
					4 as Tipo
				FROM sbo_casale_prd.dbo.OITM T0
				--WHERE T0.[ITEMCODE]='[%0]'
				WHERE T0.[ITEMCODE] in (select t0.ItemCode
									from sbo_casale_prd.dbo.OWOR t0 inner join sbo_casale_prd.dbo.oitm t1 on t0.itemcode = t1.itemcode
									where t0.DueDate between '20210601' and '20210630'
										and t0.OriginNum < 9000000
										and t1.mattype = 4
										)
				--where T0.[ITEMCODE] = '71827'

				UNION ALL

				SELECT T1.[Code], (
					c.nivel + 1) as nivel, 
					T1.[Father] as pai, 
					CAST(T1.[Quantity] AS FLOAT)*c.qtd as qtd, 
					t1.[Quantity] as QTDpadrao, T1.Type
				FROM sbo_casale_prd.dbo.ITT1 T1 INNER JOIN MENULEVEL C ON T1.[father] = C.CODIGO
			)

--use [DataWarehouse]
			select distinct  *
			into ItemMaquinasEstrutura 
			from MENULEVEL t0



		select t0.codigo , ROW_NUMBER() OVER(ORDER BY t0.codigo ASC) AS IDItem
		into nroItens
		from (select distinct t0.codigo 
				from dbo.ItemMaquinasEstrutura t0
				where tipo = 4) as t0


		select t0.codigo , ROW_NUMBER() OVER(ORDER BY t0.codigo ASC) AS IDRecurso
		into nroRecursos
		from (select distinct t0.codigo 
				from dbo.ItemMaquinasEstrutura t0
				where tipo = 290) as t0


		select case when Tipo = 4 then t1.IDItem else t2.idrecurso end ID,t3.IDItem as Pai, t0.QTD,Tipo
		into OPEstruturaId
		from ItemMaquinasEstrutura t0 
			left join nroItens t1 on t0.CODIGO=t1.CODIGO and Tipo = 4
			left join nroRecursos t2 on t0.CODIGO=t2.CODIGO	 and Tipo = 290
			left join nroItens t3 on t0.PAI = t3.CODIGO
