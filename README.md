# UMN-Data_Analytics-Project_03
This repository contains Project #3 for the University of Minnesota's Data Analytics Bootcamp.

# Billboard's Top 100 Songs Machine Learning Model
Aaron Wollman, Kelsey Richardson Blackwell, Will Huang

# Project Proposal
Link to Project Proposal

# Project Summary
We created a k-means model on billboard's top 100 songs from the 1960s to 2019. We ended up using non-scaled data to train the data with 3 clusters. After creating the model, we ran the model on our dataset and explored how the clusters related to other dataset items. This website will take you from modeling to what we found while graphing the clusters.

## K-Means Model
We had a clean dataset from <<Project 1 link>>, so we did not have to spend a lot of time on cleaning up. We first looked for the ideal value of k by creating an elbow graph. 

We trained our model using non-scaled data which gave us a Silouetter Score of <<>>. The Silouetter Score is between -1 ot 1. If the value is closer to 1, the clusters are more dense and separated from the other clusters. We then trained our mdel using scaled data which gave us a silouetter Score of <<>>.

We saved both models but when we moved forward in applying our model to our data, we used the "without-scaling" model.

## Running Model
In library.py we created a number of functions. The import_music_df_with_model function 


# Sources
Dataset from <<Kaggle link>>
