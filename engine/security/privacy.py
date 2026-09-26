class PrivacyManager:
    """
    Phase 32: Privacy
    Enforces offline-only mode and ensures no data leaves the device
    without explicit user consent.
    """
    def __init__(self, offline_only: bool = True):
        self.offline_only = offline_only

    def can_access_network(self) -> bool:
        if self.offline_only:
            print("[Security] Network access blocked. Offline mode is active.")
            return False
        return True
