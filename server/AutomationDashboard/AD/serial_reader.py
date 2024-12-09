import serial
import os
import django
import time
import logging
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'AutomationDashboard')))


# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutomationDashboard.settings')
django.setup()

from AD.models import SensorData

# Configuration - Consider moving to a config file or environment variables
ARDUINO_PORT = "COM5"  # Use appropriate port for your system
BAUD_RATE = 9600
MAX_RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds

def read_from_serial():
    """
    Continuously read sensor data from Arduino serial port
    and save to database
    """
    retry_count = 0
    while retry_count < MAX_RETRY_ATTEMPTS:
        try:
            with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1) as ser:
                logger.info(f"Connected to serial port {ARDUINO_PORT}")
                retry_count = 0  # Reset retry count on successful connection
                
                while True:
                    try:
                        line = ser.readline().decode('utf-8').strip()
                        if line:
                            try:
                                # Assuming data format is "temperature,humidity"
                                temperature, humidity = map(float, line.split(","))
                                
                                # Create and save sensor data
                                sensor_entry = SensorData.objects.create(
                                    temperature=temperature,
                                    humidity=humidity
                                )
                                
                                logger.info(f"Data saved: Temp={temperature}°C, Humidity={humidity}%")
                            
                            except ValueError:
                                logger.warning(f"Invalid data format: {line}")
                    
                    except (UnicodeDecodeError, serial.SerialException) as e:
                        logger.error(f"Serial reading error: {e}")
                        break
        
        except serial.SerialException as e:
            retry_count += 1
            logger.error(f"Failed to connect to serial port. Attempt {retry_count}/{MAX_RETRY_ATTEMPTS}. Error: {e}")
            time.sleep(RETRY_DELAY)
    
    logger.error("Max retry attempts reached. Could not establish serial connection.")

def send_to_serial(command):
    """
    Send a command to the Arduino via serial port
    
    :param command: Command string to send
    :raises serial.SerialException: If unable to send command
    """
    try:
        with serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1) as ser:
            ser.write(command.encode('utf-8'))
            logger.info(f"Command sent: {command}")
    
    except serial.SerialException as e:
        logger.error(f"Error sending serial command: {e}")
        raise

if __name__ == "__main__":
    try:
        read_from_serial()
    except KeyboardInterrupt:
        logger.info("Serial reading stopped by user.")