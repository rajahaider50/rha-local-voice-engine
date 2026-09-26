import time
from threading import Thread, Event
from engine.audio.capture import AudioCapture
from engine.vad.detector import VoiceActivityDetector
from engine.wakeword.detector import WakeWordDetector
from engine.stt.whisper_engine import WhisperEngine
from engine.language.router import LanguageRouter
from engine.intent.router import IntentRouter
from engine.llm.llama_engine import LlamaEngine
from engine.tts.router import TTSRouter
from engine.tools.android import AndroidTools
from engine.memory.manager import MemoryManager

class PipelineState:
    def __init__(self):
        self.mode = "WAKE_WORD" # WAKE_WORD, LISTENING, PROCESSING, SPEAKING
        self.interrupt_event = Event()

class RHAEngine:
    def __init__(self):
        print("[System] Initializing RHA Local Voice Engine...")
        self.state = PipelineState()
        
        # Phase 2 & 3
        self.audio = AudioCapture()
        self.vad = VoiceActivityDetector()
        
        # Phase 4 & 5
        self.wakeword = WakeWordDetector()
        self.stt = WhisperEngine()
        
        # Phase 6 & 7
        self.lang = LanguageRouter()
        self.intent = IntentRouter()
        
        # Phase 8, 9, 10
        self.tools = AndroidTools()
        self.llm = LlamaEngine()
        
        # Phase 11-14
        self.tts = TTSRouter()
        self.memory = MemoryManager()

    def run(self):
        """Main Audio Loop with Phase 15 Barge-in Support"""
        print("\n" + "="*40)
        print(" RHA ENGINE RUNNING ")
        print("="*40)
        print("Waiting for wake word ('Hey Jarvis')...")
        
        audio_buffer = []
        is_speaking_state = False
        silence_frames = 0
        
        try:
            for chunk in self.audio.start_stream():
                
                # PHASE 15: BARGE-IN INTERRUPTION
                # If we are speaking, but the user starts talking loudly, we interrupt
                if self.state.mode == "SPEAKING":
                    if self.vad.is_speech(chunk):
                        print("\n[Barge-in] User interrupted! Stopping TTS...")
                        self.state.interrupt_event.set()
                        self.state.mode = "WAKE_WORD"
                        audio_buffer = []
                    continue
                
                # STATE: Waiting for Wake Word
                if self.state.mode == "WAKE_WORD":
                    if self.wakeword.process_chunk(chunk):
                        print("\n🔔 WAKE WORD DETECTED!")
                        self.state.mode = "LISTENING"
                        self.tts.play_audio("Yes?", "english")
                        is_speaking_state = False
                        silence_frames = 0
                        audio_buffer = []
                        print("[Listening]...")
                        
                # STATE: Listening for command
                elif self.state.mode == "LISTENING":
                    if self.vad.is_speech(chunk):
                        is_speaking_state = True
                        silence_frames = 0
                        audio_buffer.append(chunk)
                    elif is_speaking_state:
                        silence_frames += 1
                        audio_buffer.append(chunk)
                        
                        # User stopped speaking
                        if silence_frames > 20:
                            self.state.mode = "PROCESSING"
                            self._process_command(b"".join(audio_buffer))
                            
                            # Return to wake word state after processing
                            if self.state.mode != "SPEAKING":
                                self.state.mode = "WAKE_WORD"
                                print("\nWaiting for wake word...")
                                
        except KeyboardInterrupt:
            print("\nShutting down RHA Engine...")
        finally:
            self.audio.terminate()

    def _process_command(self, audio_data: bytes):
        print("[STT] Transcribing...")
        text = self.stt.transcribe_audio(audio_data)
        
        if not text:
            print("[STT] No text recognized.")
            return
            
        print(f"🗣️ User: {text}")
        
        # Route Language & Intent
        lang, conf, norm = self.lang.detect_and_normalize(text)
        intent, params, i_conf = self.intent.route_intent(norm, lang)
        
        # Execute Action or LLM
        if intent == "OPEN_APP":
            app = params.get('app', '')
            self.tools.open_app(app)
            self.tts.play_audio(f"Opening {app}", "english")
            
        elif intent == "CONVERSATIONAL":
            self.state.mode = "SPEAKING"
            self.state.interrupt_event.clear()
            
            # Fetch memory
            context = self.memory.retrieve_relevant_context(norm)
            prompt = f"{context}\nUser: {norm}" if context else norm
            
            # Phase 10 & 13: Streaming LLM -> Streaming TTS
            print("[LLM] Generating response...")
            stream = self.llm.generate_stream(prompt)
            chunked_stream = self.tts.chunk_text(stream)
            
            for sentence in chunked_stream:
                if self.state.interrupt_event.is_set():
                    break # Barge-in triggered
                print(f"[Assistant] {sentence}")
                self.tts.play_audio(sentence, lang)

if __name__ == "__main__":
    RHAEngine().run()
