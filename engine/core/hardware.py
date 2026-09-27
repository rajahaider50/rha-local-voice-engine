import platform
import os
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

class HardwareProfiler:
    @staticmethod
    def get_device_info() -> dict:
        """Collects hardware info for Phase 17 optimization and Phase 18 benchmarks."""
        # Fallback values if psutil is not available
        cpu_cores = 4
        logical_cores = 8
        ram_total_gb = 4.0
        
        if PSUTIL_AVAILABLE:
            cpu_cores = psutil.cpu_count(logical=False) or 4
            logical_cores = psutil.cpu_count(logical=True) or 8
            ram_total_gb = round(psutil.virtual_memory().total / (1024**3), 2)
            
        info = {
            "os": platform.system(),
            "architecture": platform.machine(),
            "cpu_cores": cpu_cores,
            "logical_cores": logical_cores,
            "ram_total_gb": ram_total_gb,
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
        ram = 4.0
        if PSUTIL_AVAILABLE:
            ram = psutil.virtual_memory().total / (1024**3)
        
        if ram < 3.0:
            return "PROFILE_LOW"    # Tiny STT, 0.8B LLM, Q4
        elif ram < 6.0:
            return "PROFILE_MEDIUM" # Base STT, 1.5B LLM, Q4/Q5
        else:
            return "PROFILE_HIGH"   # Base STT, 4B LLM, Q5/Q6
