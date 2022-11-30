#Lab #5
#Code is publicly available @ https://machinelearningmastery.com/feature-selection-with-the-caret-r-package/


#The first time you run this code, un-comment the two next lines to install the packages
install.packages('caret')
install.packages('e1071')
install.packages("randomForest")
install.packages('mlbench')
install.packages('Hmisc')
install.packages('corrplot')
install.packages('ggcorrplot')
install.packages('https://cran.r-project.org/src/contrib/Archive/randomForest/', repos=NULL, type="source") 


#load libraries
library(caret)
library(e1071)
library(mlbench)
library(caret)
library(randomForest)
library(Hmisc)
library(corrplot)
library(ggcorrplot)

# ensure the results are repeatable
set.seed(7)
# Get attributes that are highly correlated

# Read the data from the csv file
# DERBY dataset with 33 columns
# This portion never works for me, so I just import the dataset manually 
# So where it says 33 columns, i assume the following times we use 33 should be 58 since spambase has 58 -David

# load the data
# calculate correlation matrix
# See library https://www.rdocumentation.org/packages/caret/versions/6.0-93/topics/findCorrelation
spambase$x <- NULL

#%%%%%%%%%%%%%%%%%%%%%%%%%%% un-comment lines 42-45 when using spambase dataset %%%%%%%%%%%%%%%%%%%%%%%%%
# change type to numerical (0 for nonspam and 1 for spam)
spambase[spambase =='nonspam'] <- as.numeric(0)    
spambase[spambase =='spam'] <- as.numeric(1)
spambase$type = as.numeric(spambase$type) 
str(spambase)
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

correlationMatrix <- cor(spambase[,1:58])
# using the 1:58 only works after you make 'nonspam and spam' numeric, hence rearranging the code
# summarize the correlation matrix
print(correlationMatrix)
View (correlationMatrix)


#get correlation matrix - representation 1
visCorMatrix1 <- corrplot(cor(spambase))

#get correlation matrix - representation 2
visCorMatrix2<-ggcorrplot(cor(spambase))

visCorMatrix2

# find attributes that are highly corrected (ideally >0.75)
highlyCorrelated <- findCorrelation(correlationMatrix, cutoff=0.5,verbose = FALSE,names = TRUE )
# print highly correlated attributes
print(highlyCorrelated)

# ensure results are repeatable
set.seed(7)
# prepare training scheme
control <- trainControl(method="repeatedcv", number=10, repeats=3)
# train the model
model <- train(as.factor(type)~., data=spambase, method="lvq", preProcess="scale", trControl=control)
# estimate variable importance
# This will take a minute
importance <- varImp(model, scale=FALSE)
# summarize importance
# This will take a minute
print(importance)
# plot importance
plot(importance)

#Recursive Feature Elimination (RFE) ---------------------------------
# ensure the results are repeatable
set.seed(7)
# load the library
library(mlbench)
library(caret)
# load the data
# define the control using a random forest selection function
# This will take a moment.FYI.
control <- rfeControl(functions=rfFuncs, method="cv", number=10)

# run the RFE algorithm
# results <- rfe(spambase[,1:57], spambase[,58], sizes=c(1:57), rfeControl=control) still not exactly sure on these numbers
# I know derby has classifiers in both row 32 and 33 (bug = T/F, and ref = T/F) so maybe this needs tweaked
results <- rfe(spambase[,1:57], spambase[,58], sizes=c(1:57), rfeControl=control)

# summarize the results
# this will take a hot minute
print(results)
# list the chosen features
predictors(results)
# plot the results
plot(results, type=c("g", "o"))

step8vars <- c("remove", "charExclamation", "hp", "charDollar","edu", "type")
step8subset <- dataset[step8vars]
step8subset$type = as.factor(step8subset$type)
set.seed(7)
trainIndex8 <- createDataPartition(step8subset$type, p=0.7, list = FALSE)
Train8 <- step8subset[ trainIndex8, ]
Test8 <- step8subset[ -trainIndex8, ]
trainctrl8 <- trainControl(method = "cv", number = 10, verboseIter = TRUE)
svm.modelstep8 <- train(type~., data = Train8, method = "svmRadial", tuneLength = 10, trControl = trainctrl8, metric = "Accuracy")
svm.predictstep8 <- predict(svm.modelstep8, Test8)
confusionMatrix(svm.predict, as.factor(Test8$type), mode = "prec_recall")

step6vars <- c("charExclamation", "your", "num000", "remove","charDollar", "you", "free", "business", "hp", "capitalTotal", "our", "receive", "hpl", "over", "order", "money", "capitalLong", "internet", "email", "all", "type")
step6subset <- dataset[step6vars]
step6subset$type = as.factor(step6subset$type)
set.seed(7)
trainIndex6 <- createDataPartition(step6subset$type, p=0.7, list = FALSE)
Train6 <- step6subset[ trainIndex6, ]
Test6 <- step6subset[ -trainIndex6, ]
trainctrl6 <- trainControl(method = "cv", number = 10, verboseIter = TRUE)
svm.modelstep6 <- train(type~., data = Train6, method = "svmRadial", tuneLength = 10, trControl = trainctrl6, metric = "Accuracy")
svm.predictstep6 <- predict(svm.modelstep6, Test6)
confusionMatrix(svm.predictstep6, as.factor(Test6$type), mode = "prec_recall")

dataset$x <-NULL
set.seed(7)
trainIndex <- createDataPartition(dataset$type, p=0.7, list = FALSE)
Train <- dataset[ trainIndex, ]
Test <- dataset[ -trainIndex, ]
trainctrl <- trainControl(method = "cv", number = 10, verboseIter = TRUE)
svm.model <- train(type~., data = Train, method = "svmRadial", tuneLength = 10, trControl = trainctrl, metric = "Accuracy")
svm.predict <- predict(svm.model, Test)
confusionMatrix(svm.predict, as.factor(Test$type), mode = "prec_recall")