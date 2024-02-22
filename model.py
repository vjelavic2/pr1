from flask import Flask, request, render_template
import urllib.request
import json
import os
import ssl
import matplotlib.pyplot as plt
import pandas as pd

app = Flask(__name__)


def allowSelfSignedHttps(allowed):
    # bypass the server certificate verification on client side
    if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
        ssl._create_default_https_context = ssl._create_unverified_context


allowSelfSignedHttps(True)



df = pd.read_csv('heart.csv')



@app.route('/')
def index():
    return render_template('page1.html')


@app.route('/predict', methods=['POST'])
def predict():
    age = request.form.get('age')
    sex = request.form.get ('sex')
    restingBP = request.form.get('restingBP')
    chestPainType = request.form.get('chestPainType')
    chestPainType = request.form.get('cholesterol')
    fastingBS = request.form.get('fastingBS')
    restingECG = request.form.get('restingECG')
    maxHR = request.form.get('maxHR')
    exerciseAngina = request.form.get('exerciseAngina')
    oldpeak = request.form.get('oldpeak')
    st_Slope = request.form.get('stSlope')

    data = {
        "Inputs": {
            "input1": [
                {
                   "Age": int(age),
                    "Sex": sex,
                    "RestingBP": int(restingBP),
                    "ChestPainType": chestPainType,
                    "Cholesterol": int(chestPainType),
                    "FastingBS": int(fastingBS),
                    "RestingECG": "Normal",
                    "MaxHR": int(maxHR),
                    "ExerciseAngina": exerciseAngina,
                    "Oldpeak": float(oldpeak),
                    "ST_Slope": st_Slope
                }
            ]
        },
        "GlobalParameters": {}
    }

    body = str.encode(json.dumps(data))

    url = 'http://9a5da49f-e77f-4aa9-a123-effc49910fc2.westeurope.azurecontainer.io/score'
    api_key = 'jHrVboewgsKDe6flrI1WKg5MeDh51tH1'
    headers = {'Content-Type': 'application/json',
               'Authorization': ('Bearer ' + api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)
        result = response.read()
        return render_template('page1.html', prediction=result)


    except urllib.error.HTTPError as error:
        return f"Error: {error}", 500



@app.route("/plot")
def graph():
    # Izdvajanje stupaca 'age' i 'heart_disease'
    
    srčane_bolesti = df[df['HeartDisease'] == 1]['Age']

    # Crtanje grafa
    plt.figure(figsize=(10, 6))
    plt.hist(srčane_bolesti, bins=20, color='#B8B7D8', edgecolor='black', alpha=0.7)
    plt.title('Raspodjela srčanih bolesti po dobi')
    plt.xlabel('Dob')
    plt.ylabel('Broj ljudi s srčanim bolestima')
    plt.grid(True)


    # Spremanje grafa u privremenu slikovnu datoteku
    graph_file = 'static/graph.png'
    plt.savefig(graph_file)
    
    return render_template("plot.html", graph=graph_file)



@app.route("/plot2")
def graph2():
    # Izdvajanje stupaca 'age' i 'heart_disease'
    
    srčane_bolesti = df[df['HeartDisease'] == 1]['Sex']

    # Crtanje grafa
    plt.figure(figsize=(10, 6))
    plt.hist(srčane_bolesti, bins=20, color='#B8B7D8', edgecolor='black', alpha=0.7)
    plt.title('Raspodjela srčanih bolesti po dobi')
    plt.xlabel('Spol')
    plt.ylabel('Broj ljudi s srčanim bolestima')
    plt.grid(True)


    # Spremanje grafa u privremenu slikovnu datoteku
    graph2_file = 'static/graph2.png'
    plt.savefig(graph2_file)
    
    return render_template("plot2.html", graph2=graph2_file)


@app.route("/plot3")
def graph3():
    
    srčane_bolesti = df[df['HeartDisease'] == 1]['Cholesterol']

    plt.figure(figsize=(10, 6))
    plt.hist(srčane_bolesti, bins=20, color='#B8B7D8', edgecolor='black', alpha=0.7)
    plt.title('Raspodjela srčanih bolesti po dobi')
    plt.xlabel('Kolesterol')
    plt.ylabel('Broj ljudi s srčanim bolestima')
    plt.grid(True)


    graph3_file = 'static/graph3.png'
    plt.savefig(graph3_file)
    
    return render_template("plot3.html", graph3=graph3_file)




if __name__ == '__main__':
    app.run(debug=True)
