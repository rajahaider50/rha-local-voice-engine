import platform
import os
import psutil

class HardwareProfiler:
    @staticmethod
    def get_device_info() -> dict:
        """Collects hardware info for Phase 17 optimization and Phase 18 benchmarks."""
        info = {
            "os": platform.system(),
            "architecture": platform.machine(),
            "cpu_cores": psutil.cpu_count(logical=False),
            "logical_cores": psutil.cpu_count(logical=True),
            "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "python_version": platform.python_version()
        }
        
        # Check if running in Termux (Android)
        info["is_android"] = "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ
        
        return info

    @staticmethod
    def get_profile() -> str:
        """
        Determines the optimal model profile based on available RAM.
        """
        ram = psutil.virtual_memory().total / (1024**3)
        
        if ram < 3.0:
            return "PROFILE_LOW"    # Tiny STT, 0.8B LLM, Q4
        elif ram < 6.0:
            return "PROFILE_MEDIUM" # Base STT, 1.5B LLM, Q4/Q5
        else:
            return "PROFILE_HIGH"   # Base STT, 4B LLM, Q5/Q6
