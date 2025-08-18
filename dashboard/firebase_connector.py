# dashboard/firebase_connector.py
import firebase_admin
from firebase_admin import credentials, db
import logging
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, filename='firebase.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize Firebase app
cred = credentials.Certificate(r'D:\1.0\dashboard\irrigateiq-9fe90-firebase-adminsdk-fbsvc-915a202ede.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://irrigateiq-9fe90-default-rtdb.firebaseio.com/'
})

def get_latest_sensor_data():
    """Fetch the latest sensor data from Firebase"""
    try:
        logger.debug("Attempting to fetch sensor data from Firebase")
        ref = db.reference('SensorData')  # Update to exact case-sensitive path (e.g., sensors/latest, SENSOR_DATA)
        sensor_data = ref.get()
        logger.debug(f"Raw sensor data: {sensor_data}")
        
        if sensor_data is None:
            logger.warning("No data found at 'SensorData' reference")
            return {
                'sensor_id': f'sensor_{int(time.time())}',
                'temperature': 0,
                'humidity': 0,
                'soil_moisture': 0
            }
        
        # Normalize data to expected format
        if isinstance(sensor_data, dict):
            normalized_data = {
                'sensor_id': sensor_data.get('sensor_id', sensor_data.get('id', f'sensor_{int(time.time())}')),
                'temperature': sensor_data.get('Temperature', sensor_data.get('temperature', 0)),
                'humidity': sensor_data.get('Humidity', sensor_data.get('humidity', 0)),
                'soil_moisture': sensor_data.get('Soil_Moisture', sensor_data.get('soil_moisture', 0))
            }
            logger.debug(f"Normalized sensor data: {normalized_data}")
            return normalized_data
        
        logger.warning(f"Unexpected sensor data format: {sensor_data}")
        return {
            'sensor_id': f'sensor_{int(time.time())}',
            'temperature': 0,
            'humidity': 0,
            'soil_moisture': 0
        }
    except Exception as e:
        logger.error(f"Error fetching sensor data from Firebase: {e}")
        return {
            'sensor_id': f'sensor_{int(time.time())}',
            'temperature': 0,
            'humidity': 0,
            'soil_moisture': 0
        }

def listen_sensor_data(callback):
    """Listen for real-time updates from Firebase"""
    try:
        logger.debug("Setting up real-time listener for sensor data")
        ref = db.reference('SensorData')  # Update to exact path
        ref.listen(callback)
        logger.debug("Real-time listener started")
    except Exception as e:
        logger.error(f"Error setting up real-time listener: {e}")