import smbus
import time

class MPU6050:

    GRAVITIY_MS2 = 9.80665
    address = None
    bus = None
    accel_offset = {'x': 0, 'y': 0, 'z': 0}
    gyro_offset = {'x': 0, 'y': 0, 'z': 0}

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F
    TEMP_OUT0 = 0x41
    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47
    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address, bus=1):
        self.address = address
        try:
            self.bus = smbus.SMBus(bus)
            self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)  # Wake up the MPU-6050
        except FileNotFoundError:
            raise RuntimeError("smbus not found. Please install with `sudo apt-get install python3-smbus`")

        # Perform automatic calibration
        self.calibrate_accel()
        self.calibrate_gyro()

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them into one."""
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)
        value = (high << 8) + low
        if value >= 0x8000:
            return -((65535 - value) + 1)
        else:
            return value

    def get_temp(self):
        """Reads and returns the temperature in degrees Celsius."""
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)
        actual_temp = (raw_temp / 340.0) + 36.53
        return actual_temp

    def get_accel_data(self, g=False):
        """Gets and returns accelerometer data with offsets applied."""
        x = self.read_i2c_word(self.ACCEL_XOUT0) - self.accel_offset['x']
        y = self.read_i2c_word(self.ACCEL_YOUT0) - self.accel_offset['y']
        z = self.read_i2c_word(self.ACCEL_ZOUT0) - self.accel_offset['z']

        accel_range = self.read_accel_range(True)
        accel_scale_modifier = {
            self.ACCEL_RANGE_2G: self.ACCEL_SCALE_MODIFIER_2G,
            self.ACCEL_RANGE_4G: self.ACCEL_SCALE_MODIFIER_4G,
            self.ACCEL_RANGE_8G: self.ACCEL_SCALE_MODIFIER_8G,
            self.ACCEL_RANGE_16G: self.ACCEL_SCALE_MODIFIER_16G,
        }.get(accel_range, self.ACCEL_SCALE_MODIFIER_2G)

        x /= accel_scale_modifier
        y /= accel_scale_modifier
        z /= accel_scale_modifier

        if g:
            return {'x': x, 'y': y, 'z': z}
        else:
            return {'x': x * self.GRAVITIY_MS2, 'y': y * self.GRAVITIY_MS2, 'z': z * self.GRAVITIY_MS2}

    def get_gyro_data(self):
        """Gets and returns gyroscope data with offsets applied."""
        x = (self.read_i2c_word(self.GYRO_XOUT0) - self.gyro_offset['x']) / self.GYRO_SCALE_MODIFIER_250DEG
        y = (self.read_i2c_word(self.GYRO_YOUT0) - self.gyro_offset['y']) / self.GYRO_SCALE_MODIFIER_250DEG
        z = (self.read_i2c_word(self.GYRO_ZOUT0) - self.gyro_offset['z']) / self.GYRO_SCALE_MODIFIER_250DEG

        return {'x': x, 'y': y, 'z': z}

    def get_all_data(self):
        """Reads and returns accelerometer, gyroscope, and temperature data."""
        return {
            'accel': self.get_accel_data(),
            'gyro': self.get_gyro_data(),
            'temp': self.get_temp()
        }

    def calibrate_accel(self, samples=100):
        """Automatically calibrates the accelerometer by calculating offsets."""
        print("Calibrating accelerometer...")
        x_offset, y_offset, z_offset = 0, 0, 0

        for _ in range(samples):
            accel_data = self.get_accel_data(g=True)  # Get data in 'g' units
            x_offset += accel_data['x']
            y_offset += accel_data['y']
            z_offset += (accel_data['z'] - 1)  # Subtract gravity (1g) from Z

        self.accel_offset = {
            'x': x_offset / samples,
            'y': y_offset / samples,
            'z': z_offset / samples
        }
        print("Accelerometer calibrated with offsets:", self.accel_offset)

    def calibrate_gyro(self, samples=100):
        """Automatically calibrates the gyroscope by calculating offsets."""
        print("Calibrating gyroscope...")
        x_offset, y_offset, z_offset = 0, 0, 0

        for _ in range(samples):
            gyro_data = self.get_gyro_data()
            x_offset += gyro_data['x']
            y_offset += gyro_data['y']
            z_offset += gyro_data['z']

        self.gyro_offset = {
            'x': x_offset / samples,
            'y': y_offset / samples,
            'z': z_offset / samples
        }
        print("Gyroscope calibrated with offsets:", self.gyro_offset)

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer."""
        # First clear the current accel range (bits 3 and 4)
        current_range = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG) & ~0x18
        # Set the new range
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, current_range | accel_range)

    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope."""
        # First clear the current gyro range (bits 3 and 4)
        current_range = self.bus.read_byte_data(self.address, self.GYRO_CONFIG) & ~0x18
        # Set the new range
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, current_range | gyro_range)

    def read_accel_range(self, raw=False):
        """Reads the range the accelerometer is set to."""
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw:
            return raw_data
        else:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data_buffer(self, size=10):
        """Retrieve a buffer of recent accelerometer readings."""
        buffer = []
        for _ in range(size):
            buffer.append(self.get_accel_data())
            time.sleep(0.01)  # Short delay to simulate real-time buffer reading
        return buffer

    def get_gyro_data_buffer(self, size=10):
        """Retrieve a buffer of recent gyroscope readings."""
        buffer = []
        for _ in range(size):
            buffer.append(self.get_gyro_data())
            time.sleep(0.01)  # Short delay to simulate real-time buffer reading
        return buffer
