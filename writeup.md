# Classifying Images of Birds
#### Maureen Aubrey, Jacob Malcy, and Spencer Wegner  
CSCI 4622 Machine Learning  
University of Colorado Boulder

## Problem
- Is there a clear explanation about what this project is about? Does it state clearly which type of problem (e.g. type of learning and type of the task)?
- Does it state the motivation or the goal (or why it’s important, what goal the team wants to achieve, or want to learn) clearly?
- (Extra credit) Is the project topic creative? Requires collecting data (e.g. scraping)?

The goal of this project is to classify images of birds using a convolutional neural network (CNN). Image classification and recognition, a subset of deep and supervised learning, is becoming more and more important in modern technology. Examples include self-driving cars, medical imagery and diagnoses, and e-commerce. Understanding how CNNs effectively classify large volumes of image data yields endless possibilities.  

Our team found a comprehensive data set of bird images and realized that while classifying images of birds may seem pointless to some individuals, bird watchers and wildlife enthusiasts would find great value in such a classifier. If a mobile application were built around our model many people would derive great value from it. As a team we also wanted to learn more about CNNs and get more experience working with them. 

In this project we try several different CNN architectures to see which one performs best on the bird images. By experimenting with different architectures we hope to gain some insight as to why one works better than others.

## Data
- Is data source properly quoted and described? (including links, brief explanations)
- Do they explain the data description properly? The data description can include the data size
    - e.g. for tabulated data: number of samples/rows, number of features/columns, bytesize if a huge file, data type of each feature (or just a summary if too many features- e.g. 10 categorical, 20 numeric features), description of features (at least some key features if too many), whether the data is multi-table form or gathered from multiple data source.
    - e.g. for images: you can include how many samples, number of channels (color or gray or more?) or modalities, image file format, whether images have the same dimension or not etc.
    - e.g. sequential data: texts, sound file; please describe appropriate properties such as how many documents or words, how many sound files with typical length (are they the same or variable), etc.

Our data set is sourced from a 2011 Caltech and UCSB collaboration. 
The dataset can be downloaded [here](http://www.vision.caltech.edu/visipedia/CUB-200-2011.html). 

There are 200 species of birds in this dataset and 11,788 images. 

#### Data Source Citation
Wah C., Branson S., Welinder P., Perona P., Belongie S. “The Caltech-UCSD Birds-200-2011 Dataset.” Computation & Neural Systems Technical Report, CNS-TR-2011-001.

## Data Cleaning
Example score breakdown for tabulated data format: no cleaning 0 pts (if the data was given perfectly cleaned, just give a default score of 5 pts), data types munging +1, drop NA +1, impute +2, identify imbalance +2 identify data-specific potential problem +2, and address issues +2.

- Does it include clear explanations on how and why a cleaning is performed?
    - (e.g.) the author decided to drop a feature because it had too many NaN values and the data cannot be imputed.
    - (e.g.) the author decided to impute certain values in a feature because the number of missing values were small and he/she was able to find similar samples OR, he/she used an average value or interpolated value, etc.
    - (e.g.) the author removed some features because there are too many of them and they are not relevant to the problem, or he/she knows only a few certain features are important based on their domain knowledge judgement.
    - (e.g.) the author removed certain sample (row) or a value because it is an outlier.
- Does it have conclusions or discussions? 
    - e.g. the data cleaning summary, findings, discussing foreseen difficulties and/or analysis strategy.
- Does it have a proper visualization?

## Exploratory Data Analysis
Example score breakdown: 10 for simple plots (histogram, box plot), correlation mat (+5), extra EDA (e.g. statistical tests) +5, with some insights/conclusion +5

- Does it include clear explanations on how and why an analysis (EDA) is performed?
- Does it have a proper visualization?
- Does it have proper analysis? E.g. histogram, correlation matrix, feature importance (if possible) etc.
- Does it have conclusions or discussions? E.g. the EDA summary, findings, discussing foreseen difficulties and/or analysis strategy.

## Model
Example score breakdown for typical supervised learning: 10 if a proper single model is used, +5 if addresses multilinear regression/collinearity for regression models, +5 feature engineering, +5 multiple ML models, +5 hyperparam tuning, +5 regularization or other training techniques such as cross validation, oversampling/undersamping/SMOTE or similar for managing data imbalance, +5 using models not covered from class.

- Is the choice of model(s) appropriate with the problem?
- Is the author aware of whether interaction/collinearity between features can be a problem for the choice of the model and properly treat if there is interaction or collinearity (e.g. linear regression)? Or confirms that there is no such effect with the choice of the model?
- Did the author use multiple (appropriate) models?
- Did the author investigate which ones are important features by looking at feature rankings or importance from the model? (Not by judgement- which we already covered in the EDA category) Did the author use techniques to reduce overfitting or data imbalance?
Did the author use new techniques/models we didn't cover in the class?

## Results and Analysis
Example score breakdown: showing basic result 10, with a good amount of visualization +5, try different evaluation metrics +5, iterate training/evaluating and improve performance +5, show/discuss model comparison +5

- Does it have a summary of results and analysis?
- Does it have a proper visualization? (e.g. tables, graphs/plots, heat maps, statistics summary with interpretation etc)
- Does it use different kinds of evaluation metric properly? (e.g. if your data is imbalance, there are other metrics F1, ROC or AUC better than mere accuracy). Also does it explain why they chose the metric?
- Does it iterate the training and evaluation process and improve the performance? Does it address selecting features through the iteration process?
- Did the author compare the results from the multiple models and did appropriate comparison?

## Discussion and Conclusion
Example score breakdown: basic reiteration of result 5, discussion on what are the learnings and takeaways, discussion on why something didn't work +5, suggesting ways to improve +5.