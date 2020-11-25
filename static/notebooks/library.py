import pandas as pd
import pickle

model_filenames = {
    "without-scaling" : "without-scaling",
    "with-scaling" : "with-scaling"
}

def import_music_df():
    df = pd.read_csv('../data/external/billboard_hits.csv')
    return df.drop(['Unnamed: 0'],axis=1)

def save_model(model, filename):
    """
    From https://stackoverflow.com/questions/54879434/how-to-use-the-pickle-to-save-sklearn-model
    """
    pickle.dump(model, open(f"../models/{filename}.pkl", "wb"))
    
def load_model(filename):
    """
    From https://stackoverflow.com/questions/54879434/how-to-use-the-pickle-to-save-sklearn-model
    """
    return pickle.load(open(f"../models/{filename}.pkl", "rb"))

def get_attributes(df):
    return df[['danceability', 'energy', 'key', 'loudness', "speechiness", 'acousticness', 'liveness', 'valence', 'tempo']]

def import_music_df_with_model(with_scaling = False):
    filename = model_filenames["without-scaling"]
    if(with_scaling):
        filename = model_filenames["with-scaling"]
    kmeans = load_model(filename)
    
    df = import_music_df()
    attribute_df = get_attributes(df)
    clusters = kmeans.predict(attribute_df)
    df["Cluster"] = clusters
    
    return df
    
    
    