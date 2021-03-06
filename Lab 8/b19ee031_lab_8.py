# -*- coding: utf-8 -*-
"""B19EE031 Lab_8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bn9Yo_J1eiem1z1SyDH-HQdxpC4YAe8l
"""

import pandas  as pd 
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns

"""Loading the dataset"""

df = pd.read_csv('/content/Iris.csv')
df.head()

x = df.iloc[:,1:-1]
x.head()

from sklearn.preprocessing import LabelEncoder
enc = LabelEncoder()
y = enc.fit_transform(df.Species)
df['target'] = y
y[:5]

"""**Part 1:** PCA analysis"""

from sklearn.preprocessing import StandardScaler
std = StandardScaler()
std.fit(x)
x = std.fit_transform(x)
x[:5]

from sklearn.decomposition import PCA
pca = PCA(.90)
pca.fit(x)

x_new = pca.fit_transform(x)
x_new[:5]

pca.explained_variance_ratio_

pca.components_

pca.explained_variance_

df_pca = pd.DataFrame(x_new, columns = ['PCA1','PCA2'])
df_pca['target'] = y
df_pca.corr()

plt.scatter(x_new[:,0],x_new[:,1],c =y)
plt.xlabel('PCA1')
plt.ylabel('PCA2')
plt.show()

from pylab import *
subplot(2,1,1)
sns.boxplot(x = y, y= x_new[:,0])
subplot(2,1,2)
sns.boxplot(x = y, y = x_new[:,1])

"""**Part 2**:  LDA analysis and Comparison"""

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
lda = LinearDiscriminantAnalysis(n_components=2)
x_new2 = lda.fit(x,y).transform(x)
x_new2[:5]

lda.explained_variance_ratio_

lda.coef_

lda.intercept_

plt.scatter(x_new2[:,0],x_new2[:,1],c =y)
plt.xlabel('LDA1')
plt.ylabel('LDA2')
plt.show()

subplot(2,1,1)
sns.boxplot(x = y, y= x_new2[:,0])
subplot(2,1,2)
sns.boxplot(x = y, y = x_new2[:,1])

"""Model comparisons"""

from pylab import *
subplot(2,1,1)
title('PCA')
plt.scatter(x_new[:,0],x_new[:,1],c=y)
subplot(2,1,2)
title('LDA')
plt.scatter(x_new2[:,0],x_new2[:,1],c=y)

"""Using Bayes model"""

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
gauss = GaussianNB()
x_train1,x_test1,y_train1,y_test1 = train_test_split(x_new,y,test_size=0.2) #for PCA
x_train2,x_test2,y_train2,y_test2 = train_test_split(x_new,y,test_size=0.2) #for LDA

#For PCA model
gauss.fit(x_train1,y_train1)
gauss.score(x_test1,y_test1)

#For LDA model
gauss = GaussianNB()
gauss.fit(x_train2,y_train2)
gauss.score(x_test2,y_test2)

"""**Part 3:** Feature Selection and Analysis"""

# Feature selection: Method 1
from sklearn.feature_selection import RFE
rfe = RFE(lda,2)
fit1 = rfe.fit(x,y)
fit1

print("Num Features: {}".format(fit1.n_features_))
print("Selected Features: {}".format(fit1.support_))
print("Feature Ranking: {}".format(fit1.ranking_))

selected_cols = []
for i in range(4):
  if fit1.support_[i] == True:
    selected_cols.append(df.columns[i+1])
selected_cols

df[selected_cols + ['target']].corr()

x = df.iloc[:,1:5]
feature1 = rfe.fit_transform(x,y)
feature1[:5]

#Feature Selection method 2
from sklearn.feature_selection import SelectKBest, chi2
skb = SelectKBest(score_func=chi2, k=2)
x = df.iloc[:,1:5]
fit = skb.fit(x, y)
fit

scores = fit.scores_
scores

features2 = fit.transform(x)
features2[0:5,:]

selected_cols2 = []
i = scores.argmax()   #i,j stores the indexes of 2 highest scores
selected_cols2.append(df.columns[i+1])
s1 = scores
s1[i]=0
j = s1.argmax()
selected_cols2.append(df.columns[j+1])
selected_cols2

# Applying gaussian model on feature selection by model 1
gauss = GaussianNB()
x_train,x_test,y_train,y_test = train_test_split(feature1,y)
gauss.fit(x_train,y_train)
gauss.score(x_test,y_test)

from sklearn.metrics import classification_report
y_pred = gauss.predict(x_test)
print(classification_report(y_test,y_pred))

# Applying Gaussian model for feature selection by model 2
gauss = GaussianNB()
x_train,x_test,y_train,y_test = train_test_split(features2,y)
gauss.fit(x_train,y_train)
gauss.score(x_test,y_test)

from sklearn.metrics import classification_report
y_pred = gauss.predict(x_test)
print(classification_report(y_test,y_pred))

"""Correlation matrixes"""

#For PCA
df_pca = pd.DataFrame(x_new,columns = ['PC1','PC2'])
df_pca['target'] = y
df_pca.corr()

corr_mat = df_pca.corr().abs()
kot = corr_mat[corr_mat>=.7]
plt.figure(figsize=(8,6))
sns.heatmap(kot, cmap="Greens")

kot

#For LDA
df_lda = pd.DataFrame(x_new2,columns = ['LDA1','LDA2'])
df_lda['target'] = y
df_lda.corr()

corr_mat = df_lda.corr().abs()
kot = corr_mat[corr_mat>=.7]
plt.figure(figsize=(8,6))
sns.heatmap(kot, cmap="Greens")

kot

# For RFE feature selection
df_rfe = pd.DataFrame(feature1,columns = ['RFE1','RFE2'])
df_rfe['target'] = y
df_rfe.corr()

corr_mat = df_rfe.corr().abs()
kot = corr_mat[corr_mat>=.7]
sns.heatmap(kot, cmap="Greens")

kot

# Feature Selection using kbest model
df_kbest = pd.DataFrame(features2,columns = ['KB1','KB2'])
df_kbest['target'] = y
df_kbest.corr()

corr_mat = df_kbest.corr().abs()
kot = corr_mat[corr_mat>=.7]
sns.heatmap(kot, cmap="Greens")

kot