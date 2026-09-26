class PipelineState:
    def __init__(self):
        self.is_listening = True
        self.is_processing = False
        self.is_speaking = False

class AudioPipeline:
    def __init__(self):
        # Initialize sub-modules
        # self.vad = VAD()
        # self.stt = WhisperEngine(...)
        # self.intent = IntentRouter(...)
        # self.llm = LlamaEngine(...)
        # self.tts = TTSRouter(...)
        self.state = PipelineState()

    def start(self):
        """
        Starts the main audio capture loop.
        """
        print("Starting RHA Audio Pipeline...")
        # Placeholder loop
        
    def stop(self):
        print("Stopping RHA Audio Pipeline...")
        
    def interrupt(self):
        """
        Handles Barge-in / interruption
        """
        self.state.is_speaking = False
        # clear audio queues
        print("Interrupted.")
