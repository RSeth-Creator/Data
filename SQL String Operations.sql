--SQL Server String Function 
-- Find the ASCII value for the given String 
Select ASCII('what an idea') --Ans: 84

-- Find ASCII value for  A
select ASCII('A')--Ans:65

--Find the character for 64 
select char(64)--Ans:@

--Find he position of 'SQL in given text '
select CHARINDEX('SQL','this is first SQL ')--Ans:9
select CHARINDEX('this is my first SQL query ','SQL')--Ans:0

--Find the final output of the below query
Select CONCAT('SQL','queries') --Ans: This is SQL String Function Test queries
declare @b varchar(20)='This is SQL String Function Test '
Select CONCAT(@b,'queries') --Ans: This is SQL String Fqueries

--CONCAT add two string and give the output wheater CONACT_WS is used to contact more then two string .
--length function
--Find the output of the below code 
select DATALENGTH('This is my'+'ab') --Ans: error
select DATALENGTH(' @Abcd  ')--Ans:33
select len('this is my first query ')

--lower / upper case 
select lower('WHAT ')
select upper('what')
--Trimming the string 
select ltrim('   i am here ')
select rtrim('i am here    ')
select trim('   abcd   ')
select PATINDEX( 'here','i am here')

--cut the string 
select left ('hi there ,',2)
select right ('Hi, here i am ',3)

--Update a String 
select replace ('This is a replace function','replace','SQL')
select replicate('SQL',4)
select  reverse ('Structure Query Language')
select substring('Structured query language',5,4)
select stuff('abcd@email.com',2,3,'****')

-- create a dynamic query , where email id contains only first two letters and domain name 
--application of Stuff function 
declare @email varchar(50)='rajseth2018@gmail.com'
select stuff (@email,2,(len(@email)+1)-CHARINDEX('@',@email),'*****')

--Application of upper and lower function 
--only first letter will be in upper case 
Declare  @test  varchar(20)= ' test Function '
select concat(upper(substring(trim(@test),1,1)),
				lower(substring(trim(@test),2,len(@test))))














