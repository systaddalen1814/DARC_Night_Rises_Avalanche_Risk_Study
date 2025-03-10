# Data Science Capstone
CSCI 491 Data Science Capstone Repo

<p align="center">
<img src="https://github.com/user-attachments/assets/e6cd2524-f3e1-455b-a465-38def6250a02" height=200 width=200></img>
</p>


### Avalanche Risk Communiaction Pipeline 

## 0_WebScraper 

This scapes the messages from our chosen avalanche centers’ websites and
separates the files into CSVs by center, then again by risk. This way, each center has 5
associated files, one for each avalanche risk level. A data visualization was created for
each CSV to see where we had missing data.

## 1_DataClean

We removed any rows with missing data for the messages. We
generated series of histograms to count the number of observations
from each site and at each risk level.

## 2_DataCombination

We amalgamated the cleaned data into one csv for future NLP analysis. After preprocessing and combination, we developed data graphics to help understand our data in preparation for NLP.

## 3_LengthOfMessageAnalysis

Looked at the message length both in total length and by length of individual words.
Plots were generated to visualize the differences in the lengths.
An lm and anova were fit to see if there were any statistically detectable differences.

## 4_NLP

## 5_TFIDF

## 6_TFIDF_postprocessing
