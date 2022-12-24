from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Dataset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    classification = db.Column(db.Integer, default=0)

@app.route('/')  
def main():  
    return render_template("index.html")  
	
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    save_dir = 'datasets/'

    if request.method == 'POST':
        f = request.files['file']
        # filename = save_dir + secure_filename(f.filename)
        filename = save_dir + f.filename
        f.save(filename)

        # add dataset to db
        new_dataset = Dataset(filename=filename)
        try:
            db.session.add(new_dataset)
            db.session.commit()
            return redirect(url_for('.display_data'))
        except:
            return "There was an issue adding dataset to db"

@app.route('/display_data')
def display_data():
    # get dataset from db
    current_dataset = Dataset.query.order_by(Dataset.id.desc()).first()

    # reading from pandas
    df = pd.read_csv(current_dataset.filename)

    # metadata df
    buf = io.StringIO()
    df.info(buf=buf)
    s = buf.getvalue()
    lines = [line.split() for line in s.splitlines()[3:-2]]
    metadata_df = pd.DataFrame(lines[2:], columns=lines[0])

    # prevent displaying entire dataset
    df = df.head()
    return render_template("display_data.html", 
                            column_names=df.columns.values, 
                            row_data=list(df.values.tolist()), 
                            zip=zip,
                            filename=current_dataset.filename.split('/')[-1],
                            
                            # metadata_df
                            metadata_column_names=metadata_df.columns.values, 
                            metadata_row_data=list(metadata_df.values.tolist()), 
                            
                            )

if __name__ == '__main__':
    app.run(debug = True)