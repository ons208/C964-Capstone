# initialize.py

# import
from train_model import train_machine_learning_model
from data_loader import load_data

# load data
df, education_mapping, occupation_dict = load_data('Salary_Data_Based_country_and_race.csv')

# Define X and y for train_machine_learning_model method
X = df.drop(columns=['Salary', 'Unnamed: 0', "Gender", "Race", "Country"])
y = df["Salary"]

# Train the machine learning model with loaded data
RF_model, X_train, y_train, mae, mse, rmse, y_test, y_pred, r_squared, adjusted_r_squared, mean_rmse = train_machine_learning_model(X, y)

# initialize_app method helps organize and collect all ML related variables into one easy to retrive location
def initialize_app(app):
    app.df = df
    app.education_mapping = education_mapping
    app.occupation_dict = occupation_dict
    app.RF_model = RF_model
    app.X_train = X_train
    app.y_train = y_train
    app.mae = mae
    app.mse = mse
    app.rmse = rmse
    app.mean_rmse = mean_rmse
    app.y_test = y_test
    app.y_pred = y_pred
    app.r_squared = r_squared
    app.adjusted_r_squared = adjusted_r_squared
    app.mean_rmse = mean_rmse
