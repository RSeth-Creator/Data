library(ggplot2) 
library(readr)
library(gridExtra)
library(grid)
library(tidyverse)
library(GGally)

iris
#Step1: get the dat set to R environment r 
pca_ds<-tibble(iris)
view(pca_ds)

# Step2: analysis of data 
ggplot(pca_ds,mapping = aes(Species))+geom_bar()

# summary 
summary(pca_ds)

#iris correlation plot
ggpairs(data = pca_ds,
        title = "Iris Correlation Plot",
        upper = list(continuous = wrap("cor", size = 5)), 
        lower = list(continuous = "smooth")
)

#Step3: 5 point visualization of iris data set 

BpSl <-   ggplot(pca_ds, aes(Species, Sepal.Length, fill=Species)) + 
  geom_boxplot()+
  scale_y_continuous("Sepal Length (cm)", breaks= seq(0,30, by=.5))+
  labs(title = "Sepal length vs Species", x = "Species")

BpSw <-   ggplot(pca_ds, aes(Species, Sepal.Width, fill=Species)) + 
  geom_boxplot()+
  scale_y_continuous("Setal width (cm)", breaks= seq(0,30, by=.5))+
  labs(title = "Petal width vs Species", x = "Species")

BpPl <-   ggplot(pca_ds, aes(Species, Petal.Length, fill=Species)) + 
  geom_boxplot()+
  scale_y_continuous("Petal Length (cm)", breaks= seq(0,30, by=.5))+
  labs(title = "Petal length vs Species", x = "Species")

BpPw <-    ggplot(pca_ds, aes(Species, Petal.Width, fill=Species)) + 
  geom_boxplot()+
  scale_y_continuous("Petal Width (cm)", breaks= seq(0,30, by=.5))+
  labs(title = "Petal width vs Species", x = "Species")

grid.arrange(BpSl, BpSw,BpPl,BpPw,nrow=2, ncol=2)
  

#Step 4 :Calculate mean 
Mean_sep_len<-mean(pca_ds$Sepal.Length)
Mean_sep_wid<-mean(pca_ds$Sepal.Width)
Mean_pet_len<-mean(pca_ds$Petal.Length)
Mean_pet_wid<-mean(pca_ds$Petal.Width)

#Step 5: creating new table with x(i)=x(i)-Mean
tbl_pca<-tibble(sep_len = pca_ds$Sepal.Length-Mean_sep_len, 
                sep_wid = pca_ds$Sepal.Width-Mean_sep_wid,
                pet_len = pca_ds$Petal.Length-Mean_pet_len,
                pet_wid = pca_ds$Petal.Width-Mean_pet_wid)


#Step 6: Calculate zero means and unit variance 
tbl_var<- tibble(VAR_sep_len = var(tbl_pca$sep_len),
                 VAR_sep_wid = var(tbl_pca$sep_wid),
                 VAR_pet_len = var(tbl_pca$pet_len),
                 VAR_pet_wid = var(tbl_pca$pet_wid))

#Step 7:divide each attribute value with  sd (z score normalization )
tbl_iris<-tibble(sep_len = tbl_pca$sep_len/tbl_var$VAR_sep_len,
                 sep_wid = tbl_pca$sep_wid/tbl_var$VAR_sep_wid,
                 pet_len = tbl_pca$pet_len/tbl_var$VAR_pet_len,
                 pet_wid = tbl_pca$pet_wid/tbl_var$VAR_pet_wid)


ggpairs(data = tbl_iris,
        title = "Iris Correlation Plot",
        upper = list(continuous = wrap("cor", size = 5)), 
        lower = list(continuous = "smooth")
)


#find out the co variance matrix 
cov(as.matrix(tbl_iris))
cov_matrix<-cov(as.matrix(tbl_pca))
cov_matrix

#total variance =sum of diagonal element or sum of eigen values 
sum(diag(cov_matrix))

#Step 8: find out the eigen values along with eigen vectors 
eigen(cov(as.matrix(tbl_pca)))
eigen(cov(as.matrix(tbl_iris)))

#Step 9: decomposition of the eigen values and eigen vectors 
eigenvalues = eigen(cov(as.matrix(tbl_pca)))$values
eigenvalues
max(eigenvalues)

#The eigen vectors represent the principal components
ev=eigen(cov(as.matrix(tbl_pca)))$vectors
ev

# Step 10: selection on eigen values 
diff(eigenvalues)

#the proportion of the total variance explained by the components.
plot(eigenvalues, xlab = 'Eigenvalue Number', ylab = 'Eigenvalue Size', main = ' Graph')
lines(eigenvalues)

# Step 11: Transpose of the eigen vector matrix 
ev
evt<-t(ev)
evt

#rotation
for (cov_matrix in eigenvalues) {
  print(cov_matrix / sum(eigenvalues))
}

#Step 12: matrix multiplication A(t)*x(i)
# PCA Analysis


pc1 <- tbl_pca$sep_len * evt[1,1] + tbl_pca$sep_wid*evt[1,2]+ tbl_pca$pet_len*evt[1,3]  + tbl_pca$pet_wid*evt[1,4]
pc1

pc2 <- tbl_pca$sep_len * evt[2,1] + tbl_pca$sep_wid*evt[2,2]+tbl_pca$pet_len*evt[2,3]      +tbl_pca$pet_wid*evt[2,4]
pc2


#Step 13: Graphical analysis


plot(pc1,pc2)

q<-ggplot(data = pca_ds, aes(x = pc1, y = pc4, color = Species, shape = Species)) +
  geom_hline(yintercept = 0, lty = 2) +
  geom_vline(xintercept = 0, lty = 2) +
  guides(color = guide_legend(title = "Species"), shape = guide_legend(title = "Species")) +
  scale_shape_manual(values = c(15, 16, 16, 17, 18)) +
  geom_point(alpha = 0.8, size = 2) 
q


p <- q + stat_ellipse(geom="polygon", aes(fill = Species),  alpha = 0.2, show.legend = FALSE, level = 0.95) +
  xlab("PC 1") +   ylab("PC 2") +
  theme_minimal() +theme(panel.grid = element_blank(), 
                         panel.border = element_rect(fill= "transparent"))
p


#** Using Prcomp pca analysis of  iris data 

#The prcomp function takes in the data as input, and it is highly recommended to set the argument scale=TRUE.
#This standardize the input data so that it has zero mean and variance one before doing PCA.
#Standard deviation: This is simply the eigenvalues in our case since the data has been centered and scaled (standardized)
#Proportion of Variance: This is the amount of variance the component accounts for in the data, 
#Cumulative Proportion: This is simply the accumulated amount of explained variance, 


data <- data.frame(pca_ds$Sepal.Length,pca_ds$Sepal.Width,pca_ds$Petal.Length,pca_ds$Petal.Width)
data.pca <- prcomp(data)
data.pca
summary(data.pca)
names(data.pca)
data.pca
data.pca$x
plot(data.pca$x[,1], data.pca$x[,2], pch = 19)



























