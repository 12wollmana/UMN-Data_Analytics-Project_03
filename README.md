# Billboard's Top 100 Songs Machine Learning Model
Aaron Wollman, Kelsey Richardson Blackwell, Will Huang

## Project Proposal
[Project Proposal](https://docs.google.com/document/d/18lH5qNpat62voNdJxxNazMAmrfGYoD7WSlTHtPxM6YI/edit)

## Project Summary
We used k-means, an unsupervised machine learning algorithm, on the billboard's top 100 songs from the 1960s to the late 2010's to classify the songs based on attributes from Spotify. We ended up using non-scaled data to categorize the thousands of songs into 3 clusters. After creating and running the k-means clustering algorithm, we explored how the clusters related to the songs' attributes. 

### K-Means Model
We had a clean dataset from [Project 1](https://github.com/12wollmana/UMN-Data_Analytics-Project_01), so we did not have to spend a lot of time on cleaning it. We first looked for the ideal value of k (clusters) with an elbow graph. 

We created a model with scaled and non-scaled data. We looked at the Silouetter Score for each model and decided to use the non-scaled. The Silouetter Score is between -1 ot 1. If the value is closer to 1, the clusters are more dense and separated from the other clusters. 

In library.py there are a number of functions, including import_music_df_with_model function that removes dublicates and imports the data into our jupyter notebooks.

### Graphing Clusters & Attributes
We plotted a number of graphs to see how the clusters were influenced by the attributes, decades, and placements. 

 ![](static/images/plots/attributes/danceability_percent.png)\
 
 ![](static/images/plots/top-songs/valence.png)  ![](static/images/plots/decades/line/energy.png)

### Website
We used [heroku](https://umn-data-analytics-p03-t01.herokuapp.com/) to host our report and vizualizations.

### Conclusion
The clusters were formed by the attribute tempo.

#### Sources
[Dataset](https://github.com/fortyTwo102/hitpredictor-decade-util/tree/master/Database)\
[Silouetter Score](https://dzone.com/articles/kmeans-silhouette-score-explained-with-python-exam)\
[Elbow Graph](https://predictivehacks.com/k-means-elbow-method-code-for-python/)
