from flask import Flask, request, render_template
import os
import bz2
import pickle
import _pickle as cPickle

app = Flask(__name__)

#loaded_model = pickle.load(open("model/model.pkl", "rb"))
#loaded_vectorizer = pickle.load(open('model/vec.pkl', 'rb'))

def decompress_pickle(directory, file):

    os.chdir(directory)

    data = bz2.BZ2File(file, "rb")
    data = cPickle.load(data)

    os.chdir("../")

    return data

loaded_model = decompress_pickle("model", "model.pbz2")
loaded_vectorizer = decompress_pickle("vectorizer", "vec.pbz2")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/classify", methods = ["GET", "POST"])
def classify():
    if request.method == "POST":

        prediction = loaded_model.predict(loaded_vectorizer.transform([x for x in request.form.values()]))[0]
        output = "POSITIVE" if prediction == 1 else "NEGATIVE"

        return render_template("index.html", prediction_text = f"The Entered Movie Review is {output}")

if __name__ == "__main__":
    app.run()