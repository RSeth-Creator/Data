set nocount on
--Craete Table to load some sample data 
DECLARE @NB AS TABLE (
Outlook char(50),Temp char(50),Humdt char(50),Windy char(50),Play_sts char(50)
)
--load sample data point 
Insert into @NB values
('Sunny','Hot','High','False','No'),
('Sunny','Hot','High','True','No'),
('Overcast','Hot','High','False','Yes'),
('Rainy','Mild','High','False','Yes'),
('Rainy','Cool','Normal','False','Yes'),
('Rainy','Mild','Normal','True','No'),
('Overcast','Cool','Normal','True','Yes'),
('Sunny','Mild','High','False','No'),
('Sunny','Cool','Normal','False','Yes'),
('Rainy','Cool','Normal','False','Yes'),
('Sunny','Mild','Normal','True','Yes'),
('Overcast','Mild','High','True','Yes'),
('Overcast','Hot','Normal','False','Yes'),
('Rainy','Mild','High','True','No')

declare @Outlook varchar(20)
		,@Temperature varchar(20) 
		,@Humidity Varchar(20)
		,@Windy varchar(20)
		,@Condition Varchar(20)

	Set @Outlook='Sunny'
	Set @Temperature='Hot' 
	set @Humidity ='High'
	set @Windy ='False'
	set @Condition= 'No'

		Declare @Yes int = (Select count(Play_sts)  from @NB where Play_sts='Yes'),
				@NO int = (Select count(Play_sts)  from @NB where Play_sts='No')

		Declare @Prob_Yes float =(select round((cast(@Yes as float)/(@Yes+@No)),3) ),
				@Prob_No Float =(round(Cast(@No as float)/(@Yes+@No),3) )

		declare @Prob_Outlook float =(select cast( count(Play_sts) as float)/@Yes  from @NB where Outlook=@Outlook and Play_sts=@Condition ),
				@Prob_Temperature float=(select cast( count(Play_sts) as float)/@Yes  from @NB where Temp=@Temperature and Play_sts=@Condition ),
				@Prob_Humidity float=(select cast( count(Play_sts) as float)/@Yes  from @NB where Humdt=@Humidity and Play_sts=@Condition ),
			    @Prob_Windy float=(select cast( count(Play_sts) as float)/@Yes  from @NB where Windy=@Windy and Play_sts=@Condition )

					if @Condition='Yes'
						print 'P('+@Condition+') =  '+cast ( @Prob_Yes as varchar(20))
					else 
						Print 'P('+@Condition+') =  '+cast ( @Prob_No as varchar(20))

					Print 'p(Outlook= '+@Outlook+'|'+@Condition+') =  '+cast ( @Prob_Outlook as varchar(20))
					Print 'p(Temperature= '+@Temperature+'|'+@Condition+') =  '+cast ( @Prob_Temperature as varchar(20))
					Print 'p(Humidity= '+@Humidity+'|'+@Condition+') =  '+cast ( @Prob_Humidity as varchar(20))
					Print 'p(Windy= '+@Windy+'|'+@Condition+') =  '+cast ( @Prob_Windy as varchar(20))
					
					Print'P('+@Condition+'|X) = '
						if @Condition='Yes'
							Print(@Prob_Outlook*@Prob_Temperature*@Prob_Humidity*@Prob_Windy*@Prob_Yes)
						else 
							Print(@Prob_Outlook*@Prob_Temperature*@Prob_Humidity*@Prob_Windy*@Prob_No)
					
						


						

--Frequency table /with respect to attribute 
;with Outlook as (
			select * from (
						select Outlook,Play_sts  from @NB)s
			pivot(
			count(Play_sts)
			for Play_sts IN(
					[Yes],
					[No]
					) )a 
				)
--select * from Outlook

,Temp as (
			select * from (
						select Temp,Play_sts  from @NB)s
			pivot(
			count(Play_sts)
			for Play_sts IN(
					[Yes],
					[No]
					) )a 
				)
--select * from Temp

,Humdt as (
			select * from (
						select Humdt,Play_sts  from @NB)s
			pivot(
			count(Play_sts)
			for Play_sts IN(
					[Yes],
					[No]
					) )a 
				)
--select * from Humdt


,Windy as (
			select * from (
						select Windy,Play_sts  from @NB)s
			pivot(
			count(Play_sts)
			for Play_sts IN(
					[Yes],
					[No]
					) )a 
				)
--select * from Windy



,Freq as (
			select 'Outlook' as Attribute  ,Outlook as Status,Yes, No,round((cast(Yes as float)/@Yes),3) as Prob_Yes,Cast(No as float)/@No as Prob_No from Outlook
					union
			select'Temperature' as Attribute ,Temp as Status,Yes, No ,round((cast(Yes as float)/@Yes),3) as Prob_Yes,Cast(No as float)/@No as Prob_No from Temp
					union
			select 'Humidity'as Attribute ,Humdt as Status,Yes, No,round((cast(Yes as float)/@Yes),3) as Prob_Yes,Cast(No as float)/@No as Prob_No from Humdt
					Union 
			Select 'Windy'as Attribute , Windy as Status,Yes, No,round((cast(Yes as float)/@Yes),3) as Prob_Yes,Cast(No as float)/@No as Prob_No from Windy


)

	select 
		Case when Status is null  then ''
				else Attribute 
					end as Attribute,
		Case when Status is Null then 'Total'
				else Status 
					end as Status,
		sum(yes) Yes,Sum(No) No,sum(Prob_Yes)Prob_Yes,sum(Prob_No) Prob_No
		from Freq
		
			group by rollup (Attribute,Status)
			having sum(Prob_No)<=1

		

