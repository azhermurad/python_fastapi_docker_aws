import pickle

# load the model
with open("model/model.pkl", "rb") as f:
    model = pickle.load(f)
    
def load_model(df):
    clicked_on_ad = model.predict(df)[0]
    res = "Clicked" if clicked_on_ad else "Not Clicked"
    return res