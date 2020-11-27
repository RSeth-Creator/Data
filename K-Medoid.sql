--K- Medoid Algorithm 

 declare @p1i float =4,
		 @p1j float= 2.8,
		 @p2i float=1.5 ,
		 @p2j float=2
--create the data set / you can import from direct some sample data 
declare @k_medoid table (id int identity(1,1), p1 float,p2 float)
insert into @k_medoid values (1,2),(1.1,2.3),(1.5,3.5),(1.9,2.8),(2.1,3.1),(2,3.5),(4,2),(4.1,2.3),(4.5,3.5),(4.9,2.8),(3.1,3.1),(3,3.5)
--find the max - min pair from the data set 

--find out the max and min distance from the input centroid location		 
;with abs_d as(
				select p1,p2,
						@p1i cluster1_Xc,@p1j Cluster1_Yc,
						round(abs(p1-@p1i),3) D_X1 ,
						round(abs(p2-@p1j),3) D_Y1,
						 @p2i Cluster2_Xc, @p2j Cluster2_Yc,
						round(abs(p1-@p2i),3) D_X2 ,
						round(abs(p2-@p2j),3) D_Y2 
						from @k_medoid
						)

--select * from abs_d

--Find the mahattan distance  for each pointto centroid 
,manhattan as (
select p1,p2,@p1i as P1_X,@p1j as P1_Y,@p2i as P2_X,@p2j as P2_Y,ABS(D_X1+D_Y1) Man_Dis_P1,ABS(D_X2+D_Y2) Man_Dis_P2   from abs_d
)
--select * from manhattan

--formation of the cluster 

			select 
					case when Man_Dis_P1<Man_Dis_P2 then 'Cluster 1'
							when Man_Dis_P1>Man_Dis_P2 then 'Cluster 2'
							when Man_Dis_P1=Man_Dis_P2 then 'Marginal Point'
														end as cluster
					,B.*,A.Man_Dis_P1,A.Man_Dis_P2
					
					
					from manhattan A 
					INNER JOIN abs_d B 
					ON A.P1=B.P1
					

		


