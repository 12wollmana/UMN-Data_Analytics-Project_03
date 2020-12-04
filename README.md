# UMN-Data_Analytics-Project_03
This repository contains Project #3 for the University of Minnesota's Data Analytics Bootcamp.

# Billboard's Top 100 Songs Machine Learning Model
Aaron Wollman, Kelsey Richardson Blackwell, Will Huang

# Project Proposal
Link to Project Proposal

# Project Summary
We created a k-means model on billboard's top 100 songs from the 1960s to 2019, looks at attributes from Spotify. We ended up using non-scaled data to categorize the thousands of songs into 3 clusters. After creating and running the algorithm, we explored how the clusters related to the songs' attributes. This website will take you from modeling to what we found while graphing the clusters.

## K-Means Model
We had a clean dataset from https://github.com/12wollmana/UMN-Data_Analytics-Project_01, so we did not have to spend a lot of time on cleaning up our data. We first looked for the ideal value of k by creating an elbow graph. 

We trained our model using non-scaled data which gave us a Silouetter Score of <<>>. The Silouetter Score is between -1 ot 1. If the value is closer to 1, the clusters are more dense and separated from the other clusters. We then trained our mdel using scaled data which gave us a silouetter Score of <<>>.

We saved both models but when we moved forward in applying our model to our data, we used the "without-scaling" model.

## Running Model
In library.py we created a number of functions. The import_music_df_with_model function 


# Sources
Dataset from https://github.com/fortyTwo102/hitpredictor-decade-util/tree/master/Database
Silouetter Score code https://dzone.com/articles/kmeans-silhouette-score-explained-with-python-exam
Elbow Graph https://predictivehacks.com/k-means-elbow-method-code-for-python/
