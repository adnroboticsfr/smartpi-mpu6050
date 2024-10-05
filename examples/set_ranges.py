from smartpi_mpu6050.mpu6050 import MPU6050

# Initialize MPU-6050 at I2C address 0x68
mpu = MPU6050(0x68)

# Read and print all sensor data
sensor_data = mpu.get_all_data()

print("Accelerometer:", sensor_data['accel'])
print("Gyroscope:", sensor_data['gyro'])
print(f"Temperature: {sensor_data['temp']:.2f} °C")
