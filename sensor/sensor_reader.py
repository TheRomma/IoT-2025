from machine import Pin, I2C
from time import sleep_ms
from bmp280 import BMP280


class BMP280Reader:
    def __init__(self, i2c=None, addr=0x76, mode="normal"):
        if i2c is None:
            i2c = I2C(0, sda=Pin(20), scl=Pin(21))
        self.bmp = BMP280(i2c, addr=addr)

        self.set_mode(mode)

    def set_mode(self, mode: str):
        """Set the BMP280 power mode: 'normal' or 'sleep'."""
        mode = mode.lower()
        if mode == "normal":
            self.bmp.normal_measure()
        elif mode == "sleep":
            self.bmp.sleep()
        else:
            raise ValueError("Invalid mode. Use 'normal' or 'sleep'.")

        self._mode = mode

    def get_mode(self):
        """Return current mode as a string."""
        pm = self.bmp.power_mode
        if pm == 0:
            return "sleep"
        elif pm == 1:
            return "forced"
        elif pm == 3:
            return "normal"
        else:
            return f"unknown({pm})"

    def get_temperature(self):
        """Return temperature in Celsius."""
        return self.bmp.temperature

    def get_pressure(self):
        """Return pressure in hPa."""
        return self.bmp.pressure / 100.0

    def get_all(self):
        """Return both temperature and pressure."""
        return self.get_temperature(), self.get_pressure()

    def print_readings(self):
        """Print temperature and pressure."""
        t, p = self.get_all()
        print("Temperature: {:.2f} °C".format(t))
        print("Pressure: {:.2f} hPa".format(p))

    def measure_once(self):
        """
        Force a single measurement (one-shot mode).
        Works regardless of current mode.
        If currently in normal mode, will restore it afterward.
        """
        prev_mode = self.get_mode()
        self.bmp.force_measure()
        sleep_ms(self.bmp.read_wait_ms)
        data = self.get_all()
        if prev_mode == "normal":
            self.bmp.normal_measure()
        return data


if __name__ == "__main__":
    print("Initializing BMP280 sensor...")
    i2c = I2C(0, sda=Pin(20), scl=Pin(21))
    sensor = BMP280Reader(i2c, mode='sleep')

    while True:
        print(sensor.measure_once())
        sleep_ms(1000)
        mode = sensor.get_mode()
        print("Mode after read:", mode)
