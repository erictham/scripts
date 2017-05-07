# Homework assignment for Empirical methods in finance
# installing and loading the required packages
list.of.packages <- c("gmm")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages)
require("gmm")

# Setting the active directory
setwd("C:/Users/u6038155/Documents/Scripts/R")
rm(list=ls())
# Gmm function
# theta[1] : coefficient of risk aversion
# theta[2] : impatience discount factor
momfn <- function(tet, x)
{
  consume <- x[,"con_growth"]
  consume_pow <- consume^-tet[1]
  sp500_ret_f <- 1+x[,"sp500_ret"]
  rate_real_ret_f <- x[,"rate_real"]
  m1 <- tet[2]*(consume_pow *sp500_ret_f)-1
  m2 <- tet[2]*(consume_pow *rate_real_ret_f)-1
  m1 <-m1
  m2 <-m2
  fn <- cbind(m1,m2)
  return(fn)
}

Dg <- function(tet, x)
{
  consume <- x[,"cons_ret"]
  sp500_ret <- (1+x[,"sp500_ret"])
  rate_real_ret <- (1+x[,"rate_real_ret"])
  jacobian <- matrix(c(-tet[1]*tet[2]*mean(consume^(-tet[1]-1)), mean((consume^-tet[1])*sp500_ret),
                       -tet[1]*tet[2]*mean(consume^(-tet[1]-1)), mean((consume^-tet[1])*rate_real_ret)), 
                       nrow=2,ncol=2)
   return(jacobian)
}

# Q1: Reading in data and compute returns
emf<-read.delim2("data_1.txt",sep="\t",header=TRUE)
# consumption growth
con_growth <- as.numeric(levels(emf[,"con_growth"])[emf[,"con_growth"]])
# real interest rates returns
rate_real<- as.numeric(levels(emf[,"rate_real"])[emf[,"rate_real"]])
# sp returns
sp500_ret<- as.numeric(levels(emf[,"sp500_ret"])[emf[,"sp500_ret"]])
# Q1 Combine data together and
gmmdata<-cbind(con_growth,sp500_ret,rate_real)

wtMat = matrix( c(1,0,0,1),nrow=2, ncol=2)
# Run
gmmres1step<-gmm(momfn, gmmdata,t0=c(riskcoeff=8,df=1.0), 
            traceIter= TRUE, weightsMatrix = wtMat) #,  gradv = Dg)
gmmres2step<-gmm(momfn, gmmdata,t0=c(riskcoeff=8,df=1.0), 
                 type="twoStep",traceIter= TRUE) #,  gradv = Dg)
print(summary(gmmres1step))
print(summary(gmmres2step))
