import os

class SystemTools:
    """System-level non-Android tools"""
    @staticmethod
    def get_cpu_temp() -> str:
        try:
            with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
                temp = int(f.read().strip()) / 1000.0
                return f"{temp}°C"
        except Exception:
            return "Unknown"
