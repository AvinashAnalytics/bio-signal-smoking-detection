import pandas as pd
import os
from sklearn.preprocessing import LabelEncoder

def preprocess_data(input_file: str, output_file: str):
    # Load the dataset
    df = pd.read_csv(input_file)
    print("Original Data:")
    print(df.head())

    # Remove irrelevant columns (ignore errors if missing)
    df = df.drop(columns=['ID', 'oral'], errors='ignore')

    # Check for missing values
    print("\nMissing Values Before Handling:")
    print(df.isnull().sum())

    # Fill missing values with median for numeric columns
    df.fillna(df.median(numeric_only=True), inplace=True)

    # Encode categorical columns safely
    le = LabelEncoder()
    if 'gender' in df.columns:
        df['gender'] = le.fit_transform(df['gender'])

    # Perform One-Hot Encoding for categorical features
    categorical_features = ['tartar', 'dental caries']
    df = pd.get_dummies(df, columns=categorical_features, drop_first=True)

    print("\nMissing Values After Handling:")
    print(df.isnull().sum())

    # Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"Cleaned data saved to {output_file}")

if __name__ == "__main__":
    input_path = os.path.join('data', 'smoking.csv')  # Cross-platform path handling
    output_path = 'cleaned_smoking_data.csv'
    
    preprocess_data(input_path, output_path)
