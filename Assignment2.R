#Load the quakes data into R environment 
quakes<-quakes
quakes

#a.proportion of seismic events >300 km
depth_300<-subset(quakes,quakes$depth>=300)
prp<-nrow(depth_300)/nrow(quakes)
cat("the proportion of seismic events >=300 km in quakes data ",prp*100,"%")

#b. mean median of magnitude in quakes data set 
Mean_Mag<-mean(depth_300$mag)
cat("the mean of magnitude  (seismic events >=300 km) in quakes data ",Mean_Mag)
Median_Mag<-median(depth_300$mag)
cat("the median of magnitude (seismic events >=300 km)in quakes data ",Median_Mag)
Sum_Mag<-summary(depth_300$mag)
cat("the Summary of magnitude (seismic events >=300 km) in quakes data ",Sum_Mag)

#group wise mean calculation 
Uni_feed<-list(unique(chickwts$feed))
for ( item in Uni_feed){
  data<-aggregate(chickwts$weight,chickwts$feed, mean)
}
print(data)
#distribution of modes 
freq <- table(InsectSprays$count)
freq
plot(freq)
cat("max occurance is :",max(freq))
#mode of the data set (item & frequency)
freq[freq==max(freq)]
InsectSprays

#total insect counts by each spray type
tapply(InsectSprays$count, InsectSprays$spray, sum)

#group that had at least five bugs
NInsectSprays<-subset(InsectSprays,InsectSprays$count>=5)

#NInsectSprays
#compute the Proportion of agricultural units in each spray type group 
tapply(NInsectSprays$count,INDEX=NInsectSprays$spray,
       FUN=function(x) length(x)/nrow(NInsectSprays))

#compute the percentage of agricultural units in each spray type group 
tapply(NInsectSprays$count,INDEX=NInsectSprays$spray,
       FUN=function(x) round((length(x)/nrow(NInsectSprays))*100))

chickwts 
quant<-quantile(chickwts$weight,prob=c(0,0.25,0.5,0.75,1))
quant
boxplot(chickwts$weight,ylab="Weight")
plot(chickwts$feed,chickwts$weight)







