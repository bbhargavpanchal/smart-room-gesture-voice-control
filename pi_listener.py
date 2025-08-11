import time
import serial
import logging
from azure.iot.device import IoTHubDeviceClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

CONNECTION_STRING = "HostName=SmartRoom.azure-devices.net;DeviceId=raspberrypi4;SharedAccessKey=fDoZ4csjer5uhLgmP8gvp8peZPBadtL0nAIoTBCHL1M="


def main():
    arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=2)
    time.sleep(2)
    logging.info("? Connected to Arduino")

    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    logging.info("? Connected to Azure IoT Hub")

    try:
        while True:
            try:
                message = client.receive_message()
                cmd = message.data.decode().strip()
                logging.info(f"?? Received command: {cmd}")
                arduino.write((cmd + "\n").encode())
            except Exception as e:
                logging.error(f"?? Connection lost or error: {e}")
                logging.info("?? Attempting to reconnect...")
                client.shutdown()
                time.sleep(5)
                client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
                logging.info("? Reconnected to Azure IoT Hub")

    except KeyboardInterrupt:
        logging.info("?? Shutting down...")

    finally:
        client.shutdown()
        arduino.close()
        logging.info("? Clean exit.")

if __name__ == "__main__":
    main()
