from flask import Blueprint, jsonify
import io, re, os
from flask_socketio import emit, SocketIO
import speech_recognition as sr
from gtts import gTTS
from app.routers.chatbot import (
    chat_completion,
    preprocess_chat_history,
    chat_completion_openrouter,
)

streaming_avatar = Blueprint("streaming_avatar", __name__)


@streaming_avatar.route("/a", methods=["GET"])
def hello_module1():
    return jsonify({"message": "Hello from Module streaming_avatar"})


socket_namespace = "/api/streaming-avatar"


# Helper: remove emojis (covers most ranges)
def remove_emojis(text: str) -> str:
    emoji_pattern = re.compile(
        "["
        "\U0001f600-\U0001f64f"  # emoticons
        "\U0001f300-\U0001f5ff"  # symbols & pictographs
        "\U0001f680-\U0001f6ff"  # transport & map
        "\U0001f700-\U0001f77f"  # alchemical
        "\U0001f780-\U0001f7ff"  # geometric shapes extended
        "\U0001f800-\U0001f8ff"  # supplemental arrows
        "\U0001f900-\U0001f9ff"  # supplemental symbols
        "\U0001fa00-\U0001fa6f"  # chess, symbols
        "\U0001fa70-\U0001faff"  # symbols & pictographs extended-A
        "\U00002702-\U000027b0"  # dingbats
        "\U000024c2-\U0001f251"  # Enclosed characters
        "]+",
        flags=re.UNICODE,
    )
    return emoji_pattern.sub(r"", text)


def register_socketio_handlers(socketio: SocketIO):
    @socketio.on("connect", namespace=socket_namespace)
    def handle_connect():
        print("✅ Client connected to /streaming-avatar")
        emit("message", {"info": "Connected to WebSocket!"})

    @socketio.on("disconnect", namespace=socket_namespace)
    def handle_disconnect():
        print("⚠️ Client disconnected from /streaming-avatar")

    @socketio.on("user_audio", namespace=socket_namespace)
    def handle_user_audio(data: bytes):
        """Speech-to-text from WAV audio input."""
        try:
            if not data:
                emit("stt_result", {"text": "No audio data received"})
                return

            wav_buffer = io.BytesIO(data)
            recognizer = sr.Recognizer()
            with sr.AudioFile(wav_buffer) as source:
                audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            emit("stt_result", {"text": text})
        except sr.UnknownValueError:
            emit("stt_result", {"text": "Speech not understood"})
        except sr.RequestError as e:
            emit("stt_result", {"text": f"Google API error: {e}"})
        except Exception as e:
            emit("stt_result", {"error": str(e)})

    @socketio.on("user_message", namespace=socket_namespace)
    def handle_user_message(data):
        """Chat → Assistant reply → in-memory MP3 audio streaming."""
        try:
            chat_history = data.get("history", [])
            api_key = data.get("api_key")
            model_name = data.get("model", "gpt-4")
            system_prompt = data.get("system_prompt", "")
            max_tokens = data.get("max_tokens", 150)
            top_p = data.get("top_p", 1.0)
            provider = data.get("provider", "hkbu")

            # ---- Chat completion ----
            preprocessed_history = preprocess_chat_history(
                [{"role": "system", "content": system_prompt}] + chat_history
            )
            if provider == "openrouter":
                result = chat_completion_openrouter(
                    chat_history=preprocessed_history,
                    model_name=model_name,
                    max_tokens=max_tokens,
                )
            else:  # default to HKBU GenAI
                result = chat_completion(
                    chat_history=preprocessed_history,
                    api_key=api_key,
                    model_name=model_name,
                    max_tokens=max_tokens,
                    top_p=top_p,
                )

            if "error" in result:
                assistant_reply = result["error"]
            else:
                assistant_reply = (
                    result.get("choices", [{}])[0].get("message", {}).get("content", "")
                )

            print("🤖 Assistant reply:", assistant_reply)

            # ---- clean text for TTS (remove emojis) ----
            tts_text = remove_emojis(assistant_reply).strip()
            if not tts_text:
                tts_text = " "  # avoid gTTS error on empty string
            # ---- generate MP3 in memory ----
            tts = gTTS(text=tts_text, lang="en")
            mp3_buffer = io.BytesIO()
            tts.write_to_fp(mp3_buffer)
            mp3_buffer.seek(0)

            # ---- stream mp3 chunks ----
            chunk_size = 4096
            while True:
                chunk = mp3_buffer.read(chunk_size)
                if not chunk:
                    break
                emit("audio_chunk", chunk)  # binary
            emit("audio_complete")
            # ---- send text reply first ----
            emit("assistant_reply", {"content": assistant_reply})
        except Exception as e:
            print("❌ Error in handle_user_message:", str(e))
            emit("assistant_reply", {"content": f"[Error: {str(e)}]"})
            emit("audio_complete")
