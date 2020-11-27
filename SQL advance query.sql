

--Inner join with key value null 
declare  @table1 as table (a int, b int )
insert into @table1 values(null,0),(0,1),(1,1)
declare  @table2 as table (a int, b int )
insert into @table2 values(0,0),(0,1),(1,1)

select * from @table1 x
inner join @table2 y
on x.a=y.a

--2)Recursive cte  
with cte (x) AS
(
SELECT 1
union all
SELECT x+3 from cte where x < 8
)
SELECT * FROM cte; 

--3)Stuff function
declare @email varchar(50)='rajseth2019@gmail.com'
select stuff(@email,4,len(@email)-13,'*****')



--4) group by total sum 
declare  @test as table (a int  , x varchar )
insert into  @test values(10,'a'),(23,'a'),(39,'b'),(47,'a'),(45,'b'),(123,'a'),(76,'b'),(54,'c'),(87,'c'),(53,'c')
select sum(a) over (partition by x order by x) from @test 


--5) cross join 
declare  @join as table (a int, b int )
insert into @join values(0,0),(0,1),(1,0),(1,1)
declare  @join1 as table (a int, b int )
insert into @join1 values(0,0),(0,1),(1,0),(1,1)

select * from @join x
cross join @join1 y
--on x.a=y.a

--7)Datatpe mismatch 
declare @tst as table (a varchar) 
insert into @tst values (1),(2),(1),(3),(1),(2),(3),(3),(2),(3)
select sum(a) from @tst

--8) %ile measurement 
declare @test_a  table (a float , b varchar )
declare @x float=2
declare @y float=5
insert into @test_a values(@x,'a'),(@y,'b'),(@y,'a'),(@x,'b')--,(4,'a'),(13,'a'),(2,'b'),(9,'a'),(10,'c'),(4,'a')
SELECT DISTINCT b  
       ,PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY a)  
        OVER (PARTITION BY b) AS z  
FROM @test_a 
  
--9) Identity key logic  

declare  @test_name  table ( id INT IDENTITY(1,1), name VARCHAR(50))
insert into @test_name values ( 'test1' ), ( 'test2' )
delete from @test_name where name='test2'
insert into @test_name values ('test2')

select   id , [name] FROM @test_name 


--10)pivot example  
declare @source table (name varchar, income float)
insert into @source values('A',10000),('B',13000),('C',20000),('A',20000)
SELECT 'income',[A], [B],[C]
FROM
(SELECT name, income
 FROM @source) AS s
PIVOT
(
 SUM(income)
 FOR name IN ([A], [B],[C])
) AS PivotTable;

declare @test as table  (id int identity (1000,67) , name  varchar(20), income float )
insert into @test values ('A',23000),('B',34000),('D',40000),('C',20000),('E',45000),('F',45000),('G',34000)

--11)find the rank of a person 
select * , RANK() over (order by income  desc) from @test

--12)find the nth heighest income  
select * , dense_RANK() over (order by income  desc) as rnk from @test 

--13)find the row number in each partition 
select *, row_number() over (partition by income order by income desc ) as rnk from @test 

--14)running sum 
select id, name ,income,sum(income) over (order by name ) as running_total from @test

--15)running avg
select id, name ,income,avg(income) over (order by name ) as running_total from @test 

--16)running difference forward 
;with cte as (
select ID,lag(income,1,0) over (order by name) n  from @test
)
select  a.id, name, income,income-n
from @test A 
inner join 
cte B 
on A.id=B.id

--17)running difference backward
;with cte2 as (
select ID,lead(income,1,0) over (order by name) n  from @test
)
select  a.id, name, income,income-n
from @test A 
inner join 
cte2 B 
on A.id=B.id








