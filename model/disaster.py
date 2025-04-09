import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import OneHotEncoder
import random

class DisasterModel:
    _instance = None

    def __init__(self):
        self.model = None
        self.dt = None
        self.encoder = OneHotEncoder(handle_unknown='ignore')
        self.features = ['magnitude_or_intensity', 'distance_to_disaster', 'alert_time', 
                         'evacuation_available', 'shelter_nearby']
        self.target = 'survived'
        self._clean()
        self._train()

    def _clean(self):
        # Simulated San Diego disaster survival dataset
        n = 500
        df = pd.DataFrame({
            'disaster_type': np.random.choice(['earthquake', 'wildfire', 'tsunami'], n),
            'magnitude_or_intensity': np.random.uniform(4, 10, n),
            'distance_to_disaster': np.random.uniform(0.5, 50, n),
            'alert_time': np.random.uniform(0, 30, n),
            'evacuation_available': np.random.choice([0, 1], n),
            'shelter_nearby': np.random.choice([0, 1], n),
        })

        # Survival logic for simulation
        df['survived'] = (
            (df['magnitude_or_intensity'] < 7) &
            (df['distance_to_disaster'] > 10) &
            (df['alert_time'] > 10) &
            (df['evacuation_available'] == 1) &
            (df['shelter_nearby'] == 1)
        ).astype(int)

        # One-hot encode disaster_type
        onehot = self.encoder.fit_transform(df[['disaster_type']]).toarray()
        cols = ['disaster_type_' + val for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)

        df = pd.concat([df, onehot_df], axis=1)
        df.drop(columns=['disaster_type'], inplace=True)

        self.features.extend(cols)
        self.df = df

    def _train(self):
        X = self.df[self.features]
        y = self.df[self.target]
        self.model = LogisticRegression(max_iter=1000)
        self.model.fit(X, y)
        self.dt = DecisionTreeClassifier()
        self.dt.fit(X, y)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def predict(self, input_data):
        df = pd.DataFrame(input_data, index=[0])
        df['evacuation_available'] = int(df['evacuation_available'])
        df['shelter_nearby'] = int(df['shelter_nearby'])

        # One-hot encode disaster_type
        onehot = self.encoder.transform(df[['disaster_type']]).toarray()
        cols = ['disaster_type_' + val for val in self.encoder.categories_[0]]
        onehot_df = pd.DataFrame(onehot, columns=cols)

        df = pd.concat([df.drop(columns=['disaster_type']), onehot_df], axis=1)

        # Fill missing columns (if any)
        for col in self.features:
            if col not in df.columns:
                df[col] = 0
        df = df[self.features]

        die, survive = np.squeeze(self.model.predict_proba(df))
        return {'die': round(die, 4), 'survive': round(survive, 4)}

    def feature_weights(self):
        importances = self.dt.feature_importances_
        return {feature: importance for feature, importance in zip(self.features, importances)}

def initDisaster():
    DisasterModel.get_instance()

def testDisaster():
    print("Test DisasterModel Prediction")
    disaster_data = {
        'disaster_type': 'earthquake',
        'magnitude_or_intensity': 7.8,
        'distance_to_disaster': 3,
        'alert_time': 2,
        'evacuation_available': 0,
        'shelter_nearby': 0
    }

    model = DisasterModel.get_instance()
    result = model.predict(disaster_data)
    print("Prediction:", result)
    weights = model.feature_weights()
    print("Feature importances:", weights)

if __name__ == "__main__":
    testDisaster()