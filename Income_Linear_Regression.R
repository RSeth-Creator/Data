library(tidyverse)
ds<-read.csv("~/income_data.csv")
attach(ds)
plot(ds$income,ds$happiness)
ggplot(data=ds,aes(income))+geom_histogram()
ggplot(data=ds,aes(happiness))+geom_histogram()
summary(ds)
a<-sum((income-mean(income))*(happiness-mean(happiness)))
a
b<-sum((income-mean(income))**2)
b
b1<-a/b
b1
b0<-mean(happiness)-b1*mean(income)
b0
linear_model<-lm(happiness~income)
summary(linear_model)

plot(linear_model)

ggplot(linear_model, aes(x=income, y=happiness))+  geom_point()+geom_smooth(formula="lm",col="black")

x<-readline(prompt="Enter your income : ")
x<-as.numeric(x)
x
y<-b0+b1*x
cat("your happiness index is :", y)






