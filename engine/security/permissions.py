class PermissionManager:
    """
    Phase 33: Security
    Validates tool calls before execution to prevent shell injection or dangerous commands.
    """
    def __init__(self):
        self.allowed_tools = ["OPEN_APP", "SET_VOLUME", "TIME", "BATTERY"]

    def validate_tool_call(self, intent: str) -> bool:
        if intent not in self.allowed_tools and intent != "CONVERSATIONAL":
            print(f"[Security] Tool call blocked: {intent} is not in allowlist.")
            return False
        return True
