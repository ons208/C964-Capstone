# data_loader.py

# import libraries
import pandas as pd


# load_data method loads data and performs preprocessing operations(cleaning up incomplete data,
# formatting features and returns the data as a dataframe
def load_data(file_path):
    # Read File
    df = pd.read_csv(file_path)

    # Renaming columns
    df.rename(columns={'Education Level': 'education', 'Job Title': 'occupation', 'Years of Experience': 'years'},
              inplace=True)

    # Handle data with missing values
    df = df.dropna()

    # Create mappings for education levels
    education_mapping = {
        "High School": 0,
        "Bachelor's Degree": 1,
        "Bachelor's": 1,
        "Master's Degree": 2,
        "Master's": 2,
        "PhD": 3,
        "phD": 3
    }

    # Map the categorical columns consistently
    df['education'] = df['education'].map(education_mapping)

    # Map the occupation column consistently
    occupation_mapping = df['occupation'].value_counts().to_dict()
    df['occupation'] = df['occupation'].map(occupation_mapping)

    # Return the DataFrame and the variables
    return df, education_mapping, occupation_mapping
