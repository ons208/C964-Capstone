# app.py file

# import
import os
from flask import Flask, render_template, request, jsonify
import pandas as pd


# Imports from initialize and train_model
from data_loader import load_data
from train_model import train_machine_learning_model
from initialize import initialize_app, education_mapping, occupation_dict

# create Flask app
app = Flask(__name__)

# Configure path for static files
app.static_url_path = '/static'
app.static_folder = 'static'

# Initialize app
initialize_app(app)


# Define route for main webpage, handles both GET/POST requests
@app.route('/', methods=['GET', 'POST'])
def predict_salary():
    # POST requests logic
    if request.method == 'POST':
        user_data = request.json
        selected_metric = user_data.get('selected_metric', 'mae')
        # Access data from initialize app
        df = app.df
        # Apply the data mappings
        user_data['education'] = education_mapping[user_data['education']]
        user_data['occupation'] = occupation_dict[user_data['occupation']]
        # remove selected metric from the user data, not needed for ML model
        del user_data['selected_metric']
        # create dataframe
        new_data_df = pd.DataFrame([user_data])

        # Import ML model, training data and metrics
        RF_model = app.RF_model
        X_train = app.X_train
        y_train = app.y_train
        mae = app.mae
        mse = app.mse
        rmse = app.rmse
        mean_rmse = app.mean_rmse

        # Define a mapping for metrics
        metric_mapping = {
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mean_rmse': mean_rmse
        }
        # Retreve metric value from selected metric
        metric_value = metric_mapping.get(selected_metric, mae)
        # Predict salary
        predicted_salary = RF_model.predict(new_data_df)[0]
        # Calculate the lower and upper bounds
        predicted_lower_bound = predicted_salary - metric_value
        predicted_upper_bound = predicted_salary + metric_value
        # Convert values to Python floats and round to 2 decimal places
        predicted_salary = round(float(predicted_salary), 2)
        predicted_lower_bound = round(float(predicted_lower_bound), 2)
        predicted_upper_bound = round(float(predicted_upper_bound), 2)

        # Create JSON response to send to frontend
        response_data = {
            "predicted_salary": predicted_salary,
            "lower_bound": predicted_lower_bound,
            "upper_bound": predicted_upper_bound,
        }

        # Return the JSON response
        return jsonify(response_data)
    else:
        # GET request logic, render template with initial data
        return render_template('index.html',
                               occupation_dict=occupation_dict, predicted_salary=None)


# Define route for data page
@app.route('/data', methods=['GET'])
def data_page():
    return render_template('data.html')


# Define route for generating accuracy metrics
@app.route('/accuracy_metrics', methods=['GET'])
def get_accuracy_metrics():
    # Import metrics from initialize app
    mae = app.mae
    mse = app.mse
    rmse = app.rmse
    mean_rmse = app.mean_rmse
    r_squared = app.r_squared
    adjusted_r_squared = app.adjusted_r_squared

    # Create a dictionary for the accuracy metrics
    accuracy_metrics = {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'mean_rmse': mean_rmse,
        'r_squared': r_squared,
        'adjusted_r_squared': adjusted_r_squared
    }
    # Send acurracy metrics back to Frontend
    return jsonify(accuracy_metrics)


# Running the flask app if script is executed directly
if __name__ == '__main__':
    # Load the data
    df, education_mapping, occupation_dict = load_data('Salary_Data_Based_country_and_race.csv')
    # Extract features (X) and target (y)
    X = df.drop(columns=['Salary', 'Unnamed: 0', "Gender", "Race", "Country"])
    y = df["Salary"]

    # Train the machine learning model with loaded data
    RF_model, X_train, y_train, mae, mse, rmse, y_test, y_pred, r_squared, adjusted_r_squared, mean_rmse = train_machine_learning_model(
        X, y)

    # Initialize the Flask app with data and trained model
    initialize_app(app)

    os.environ['PORT'] = '10000'
    # Recommended instructions from render.com
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 10000)))
