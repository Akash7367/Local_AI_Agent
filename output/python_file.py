import pandas as pd
import numpy as np

# Generate random data
np.random.seed(0)
data = {
    'Name': ['Tom', 'Nick', 'John', 'Peter', 'Clark'],
    'Age': np.random.randint(18, 25, 5),
    'CGPA': np.random.uniform(7, 10, 5)
}

# Create DataFrame
df = pd.DataFrame(data)

# Add 'Placed' column
df['Placed'] = np.random.choice([True, False], 5)

# Print DataFrame
print(df)

# Function to predict placement
def predict_placement(name, age, cgpa):
    # Generate random prediction
    prediction = np.random.choice([True, False])
    return prediction

# Test the function
print(predict_placement('John', 22, 8.5))