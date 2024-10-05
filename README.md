# smartpi-mpu6050

A Python library for interacting with the MPU-6050 sensor on the Smart Pi One (Yumi) through I2C communication. This package simplifies the process of retrieving accelerometer, gyroscope, and temperature data from the MPU-6050 sensor, making it ideal for projects that involve motion detection, orientation sensing, or basic IMU tasks.

## Features

- Easy-to-use Python API for MPU-6050 sensor.
- Retrieves accelerometer, gyroscope, and temperature data.
- Configurable ranges for both accelerometer and gyroscope.
- Includes automatic installation of system dependency `python3-smbus`.

## Requirements

- **Hardware**: Smart Pi One (or other systems with I2C support) + MPU-6050 sensor.
- **Software**: Python 3.6 or higher, `smbus` for I2C communication.

## Installation

### Step 1: Clone the repository (if installing manually)

```bash
git clone https://github.com/adnroboticsfr/smartpi-mpu6050.git
cd smartpi-mpu6050
```

### Step 2: Install using pip

You can install the package directly from this repository or PyPI.

```bash
pip3 install smartpi-mpu6050
```

This package will automatically install the system dependency python3-smbus required for I2C communication on Raspberry Pi.

If you have trouble with system-level dependencies, you can manually install python3-smbus via:

```bash
sudo apt-get update
sudo apt-get install python3-dev python3-pip python3-smbus
```

## Uninstallation

To uninstall the package, simply run:

```bash
pip3 uninstall smartpi-mpu6050
```

Optionally, you can remove the python3-smbus system package as well:

```bash
sudo apt-get remove python3-smbus
```

## Usage

After installing the package, you can easily start using it in your Python scripts. Here's a basic example to get temperature, accelerometer, and gyroscope data from the MPU-6050 sensor.

**Automatic Calibration:**  
Calibration is performed automatically during sensor initialization:

```python
mpu = MPU6050(0x68)
```
Offsets are applied automatically when retrieving data from the sensors.

**Real-Time Optimization:**  
To retrieve acceleration or gyroscope data in real-time with a buffer:

```python
mpu = MPU6050(0x68)
accel_buffer = mpu.get_accel_data_buffer(size=10)  # Buffer of 10 readings
gyro_buffer = mpu.get_gyro_data_buffer(size=10)    # Buffer of 10 readings
``` 

### Example 1: Read Temperature, Accelerometer, and Gyroscope Data

```python
from smartpi_mpu6050.mpu6050 import MPU6050

# Initialize the sensor at I2C address 0x68
mpu = MPU6050(0x68)

# Get temperature
temp = mpu.get_temp()
print(f"Temperature: {temp:.2f} °C")

# Get accelerometer data
accel_data = mpu.get_accel_data()
print(f"Accelerometer: X={accel_data['x']:.2f} m/s^2, Y={accel_data['y']:.2f} m/s^2, Z={accel_data['z']:.2f} m/s^2")

# Get gyroscope data
gyro_data = mpu.get_gyro_data()
print(f"Gyroscope: X={gyro_data['x']:.2f} °/s, Y={gyro_data['y']:.2f} °/s, Z={gyro_data['z']:.2f} °/s")
```

### Example 2: Set Accelerometer and Gyroscope Ranges

You can set the range for both the accelerometer and gyroscope to better suit your needs. The default ranges are 2G for the accelerometer and 250 degrees/sec for the gyroscope.

```python
from smartpi_mpu6050.mpu6050 import MPU6050

mpu = MPU6050(0x68)

# Set accelerometer range to 8G
mpu.set_accel_range(mpu.ACCEL_RANGE_8G)

# Set gyroscope range to 1000 degrees/sec
mpu.set_gyro_range(mpu.GYRO_RANGE_1000DEG)

# Now you can retrieve data with the updated ranges
accel_data = mpu.get_accel_data()
gyro_data = mpu.get_gyro_data()

print("Updated Accelerometer Data:", accel_data)
print("Updated Gyroscope Data:", gyro_data)
```

### Example 3: Reading All Data Simultaneously

```python
from smartpi_mpu6050.mpu6050 import MPU6050

mpu = MPU6050(0x68)

# Read all sensor data (accelerometer, gyroscope, and temperature)
sensor_data = mpu.get_all_data()

print("Accelerometer:", sensor_data['accel'])
print("Gyroscope:", sensor_data['gyro'])
print(f"Temperature: {sensor_data['temp']:.2f} °C")

```

## Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue on GitHub. Please make sure to follow the Python coding conventions (PEP-8).

## License 

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

## 
Author
Developed by ADNRoboticsfr.
