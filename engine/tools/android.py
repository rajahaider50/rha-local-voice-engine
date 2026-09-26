import subprocess
import json

class AndroidTools:
    """
    Interface for Android native actions, meant to be called 
    by the intent engine or LLM.
    Uses Termux API for local execution on Android.
    """
    def __init__(self):
        self.is_termux = self._check_termux()

    def _check_termux(self) -> bool:
        try:
            subprocess.run(["termux-info"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except FileNotFoundError:
            return False

    def _run_termux_cmd(self, cmd: list) -> str:
        if not self.is_termux:
            print(f"[AndroidTools] Not in Termux. Mocking command: {' '.join(cmd)}")
            return ""
        
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"[AndroidTools] Error running Termux command: {e}")
            return ""

    def open_app(self, package_name: str) -> bool:
        """Opens an Android application using termux-open."""
        print(f"[AndroidTools] Opening app/URL: {package_name}")
        # 'termux-open' can open URLs or sometimes package intents if configured.
        # Alternatively, am start can be used if rooted or via adb, 
        # but termux-open is standard for opening links/files.
        if package_name.lower() == "youtube":
            self._run_termux_cmd(["termux-open", "https://www.youtube.com"])
        else:
            self._run_termux_cmd(["termux-open", package_name])
        return True
        
    def set_volume(self, stream: str, level: int) -> bool:
        """Sets device volume via termux-volume."""
        print(f"[AndroidTools] Setting {stream} volume to: {level}")
        self._run_termux_cmd(["termux-volume", stream, str(level)])
        return True
        
    def get_battery(self) -> int:
        """Gets battery status via termux-battery-status."""
        print("[AndroidTools] Reading battery level...")
        output = self._run_termux_cmd(["termux-battery-status"])
        if output:
            try:
                data = json.loads(output)
                return int(data.get("percentage", 100))
            except json.JSONDecodeError:
                pass
        return 100

    def toggle_flashlight(self, state: bool) -> bool:
        """Toggles flashlight via termux-torch."""
        cmd = ["termux-torch", "on" if state else "off"]
        self._run_termux_cmd(cmd)
        return True

    def text_to_speech(self, text: str):
        """Uses system TTS as a fallback via termux-tts-speak."""
        self._run_termux_cmd(["termux-tts-speak", text])
        return True
