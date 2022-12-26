import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# import plotly.express as px
# from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
# from yellowbrick.classifier import ConfusionMatrix
# from sklearn.tree import DecisionTreeClassifier
# from sklearn.metrics import r2_score
# from sklearn.metrics import mean_absolute_error, mean_squared_error
# from sklearn.model_selection import GridSearchCV


# correlation heatmap
def correlation_heatmap(df, path):
    correlation = df.corr().round(2)
    plt.figure(figsize = (14,7))
    correlation_plot = sns.heatmap(correlation, annot = True, cmap = 'YlOrBr')

    # saving figure
    fig = correlation_plot.get_figure()
    fig.savefig(f"{path}/correlation.png")

# for continuous variables
def dist_plot(df, column, path, index=0):
    plt.figure(figsize = (5,4))
    sns.set(color_codes = True)

    fig = sns.distplot(df[column], kde = False).get_figure()
    fig.savefig(f"{path}/distplot_{index}_{column}.png")



def draw_all(df):
    """
    makes the call to all the functions to generate and save plots
    """
    path = "static/eda" # savepath of the plots
    columns = list(df)

    correlation_heatmap(df, path)

    for index, col in enumerate(columns):
        dist_plot(df, col, path, index=index)