set.seed(42)

trainIndex <- createDataPartition(spambase$type, p=0.7, list = FALSE)

Train <- spambase[ trainIndex, ]

Test <- spambase[ -trainIndex, ]

svmGrid <- expand.grid(sigma =
                         c(0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1), C = c(0.25, 0.5, 1, 2, 4, 8, 16, 32, 64, 128))

trainctrl <- trainControl(method = "cv", number = 10, verboseIter = TRUE)

svm.model <- train(type~., data = Train, method = "svmRadial", 
                   trControl = trainctrl, tuneGrid = svmGrid)
                   
svm.predict <- predict(svm.model, Test)

confusionMatrix(svm.predict, as.factor(Test$type), mode = "prec_recall")

set.seed(42)

nnet.model <- train(type~., data = Train, method = "nnet", 
                    tuneLength = 10, 
                    trControl = trainctrl,
                    metric="Accuracy")

nnet.predict <- predict(nnet.model, test)

confusionMatrix(nnet.predict, as.factor(Test$type), mode = "prec_recall")

set.seed(42)

nnet.predict <- predict(nnet.model, Test)

confusionMatrix(nnet.predict, as.factor(Test$type), mode = "prec_recall")