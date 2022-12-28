from flask import Flask, request, render_template
import os
import bz2
import pickle
import _pickle as cPickle
import gdown

app = Flask(__name__)

#loaded_model = pickle.load(open("model/model.pkl", "rb"))
#loaded_vectorizer = pickle.load(open('model/vec.pkl', 'rb'))

def decompress_pickle(file):

    #os.chdir(directory)

    data = bz2.BZ2File(file, "rb")
    data = cPickle.load(data)

    #os.chdir("../")

    return data

url = 'https://drive.google.com/uc?id=1ZN7tJSS7el2APXwd2hjPqNznb_ewmhud'
loaded_vectorizer = '/tmp/vec.pbz2'
gdown.download(url, loaded_vectorizer, quiet=False)
loaded_vectorizer = decompress_pickle(loaded_vectorizer)

url = 'https://drive.google.com/uc?id=1zSbaGwyg0j6X3Q5IjVycUXJ8LolVqPeV'
loaded_model = '/tmp/model.pbz2'
gdown.download(url, loaded_model, quiet=False)
loaded_model = decompress_pickle(loaded_model)


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
    app.run(debug = True)