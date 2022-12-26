from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import io
import eda_draw
import os

app = Flask(__name__)
app.secret_key = "super secret key"

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# eda plots save folder
EDA_FOLDER = os.path.join('static', 'eda')
app.config['UPLOAD_FOLDER'] = EDA_FOLDER

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

@app.route('/eda', methods = ['GET', 'POST'])
def eda():
    if request.method == 'POST':
        columns=request.form.getlist('columns')
        label=request.form['label']

        # prevent label from appearing twice
        if label in columns:
            columns.remove(label)

        # get dataset from db
        current_dataset = Dataset.query.order_by(Dataset.id.desc()).first()

        # reading from pandas
        df = pd.read_csv(current_dataset.filename)


        # filter out columns
        df = df[columns + [label]]
        describe = df.describe().applymap('{:,.2f}'.format)
        operation = list(describe.index)
        describe.insert(loc=0, column='', value=operation)

        # df to use for feature selection
        # df_feature = df_feature[columns]
        feature_dict = {"Features":columns}
        df_feature = pd.DataFrame.from_dict(feature_dict)


        # clear eda folder first
        for file in os.listdir('static/eda'):
            os.remove('static/eda/'+file)

        # draw and save the graphs
        eda_draw.draw_all(df)

        # distplot filenames
        distplots = [i for i in os.listdir('static/eda') if 'distplot' in i]
        temp = []
        for plot in distplots: # add full filepath
            temp.append(os.path.join(app.config['UPLOAD_FOLDER'], plot))
        distplots = temp

        return render_template("eda.html", 
                                columns=request.form.getlist('columns'),
                                label=request.form['label'],

                                # df.describe
                                column_names=describe.columns.values, 
                                row_data=list(describe.values.tolist()), 
                                zip=zip,
                                link_column='',
                                
                                correlation_plot=os.path.join(app.config['UPLOAD_FOLDER'], 'correlation.png'),

                                distplots = distplots,

                                # metadata_df
                                df_feature_column_names=df_feature.columns.values, 
                                df_feature_row_data=list(df_feature.values.tolist()), 

                                )

@app.route('/train', methods = ['GET', 'POST'])
def train():
    if request.method == 'POST':
        columns=request.form.getlist('columns')
        time_left_for_this_task=request.form['time_left_for_this_task']
        per_run_time_limit=request.form['per_run_time_limit']

        return render_template('train.html',
                                columns=columns,
                                time_left_for_this_task=time_left_for_this_task,
                                per_run_time_limit=per_run_time_limit
        )


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