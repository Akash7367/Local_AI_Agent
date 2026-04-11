import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Generate random data
np.random.seed(0)
data = pd.DataFrame({
    'Name': ['John', 'Anna', 'Peter', 'Linda', 'Phil', 'Liz', 'Tom', 'Lily', 'Jack', 'Rose'] * 10,
    'CGPA': np.random.uniform(0, 10, 100)
})
data['Placed'] = np.random.choice([0, 1], 100)

# Split data into features and target
X = data[['Name', 'CGPA']]
y = data['Placed']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train a random forest classifier
clf = RandomForestClassifier()
cf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Print the first 10 rows of the data
print(data.head())

# Print the accuracy of the model
print('Accuracy:', clf.score(X_test, y_test))