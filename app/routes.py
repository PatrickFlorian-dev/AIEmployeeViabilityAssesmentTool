from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields, Namespace
from app.data_generator import generate_employees, reset_database
from app.database import Session
from app.database import session_scope
from app.models import Base 

app = Flask(__name__)

api = Api(app, 
    version='1.0', 
    title='Employee Success Prediction API',
    description='AI/ML Engine for employee success evaluation',
    doc='/')

ai_ns = Namespace('AI Resources', 
    path='/api',
    description='AI model training and evaluation operations')

# Define request/response models
model_run_model = api.model('ModelRun', {
    'model_type': fields.String(required=True),
    'hyperparameters': fields.Raw(required=True),
    'metrics': fields.Raw(required=True)
})

evaluation_model = api.model('Evaluation', {
    'employee_id': fields.Integer(required=True),
    'success_score': fields.Float(required=True)
})

error_model = api.model('Error', {
    'error': fields.String(description='Error message'),
    'details': fields.String(description='Additional error details')
})

@ai_ns.route('/train')
class TrainModel(Resource):
    @ai_ns.doc('train_model', 
              params={'epochs': 'Number of training epochs'},
              responses={200: 'Success', 500: 'Training failed'})
    @ai_ns.expect(api.model('TrainParams', {'epochs': fields.Integer}))
    def post(self):
        try:
            """Train the prediction model"""
            epochs = request.json.get('epochs', 50)
            model = SuccessPredictor()
            metrics = model.train(epochs=epochs)
            
            run = ModelRun(
                model_type="SequentialNN",
                hyperparameters={"epochs": epochs, "layers": [64,32]},
                metrics=metrics
            )
            session = Session()
            session.add(run)
            session.commit()
            
            return metrics, 200
        except ValueError as e:
            ai_ns.abort(400, str(e))
        except SQLAlchemyError as e:
            app.logger.error(f"Database error: {str(e)}")
            ai_ns.abort(500, "Failed to save training results")
        except Exception as e:
            app.logger.error(f"Training failed: {str(e)}")
            ai_ns.abort(500, "Model training failed")

@ai_ns.route('/evaluate')
class EvaluateEmployee(Resource):
    @ai_ns.doc('evaluate_employee',
              responses={200: 'Success', 400: 'Invalid input'})
    @ai_ns.expect(api.model('EmployeeData', {
        'id': fields.Integer(required=True),
        'features': fields.Raw(required=True)
    }))
    @ai_ns.marshal_with(evaluation_model)
    def post(self):
        """Evaluate an employee's success potential"""
        try:
            data = request.get_json()
            if not data or 'employee_id' not in data or 'features' not in data:
                raise ValueError("Missing required fields in request")
            
            employee_id = data['employee_id']
            features = data['features']
            
            # Validate employee exists
            with session_scope() as session:
                employee = session.query(Employee).get(employee_id)
                if not employee:
                    ai_ns.abort(404, "Employee not found")
            
            # Get prediction
            model = SuccessPredictor()
            prediction = model.predict(features)
            
            # Save evaluation
            with session_scope() as session:
                latest_run = session.query(ModelRun).order_by(ModelRun.id.desc()).first()
                evaluation = ModelEvaluation(
                    employee_id=employee_id,
                    model_run_id=latest_run.id,
                    success_score=prediction['score'],
                    confidence=prediction['confidence']
                )
                session.add(evaluation)
            
            return {
                'employee_id': employee_id,
                'success_score': prediction['score'],
                'confidence': prediction['confidence']
            }, 200
            
        except ValueError as e:
            ai_ns.abort(400, str(e))
        except SQLAlchemyError as e:
            app.logger.error(f"Database error: {str(e)}")
            ai_ns.abort(500, "Failed to save evaluation")
        except Exception as e:
            app.logger.error(f"Evaluation failed: {str(e)}")
            ai_ns.abort(500, "Prediction failed")

@ai_ns.route('/models/<string:version>')
class ModelVersion(Resource):
    @ai_ns.doc('switch_model',
              params={'version': 'Model version identifier'},
              responses={200: 'Model switched', 404: 'Model not found'})
    def post(self, version):
        """Switch active model version"""
        global active_model
        s3.download_file('your-bucket', f'models/v{version}.h5', 'current_model.h5')
        active_model = tf.keras.models.load_model('current_model.h5')
        return {"status": f"Model {version} loaded"}, 200

@ai_ns.route('/models/retrain')
class ModelRetrain(Resource):
    @ai_ns.doc('retrain_model',
              params={'epochs': 'Number of training epochs', 'fine_tune': 'Fine-tune existing model'},
              responses={200: 'Retrained successfully', 500: 'Retraining failed'})
    @ai_ns.expect(api.model('RetrainParams', {
        'epochs': fields.Integer,
        'fine_tune': fields.Boolean
    }))
    def post(self):
        """Retrain model with new parameters"""
        epochs = request.json.get('epochs', 50)
        fine_tune = request.json.get('fine_tune', False)
        
        model = SuccessPredictor()
        if fine_tune:
            model = fine_tune_model(model)
        
        metrics = model.train(epochs=epochs)
        model.save_model_to_s3(version=datetime.now().strftime("%Y%m%d%H%M"))
        
        return metrics, 200

api.add_namespace(ai_ns)

@app.before_request
def initialize_app():
    if not hasattr(app, 'initialized'):
        try:
            from app.database import engine
            Base.metadata.create_all(engine)
            generate_employees()
            app.initialized = True
        except Exception as e:
            app.logger.error(f"Initialization failed: {str(e)}")
            raise

if __name__ == '__main__':
    app.run(debug=True)