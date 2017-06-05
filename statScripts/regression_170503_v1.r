Sys.setenv(LANG="en")
library(RMySQL)
con_sql <- dbConnect(RMySQL::MySQL(),user="root", dbname="patent_research_dev")
PanelData <- dbReadTable(conn = con_sql, name="FinalTableV13", header=TRUE, row.names=NULL)

options(scipen=999)

library(plm)
library(Hmisc)
library(MASS)
library(rms)
library(stargazer)
library(dummies)
library(lmtest)




# model1<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model2<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Industry
# 		+ Country
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model3<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model3.ftest<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model4<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		, data=PanelData, index=c("Company","Year_Dum"), model="random")
# model4.ftest<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		, data=PanelData, index=c("Company","Year_Dum"), model="random")




# model1.time<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ factor(Year)
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model2.time<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Industry
# 		+ Country
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ factor(Year)
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model3.time<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		+ factor(Year)
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model3.timeftest<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		+ factor(Year)
# 		, x=TRUE, data=PanelData, index=c("Company","Year_Dum"), model="within")
# model4.time<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		+ factor(Year)
# 		, data=PanelData, index=c("Company","Year_Dum"), model="random")
# model4.timeftest<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		+ factor(Year)
# 		, data=PanelData, index=c("Company","Year_Dum"), model="random")


# olsmodel<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		, data=PanelData, index=c("Company","Year_Dum"), model="pooling")
# olsmodel.time<-plm(
# 		Market_Capital ~
# 		+ Company_Diversity
# 		+ Industry_Diversity
# 		+ Technological_Diversity
# 		+ Experience
# 		+ Experience_Quality
# 		+ Company_Diversity*Industry_Diversity*Technological_Diversity
# 		+ Experience*Experience_Quality
# 		+ Market_Age
# 		+ Number_of_Employees
# 		+ Company_Patents
# 		+ Company_Star_Patents
# 		+ Total_Assets
# 		+ Operating_Revenue
# 		+ Research_and_Development_Expenses
# 		+ EBITDA
# 		+ Industry
# 		+ Country
# 		+ factor(Year)
# 		, data=PanelData, index=c("Company","Year_Dum"), model="pooling")




# # Testing for random effects: Breusch-Pagan Lagrange multiplier (LM)
# # Significant results = Random Model
# # 
# # The null hypothesis in the LM test is that
# # variances across entities is zero. This is, no
# # significant difference across units (i.e. no panel
# # effect).
# # 
# # OLS or NOT OLS

# print("")
# print("")
# print("#####################")
# print("")
# print("")
# print("Fixed/Random or OLS")
# print(plmtest(olsmodel, type=c("bp")))
# print(plmtest(olsmodel.time, type=c("bp")))


# # Testing time-fixed effects. The null is that no time-fixed
# # effects needed
# # 
# # To see if time fixed effects are needed
# # when running a FE model use the
# # command testparm. It is a joint test to
# # see if the dummies for all years are equal
# # to 0, if they are then no time fixed effects
# # are needed

# print("")
# print("")
# print("#####################")
# print("")
# print("")
# print("Test for Time-fixed effects for each model")
# print("Model 1")
# print(pFtest(model1.time, model1))

# print("Model 2")
# print(pFtest(model2.time, model2))

# print("Model 3")
# print(pFtest(model3.time, model3))

# print("Model 4")
# print(pFtest(model4.time, model4))



# # Hausman test
# # FIXED or RANDOM

# print("")
# print("")
# print("#####################")
# print("")
# print("")
# print("Test if Fixed or Random")
# print("model3 vs model4")
# print(phtest(model3.ftest,model4.ftest))
# print(phtest(model3.timeftest,model4.timeftest))


# # VIF test for multicollinearity

# print("")
# print("")
# print("#####################")
# print("")
# print("")
# print("Test for multicollinearity")

# print("Model 1")
# # print(vif(model1.time))
# print(sqrt(vif(model1.time)))

# print("Model 2")
# # print(vif(model2.time))
# print(sqrt(vif(model2.time)))

# print("Model 3")
# # print(vif(model3.time))
# print(sqrt(vif(model3.time)))

# print("Model 4")
# # print(vif(model4.time))
# print(sqrt(vif(model4.time)))


# # Testing for heteroskedasticity
# # The null hypothesis for the Breusch-Pagan test is homoskedasticity.

# print("")
# print("")
# print("#####################")
# print("")
# print("")
# print("Test for heteroskedasticity")
# print("Model 1")
# print(bptest(model1, studentize=F))
# print(bptest(model1.time, studentize=F))

# print("Model 2")
# print(bptest(model2, studentize=F))
# print(bptest(model2.time, studentize=F))

# print("Model 3")
# print(bptest(model3, studentize=F))
# print(bptest(model3.time, studentize=F))

# print("Model 4")
# print(bptest(model4, studentize=F))
# print(bptest(model4.time, studentize=F))



# # Summary for each model


# print("")
# print("")
# print("Model 1")
# # print(summary(model1))
# # print("########")
# print(summary(model1.time))


# print("")
# print("")
# print("Model 2")
# # print(summary(model2))
# # print("########")
# print(summary(model2.time))


# print("")
# print("")
# print("Model 3")
# # print(summary(model3))
# # print("########")
# print(summary(model3.time))


# print("")
# print("")
# print("Model 4")
# # print(summary(model4))
# # print("########")
# print(summary(model4.time))

















print(
	cor(
		data.frame(
			PanelData$Company_Diversity,
			PanelData$Industry_Diversity,
			PanelData$Technological_Diversity,
			PanelData$Experience,
			PanelData$Experience_Quality
		)
	)
)

# Retrieving the barplots

test <- aggregate(PanelData, by=list(PanelData$Company),FUN=head,1)

# par(mfrow=c(1,2))
# barplot(table(test$Country),horiz=TRUE,las=2,cex.names=0.6,cex.axis=0.8,xlab="Companies",ylab="Country")
# barplot(table(test$Industry),horiz=TRUE,las=2,cex.names=0.45,cex.axis=0.8,xlab="Companies",ylab="Industry")


# require( tikzDevice )
# tikz( 'myPlot.tex' )

# stargazer(PanelData, align=TRUE,summary=TRUE, no.space=TRUE, single.row=TRUE)

lapply( dbListConnections( dbDriver( drv = "MySQL")), dbDisconnect)
