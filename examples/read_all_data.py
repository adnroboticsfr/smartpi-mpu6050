from smartpi_mpu6050.mpu6050 import MPU6050

# Initialize MPU-6050 at I2C address 0x68
mpu = MPU6050(0x68)

# Set the accelerometer to 8G and gyroscope to 1000 degrees/sec
mpu.set_accel_range(mpu.ACCEL_RANGE_8G)
mpu.set_gyro_range(mpu.GYRO_RANGE_1000DEG)

# Get and print the updated accelerometer and gyroscope data
accel_data = mpu.get_accel_data()
gyro_data = mpu.get_gyro_data()

print("Updated Accelerometer Data:", accel_data)
print("Updated Gyroscope Data:", gyro_data)
