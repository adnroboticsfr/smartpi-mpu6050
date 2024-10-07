from smartpi_mpu6050.mpu6050 import MPU6050

# Initialize MPU-6050 at I2C address 0x68
mpu = MPU6050(0x68)  # Use 0x53 for ADXL345

# Print temperature
print(f"Temperature: {mpu.get_temp():.2f} °C")

# Print accelerometer data
accel = mpu.get_accel_data()
print(f"Accelerometer: {accel}")

# Print gyroscope data
gyro = mpu.get_gyro_data()
print(f"Gyroscope: {gyro}")
