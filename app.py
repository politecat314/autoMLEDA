from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
app = Flask(__name__)

@app.route('/')  
def main():  
    return render_template("index.html")  
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    save_dir = 'datasets/'

    if request.method == 'POST':
        f = request.files['file']
        filename = save_dir + secure_filename(f.filename)
        f.save(filename)
        return render_template('index.html',  filename=filename)


if __name__ == '__main__':
    app.run(debug = True)


# exit()

# from distutils.log import debug
# from fileinput import filename
# from flask import *
# import pandas as pd
# import numpy as np

# app = Flask(__name__)  
  
# @app.route('/')  
# def main():  
#     return render_template("index.html")  
  
# @app.route('/upload', methods = ['POST'])  
# def upload():  
#     if request.method == 'POST':  
#         f = request.files['file']
        
#         filename = 'datasets/' + f.filename
#         f.save(filename)
#         df = pd.read_csv(filename)
#         df = df.head()

#         return render_template('display.html',  tables=[df.to_html(classes='data')], titles=df.columns.values)  



# if __name__ == '__main__': 
#     app.run(debug=True)