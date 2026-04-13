import pandas as pd
import numpy as np

# Generate random data
np.random.seed(0)
data = {
    'Name': ['John', 'Anna', 'Peter', 'Linda', 'Phil', 'Liz', 'Tom', 'Lily', 'Jack', 'Rose'],
    'Age': np.random.randint(18, 25, 10),
    'CGPA': np.random.uniform(7, 10, 10)
}
df = pd.DataFrame(data)

# Create a new column 'Placed' with random values
df['Placed'] = np.random.choice([0, 1], 10)

# Print the data
print(df)

# Define a function to predict placement
def predict_placement(name, age, cgpa):
    # Create a new row with the given values
    new_row = pd.DataFrame({'Name': [name], 'Age': [age], 'CGPA': [cgpa]})
    
    # Merge the new row with the original data
    merged_df = pd.concat([df, new_row], ignore_index=True)
    
    # Predict placement based on the model (for simplicity, we'll use a basic threshold)
    threshold = df['CGPA'].mean()
    if merged_df.loc[merged_df.shape[0] - 1, 'CGPA'] > threshold:
        return 'Placed'
    else:
        return 'Not Placed'

# Test the function
print(predict_placement('John Doe', 22, 8.5))