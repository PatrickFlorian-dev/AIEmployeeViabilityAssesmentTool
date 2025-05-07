import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sqlalchemy import create_engine
import pandas as pd
import os
from datetime import datetime
import boto3
from botocore.client import Config
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from app.models import Employee, ModelRun
import logging

logger = logging.getLogger(__name__)

class SuccessPredictor:
    def __init__(self):
        self.model = self.build_model()
        self.scaler = StandardScaler()

    def build_model(self, layers=[64, 32]):
        try:
            model = tf.keras.Sequential([
                tf.keras.layers.Dense(layers[0], activation='relu', input_shape=(input_dim,)),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Dense(layers[1], activation='relu'),
                tf.keras.layers.Dense(1, activation='linear')  # Output 1-10 score
            ])
            model.compile(optimizer='adam', loss='mse', metrics=['mae'])
            return model
        except Exception as e:
            logger.error(f"Model build failed: {str(e)}")
            raise

    def preprocess_data(self):
        try:
            with session_scope() as session:
                query = session.query(Employee).statement
                df = pd.read_sql(query, session.bind)
            
            # Feature engineering
            df['age'] = (datetime.now() - pd.to_datetime(df['dob'])).dt.days // 365
            df = pd.get_dummies(df, columns=[
                'role', 
                'has_leadership_experience',
                'military_experience',
                'volunteer_experience'
            ])
            
            if 'success_score' not in df.columns:
                raise ValueError("Missing success_score in dataset")
            
            X = df.drop(['id', 'success_score', 'dob'], axis=1, errors='ignore')
            y = df['success_score']
            
            # Ensure consistent input dimension
            self.input_dim = X.shape[1]
            return X, y
            
        except Exception as e:
            logger.error(f"Data preprocessing failed: {str(e)}")
            raise

    def train(self, epochs=50, batch_size=32):
        try:
            X, y = self.preprocess_data()
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            X_train = self.scaler.fit_transform(X_train)
            X_test = self.scaler.transform(X_test)
            
            history = self.model.fit(
                X_train, y_train,
                validation_data=(X_test, y_test),
                epochs=epochs,
                batch_size=32,
                verbose=0
            )
            
            return {
                'accuracy': history.history['accuracy'][-1],
                'val_accuracy': history.history['val_accuracy'][-1],
                'loss': history.history['loss'][-1],
                'val_loss': history.history['val_loss'][-1]
            }
            
        except Exception as e:
            logger.error(f"Training failed: {str(e)}")
            raise
    
    def save_model_to_s3(self, version):
        try:
            s3 = boto3.client('s3',
                endpoint_url=os.getenv('AWS_ENDPOINT'),
                aws_access_key_id=os.getenv('AWS_KEY'),
                aws_secret_access_key=os.getenv('AWS_SECRET'),
                config=Config(signature_version='s3v4')  # Required for MinIO
            )
            
            # Create bucket if it doesn't exist
            try:
                s3.create_bucket(Bucket='models')
            except s3.exceptions.BucketAlreadyOwnedByYou:
                pass
            
            # Upload model
            buffer = BytesIO()
            tf.keras.models.save_model(self.model, buffer)
            buffer.seek(0)
            s3.upload_fileobj(buffer, 'models', f'v{version}.h5')
        except Exception as e:
            logger.error(f"Model save failed: {str(e)}")
            raise

    def predict(self, features):
            """Make prediction for a single employee"""
            try:
                # Convert features to numpy array and scale
                features_array = np.array([list(features.values())])
                scaled_features = self.scaler.transform(features_array)
                
                prediction = self.model.predict(scaled_features)
                confidence = prediction[0][0]
                
                return {
                    'score': float(confidence * 10),  # Scale to 1-10
                    'confidence': float(confidence)
                }
                
            except Exception as e:
                logger.error(f"Prediction failed: {str(e)}")
                raise

def cluster_employees():
    engine = create_engine(os.getenv('DATABASE_URL'))
    df = pd.read_sql("SELECT * FROM employees", engine)
    
    # Select features
    features = df[[
        'years_experience', 'different_industries_worked_in',
        'has_leadership_experience', 'largest_company_size_worked_at'
    ]]
    
    # Cluster into 10 groups (1-10 scores)
    kmeans = KMeans(n_clusters=10)
    df['success_score'] = kmeans.fit_predict(StandardScaler().fit_transform(features)) + 1
    
    # Save back to DB
    df[['id', 'success_score']].to_sql('employees', engine, if_exists='append')