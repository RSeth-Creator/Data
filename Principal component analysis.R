library(ggplot2) 
library(readr)
library(gridExtra)
library(grid)
library(tidyverse)
library(GGally)
?iris
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


#make_matrix <- function(df,rownames = NULL){
#  my_matrix <-  as.matrix(df)
#  if(!is.null(rownames))
#   rownames(my_matrix) = rownames
#  my_matrix
#}
#(my_tibble = tibble( row_names=1:10,a = 1:10, b = 11:20, c = 21:30))
#(my_matrix <- make_matrix(select(my_tibble,-row_names),
#                          pull(my_tibble,row_names)))


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
diff(eigenvalues1)

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


pc1 <- pca_ds$Sepal.Length * evt[1,1] +pca_ds$Sepal.Width*evt[1,2]+pca_ds$Petal.Length*evt[1,3]        +pca_ds$Petal.Width*evt[1,4]
pc1

pc2 <- pca_ds$Sepal.Length * evt[2,1] + pca_ds$Sepal.Width*evt[2,2]+pca_ds$Petal.Length*evt[2,3]      +pca_ds$Petal.Width*evt[2,4]
pc2

pc3 <- pca_ds$Sepal.Length * evt[3,1] + pca_ds$Sepal.Width*evt[3,2]+pca_ds$Petal.Length*evt[3,3]
+pca_ds$Petal.Width*evt[3,4]
pc3

pc4 <- pca_ds$Sepal.Length * evt[4,1] + pca_ds$Sepal.Width*evt[4,2]+pca_ds$Petal.Length*evt[4,3]+ pca_ds$Petal.Width*evt[4,4]
pc4

final<-tibble(pc1,pc2,pc3,pc4)
final

#Step 13: Graphical analysis

par(mfrow=c(2,3))
plot(pc1,pc2)
plot(pc1,pc3)
plot(pc1,pc4)

plot(pc2,pc3)
plot(pc2,pc1)
plot(pc2,pc4)


par(mfrow=c(2,3))
plot(pc3,pc1)
plot(pc3,pc2)
plot(pc3,pc4)


plot(pc4,pc1)
plot(pc4,pc2)
plot(pc4,pc3)

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



##don't count this is for test
# Test purpose

eigenvalues1 = eigen(cov(as.matrix(tbl_iris)))$values
eigenvalues1
max(eigenvalues1)
ev1=eigen(cov(as.matrix(tbl_iris)))$vectors
ev1


pc11 <- pca_ds$Sepal.Length * ev1[1,1] + pca_ds$Sepal.Length*ev1[2,1]+pca_ds$Petal.Length*ev1[3,1]
      +pca_ds$Petal.Width*ev1[4,1]
pc11

pc22 <- pca_ds$Sepal.Length * ev1[1,2] + pca_ds$Sepal.Length*ev1[2,2]+pca_ds$Petal.Length*ev1[3,2]
        +pca_ds$Petal.Width*ev1[4,2]
pc22

  
pc33 <- pca_ds$Sepal.Length * ev1[1,3] + pca_ds$Sepal.Length*ev1[2,3]+pca_ds$Petal.Length*ev1[3,3]
 +pca_ds$Petal.Width*ev1[4,3]
pc33
  
pc44 <- pca_ds$Sepal.Length * ev1[1,4] + pca_ds$Sepal.Length*ev1[2,4]+pca_ds$Petal.Length*ev1[3,4]
+pca_ds$Petal.Width*ev1[4,4]
pc44
  
  
  tibble(pc11,pc22,pc33,pc44)

  par(mfrow=c(2,3))
  plot(pc11,pc22)
  plot(pc11,pc33)
  plot(pc11,pc44)
  
  plot(pc22,pc33)
  plot(pc22,pc11)
  plot(pc22,pc44)

  

























