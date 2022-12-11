import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Loading the dataset
df = pd.read_csv('admission_predict.csv')

# print(df.head())
# print(df.tail())
print(df.columns)

# Returns basic statistics on numeric columns
# print(df.describe().T)

df = df.rename(columns={'GRE Score': 'GRE', 'TOEFL Score': 'TOEFL', 'LOR ': 'LOR', 'Chance of Admit ': 'Probability'})
print(df.columns)

def dis_GreScores():
    plt.hist(df['GRE'], rwidth=0.7)
    plt.title("Distribution of GRE Scores")
    plt.xlabel('GRE Scores')
    plt.ylabel('Count')
    plt.show()

def dis_TOEFL():
    plt.hist(df['TOEFL'], rwidth=0.7)
    plt.title('Distribution of TOEFL Scores')
    plt.xlabel('TOEFL Scores')
    plt.ylabel('Count')
    plt.show()

def dis_UniRating():
    plt.hist(df['University Rating'], rwidth=0.7)
    plt.title('Distribution of University Rating')
    plt.xlabel('University Rating')
    plt.ylabel('Count')
    plt.show()

# Removing the serial no, column
df.drop('Serial No.', axis='columns', inplace=True)
print(df.columns)

# Replacing the 0 values from ['GRE','TOEFL','University Rating','SOP','LOR','CGPA'] by NaN
df_copy = df.copy(deep=True)
df_copy[['GRE', 'TOEFL', 'University Rating', 'SOP', 'LOR', 'CGPA']] = df_copy[
    ['GRE', 'TOEFL', 'University Rating', 'SOP', 'LOR', 'CGPA']].replace(0, np.NaN)
df_copy.isnull().sum()

# Splitting the dataset in features and label
X = df_copy.drop('Probability', axis='columns')
y = df_copy['Probability']

# Using GridSearchCV to find the best algorithm for this problem
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

""""
# Creating a function to calculate best model for this problem
def find_best_model(X, y):
    models = {
        'linear_regression': {
            'model': LinearRegression(),
            'parameters': {
                'normalize': [True, False]
            }
        },

        'lasso': {
            'model': Lasso(),
            'parameters': {
                'alpha': [1, 2],
                'selection': ['random', 'cyclic']
            }
        },

        'svr': {
            'model': SVR(),
            'parameters': {
                'gamma': ['auto', 'scale']
            }
        },

        'decision_tree': {
            'model': DecisionTreeRegressor(),
            'parameters': {
                'criterion': ['mse', 'friedman_mse'],
                'splitter': ['best', 'random']
            }
        },

        'random_forest': {
            'model': RandomForestRegressor(criterion='mse'),
            'parameters': {
                'n_estimators': [5, 10, 15, 20]
            }
        },

        'knn': {
            'model': KNeighborsRegressor(algorithm='auto'),
            'parameters': {
                'n_neighbors': [2, 5, 10, 20]
            }
        }
    }

    scores = []
    for model_name, model_params in models.items():
        gs = GridSearchCV(model_params['model'], model_params['parameters'], cv=5, return_train_score=False)
        gs.fit(X, y)
        scores.append({
            'model': model_name,
            'best_parameters': gs.best_params_,
            'score': gs.best_score_
        })

    return pd.DataFrame(scores, columns=['model', 'best_parameters', 'score'])


print(find_best_model(X, y))

"""
# Using cross_val_score for gaining the highest accuracy
from sklearn.model_selection import cross_val_score
scores = cross_val_score(LinearRegression(normalize=True), X, y, cv=5)
print('Highest Accuracy : {}%'.format(round(sum(scores)*100/len(scores)), 3))

# Splitting the dataset into train and test samples
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=5)
print(len(X_train), len(X_test))


# Creating Linear Regression Model
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
model = make_pipeline(StandardScaler(with_mean=False), LinearRegression())
model.fit(X_train, y_train)
model.score(X_test, y_test)

# Prediction 1
# Input in the form : GRE, TOEFL, University Rating, SOP, LOR, CGPA, Research
print('Chance of getting into UCLA is {}%'.format(round(model.predict([[337, 118, 4, 4.5, 4.5, 9.65, 0]])[0]*100, 3)))


# Prediction 2
# Input in the form : GRE, TOEFL, University Rating, SOP, LOR, CGPA, Research
# print('Chance of getting into UCLA is {}%'.format(round(model.predict([[320, 113, 2, 2.0, 2.5, 8.64, 1]])[0]*100, 3)))
print("mc",round(model.predict([[340, 120, 4, 4,4, 9.6, 1]])[0]*100, 3))