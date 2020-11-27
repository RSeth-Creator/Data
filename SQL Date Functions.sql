select CURRENT_TIMESTAMP
--select DATEDIFF(getdate(), getdate(),DAY)

select DATENAME(DAY,GETDATE())

--Extract different date part 
select datepart(DAY,getdate())
select datepart(DAYOFYEAR,getdate())
select datepart(DW,getdate())
select datepart(year,getdate())

select datepart(MONTH,getdate())
select datepart(MS,getdate())
--Extract different time stamp
select GETUTCDATE()
select SYSDATETIME()
--Boolean type to check the string is ins date or not 
select ISDATE(getdate())
select ISDATE('1234')
--extract the date , month and yeat from a date
select YEAR	(getdate())
select month	(getdate())
select day	(getdate())

--different type of date format 
select convert (varchar , getdate(), 101)
select convert (varchar , getdate(), 102)
select convert (varchar , getdate(), 103)
select convert (varchar , getdate(), 104)
select convert (varchar , getdate(), 105)
select convert (varchar , getdate(), 106)
select convert (varchar , getdate(), 107)
select convert (varchar , getdate(), 108)
select convert (varchar , getdate(), 109)
select convert (varchar , getdate(), 110)
select convert (varchar , getdate(), 111)
select convert (varchar , getdate(), 112)