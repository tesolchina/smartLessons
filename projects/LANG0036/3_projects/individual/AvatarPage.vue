<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <!-- Left Sidebar -->
    <LeftSidebar
      v-model:isOpen="isSidebarOpen"
      v-model:apiKey="apiKey"
      v-model:model="model"
      v-model:selectedProvider="selectedProvider"
      :systemPrompt="systemPrompt"
      :welcomePrompt="welcomePrompt"
      :isConnected="isConnected"
      :tokenUsage="tokenUsage"
      :isConnecting="isConnecting"
      @connectAPI="connectAPI"
      @clearAPI="clearAPI"
    />

    <!-- Main Chat Area -->
    <div
      class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden transition-all duration-300"
    >
      <!-- Header -->
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">🎙️ Speak with your AI assistant</div>
        </div>
        <div class="flex gap-2">
          <button
            v-for="btn in headerButtons"
            :key="btn.id"
            class="bg-white/20 px-3 py-1 rounded-lg hover:bg-white/30"
            @click="btn.action"
          >
            {{ btn.label }}
          </button>
        </div>
      </div>

      <!-- Avatar moved here -->
      <div
        v-if="showAvatar"
        class="chat-avatar-container flex justify-center items-center py-4 border-b"
      >
        <AvatarComponent :state="avatarState" />
      </div>

      <!-- Messages -->
      <div ref="messagesContainer" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div v-for="(msg, i) in formattedMessages" :key="i" class="flex" :class="msg.align">
          <div
            class="max-w-xs md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="msg.style"
          >
            <div class="font-semibold text-xs mb-1">{{ msg.label }}</div>
            <div class="text-base whitespace-pre-wrap">{{ msg.content }}</div>
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.time }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <!-- Overlay if not connected -->
        <div
          v-if="!isConnected"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your API key first
        </div>

        <!-- Mode Toggle -->
        <div class="flex justify-end mb-4">
          <div class="flex items-center space-x-2">
            <span class="text-sm font-medium text-gray-700">Audio Mode</span>
            <button
              @click="toggleInputMode"
              :class="[
                'relative inline-flex h-6 w-11 items-center rounded-full transition-colors',
                inputMode === 'audio' ? 'bg-indigo-600' : 'bg-gray-200',
              ]"
            >
              <span
                :class="[
                  'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                  inputMode === 'audio' ? 'translate-x-6' : 'translate-x-1',
                ]"
              ></span>
            </button>
            <span class="text-sm font-medium text-gray-700">Text Mode</span>
          </div>
        </div>

        <!-- Audio Input -->
        <div v-if="inputMode === 'audio'">
          <div class="flex justify-center">
            <button
              class="px-6 py-3 rounded-full bg-red-500 text-white text-lg font-bold shadow-lg hover:bg-red-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
              :disabled="!isConnected || isPlaying || isRecognizing"
              @click="toggleRecording"
            >
              {{ isRecording ? "⏹ Listening" : "🎤 Speak" }}
            </button>
          </div>
        </div>

        <!-- Text Input -->
        <div v-else class="flex items-center space-x-2">
          <input
            v-model="userText"
            @keyup.enter="sendTextToChatbot"
            type="text"
            placeholder="Type your message..."
            class="flex-1 p-3 rounded-full border border-gray-300 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-shadow disabled:bg-gray-100"
            :disabled="!isConnected || isLoading"
          />
          <button
            @click="sendTextToChatbot"
            :disabled="!isConnected || !userText.trim() || isLoading"
            class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            Send
          </button>
          <button
            class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
            :disabled="!chatHistory.length"
            @click="showReport = true"
            title="Finish & View Report"
          >
            ✓
          </button>
        </div>
      </div>

      <!-- Report Modal -->
      <ReportModal
        :show="showReport"
        :chatHistory="chatHistory"
        :userCount="userCount"
        :assistantCount="assistantCount"
        :botName="selectedBot.name"
        @close="showReport = false"
      />
    </div>
  </div>

  <!-- Loader -->
  <div
    v-else
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 items-center justify-center"
  >
    <div class="flex items-center justify-center space-x-3">
      <svg
        class="animate-spin h-8 w-8 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle
          class="opacity-25"
          cx="12"
          cy="12"
          r="10"
          stroke="currentColor"
          stroke-width="4"
        ></circle>
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        ></path>
      </svg>
      <span class="text-white text-2xl font-semibold">Loading Chatbot...</span>
    </div>
  </div>

  <!-- Notification -->
  <div
    v-if="notification.visible"
    class="fixed top-5 right-5 z-50 px-4 py-3 rounded-lg shadow-lg text-white"
    :class="notificationClass"
  >
    {{ notification.message }}
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "../components/chatbotStore";
import { io } from "socket.io-client";
import { BASE_URL } from "../components/base_url";
import AvatarComponent from "../components/avatar/AvatarComponent.vue";
import LeftSidebar from "../components/avatar/LeftSidebar.vue";
import ReportModal from "../components/ReportModal.vue";
import * as speechsdk from "microsoft-cognitiveservices-speech-sdk";

const props = defineProps({ avatarId: { type: String, required: true } });
const router = useRouter();
const chatbotStore = useChatbotStore();

// --- State ---
const chatHistory = ref([]);
const apiKey = ref("");
const systemPrompt = ref("");
const welcomePrompt = ref("");
const model = ref("");
const isConnected = ref(false);
const isSidebarOpen = ref(true);
const avatarState = ref("idle");
const isRecording = ref(false);
const isPlaying = ref(false);
const isRecognizing = ref(false);
const inputMode = ref("audio");
const userText = ref("");
const isLoading = ref(false);
const showReport = ref(false);
const selectedProvider = ref("openrouter");
const isConnecting = ref(false);
const notification = ref({ message: "", type: "success", visible: false });
const messagesContainer = ref(null);
const showAvatar = ref(true);

let socket = null;

// --- Computeds ---
const selectedBot = computed(() => chatbotStore.availableBots.find((b) => b.id === props.avatarId));
const assistantCount = computed(
  () => chatHistory.value.filter((m) => m.role === "assistant").length
);
const userCount = computed(() => chatHistory.value.filter((m) => m.role === "user").length);
const tokenUsage = computed(() => {
  let total = 0;
  chatHistory.value.forEach((m, i) => {
    if (m.role === "user") total += m.content?.length || 0;
    if (m.role === "assistant" && i !== 0) {
      total += m.content?.length || 0;
    }
  });
  return Math.floor((total * 3) / 4);
});

const formattedMessages = computed(() =>
  chatHistory.value.map((m) => ({
    ...m,
    align: m.role === "user" ? "justify-end" : "justify-start",
    style:
      m.role === "user"
        ? "bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none"
        : "bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none",
    label: m.role === "user" ? "👤 You" : "🤖 Assistant",
    time: m.timestamp.toLocaleTimeString(),
  }))
);
const notificationClass = computed(() =>
  notification.value.type === "success" ? "bg-green-500" : "bg-red-500"
);
const headerButtons = [
  {
    id: "left",
    label: computed(() => (isSidebarOpen.value ? "⬅ Hide Left" : "➡ Show Left")),
    action: () => (isSidebarOpen.value = !isSidebarOpen.value),
  },
  {
    id: "up",
    label: computed(() => (showAvatar.value ? "⬆️ Hide Avatar" : "⬇️ Show Avatar")),
    action: () => (showAvatar.value = !showAvatar.value),
  },
  { id: "new", label: "🔄 New Session", action: () => startNewSession() },
  { id: "back", label: "⬅ Back", action: () => goBack() },
];

// --- Lifecycle ---
onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedBot.value) {
    router.push("/");
    return;
  }

  systemPrompt.value = selectedBot.value.systemPrompt;
  welcomePrompt.value = selectedBot.value.welcomePrompt;
  model.value = selectedBot.value.model;
  await getAzureToken();
  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true);
  }
});

// --- Cookie helpers ---
function setCookie(name, value, minutes) {
  const d = new Date();
  d.setTime(d.getTime() + minutes * 60 * 1000);
  const expires = "expires=" + d.toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)};${expires};path=/`;
}
function getCookie(name) {
  const decodedCookie = decodeURIComponent(document.cookie);
  const cookies = decodedCookie.split("; ");
  for (let cookie of cookies) {
    const [key, value] = cookie.split("=");
    if (key === name) return value;
  }
  return null;
}

// --- Azure Token ---
async function getAzureToken() {
  const cachedToken = getCookie("azureToken");
  const cachedRegion = getCookie("azureRegion");
  if (cachedToken && cachedRegion) {
    return { authToken: cachedToken, region: cachedRegion };
  }
  try {
    const res = await fetch(`${BASE_URL}/streaming-avatar/get-speech-token`);
    if (!res.ok) throw new Error("Failed to fetch speech token");
    const data = await res.json();
    setCookie("azureToken", data.token, 9);
    setCookie("azureRegion", data.region, 9);
    return { authToken: data.token, region: data.region };
  } catch (err) {
    console.error("Azure token fetch error:", err);
    return { authToken: null, region: null };
  }
}

// --- Azure TTS helpers ---
function splitIntoSentences(text) {
  return text.replace(/\s+/g, " ").match(/[^.!?]+[.!?]+/g) || [text];
}

// Convert text → ArrayBuffer (not auto-play)
async function synthesizeToBuffer(sentence) {
  const tokenObj = await getAzureToken();
  if (!tokenObj.authToken) throw new Error("No Azure token");

  const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(
    tokenObj.authToken,
    tokenObj.region
  );
  speechConfig.speechSynthesisVoiceName = "en-US-JennyNeural";

  return new Promise((resolve, reject) => {
    const pushStream = speechsdk.AudioOutputStream.createPullStream();
    const audioConfig = speechsdk.AudioConfig.fromStreamOutput(pushStream);
    const synthesizer = new speechsdk.SpeechSynthesizer(speechConfig, audioConfig);

    synthesizer.speakTextAsync(
      sentence,
      (result) => {
        synthesizer.close();
        if (result.reason === speechsdk.ResultReason.SynthesizingAudioCompleted) {
          // Collect audio data into a Blob
          const buffer = result.audioData;
          resolve(buffer);
        } else {
          reject(result.errorDetails);
        }
      },
      (err) => {
        synthesizer.close();
        reject(err);
      }
    );
  });
}

// Plays a buffer sequentially
function playAudioBuffer(buffer) {
  return new Promise((resolve) => {
    const blob = new Blob([buffer], { type: "audio/wav" });
    const url = URL.createObjectURL(blob);
    const audio = new Audio(url);
    audio.onended = () => {
      URL.revokeObjectURL(url);
      resolve();
    };
    audio.play();
  });
}

// Speak reply with pipelined synthesis + playback
async function speakReplySequentially(replyText) {
  const sentences = splitIntoSentences(replyText);
  isPlaying.value = true;
  avatarState.value = "speaking";

  try {
    let playPromise = Promise.resolve(); // chain for ordered playback

    for (const sentence of sentences) {
      // Start synthesis immediately
      const synthPromise = synthesizeToBuffer(sentence);
      // When synthesis finishes, enqueue playback to happen *after previous one finishes*
      playPromise = playPromise.then(async () => {
        try {
          const buffer = await synthPromise;
          await playAudioBuffer(buffer);
        } catch (err) {
          console.error("TTS sentence error:", err);
        }
      });
    }

    // Wait until last playback finishes
    await playPromise;
  } catch (err) {
    console.error("Pipeline TTS error:", err);
  } finally {
    isPlaying.value = false;
    avatarState.value = "idle";
  }
}

// --- Speech Recognition ---
async function toggleRecording() {
  if (isRecording.value) {
    isRecording.value = false;
    avatarState.value = "idle";
    return;
  }
  try {
    const tokenObj = await getAzureToken();
    if (!tokenObj.authToken) {
      showNotification("❌ Could not get Azure token", "error");
      return;
    }
    isRecording.value = true;
    avatarState.value = "listening";
    isRecognizing.value = true;
    const speechConfig = speechsdk.SpeechConfig.fromAuthorizationToken(
      tokenObj.authToken,
      tokenObj.region
    );
    speechConfig.speechRecognitionLanguage = "en-US";
    const audioConfig = speechsdk.AudioConfig.fromDefaultMicrophoneInput();
    const recognizer = new speechsdk.SpeechRecognizer(speechConfig, audioConfig);
    recognizer.recognizeOnceAsync((result) => {
      isRecording.value = false;
      isRecognizing.value = false;
      avatarState.value = "thinking";
      if (result.reason === speechsdk.ResultReason.RecognizedSpeech) {
        const recognizedText = result.text.trim();
        if (recognizedText) {
          chatHistory.value.push(newMessage("user", recognizedText));
          sendUserAudioMessage(recognizedText);
        }
      } else {
        showNotification("⚠️ Speech not recognized", "error");
      }
      recognizer.close();
    });
  } catch (err) {
    console.error("Azure STT error:", err);
    showNotification("❌ Speech recognition failed", "error");
    isRecording.value = false;
    isRecognizing.value = false;
    avatarState.value = "idle";
  }
}

// --- Helpers ---
const newMessage = (role, content) => ({ role, content, timestamp: new Date() });
function scrollToBottom() {
  nextTick(() => {
    const el = messagesContainer.value;
    if (el) el.scrollTop = el.scrollHeight;
  });
}
function goBack() {
  router.push("/");
}
function toggleInputMode() {
  inputMode.value = inputMode.value === "audio" ? "text" : "audio";
}
function showNotification(msg, type = "success") {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
}
async function apiCall(endpoint, payload) {
  const res = await fetch(`${BASE_URL}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// --- API Connect ---
async function connectAPI(auto = false) {
  if (!apiKey.value && !auto && selectedProvider.value !== "openrouter") return;
  localStorage.setItem("chatbot_api_key", apiKey.value);
  isConnecting.value = true;
  isConnected.value = false;
  try {
    let providerUrl =
      selectedProvider.value === "openrouter" ? "/chatbot/chat_openrouter" : "/chatbot/chat";
    const data = await apiCall(providerUrl, {
      chat_history: [
        { role: "system", content: "connection test, return 1 if you can read." },
        { role: "user", content: "Hello!" },
      ],
      api_key: apiKey.value,
      model_name: model.value,
    });
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message;
    if (reply?.trim()) {
      isConnected.value = true;
      showNotification("✅ Connected and working!");
    } else {
      showNotification("⚠️ Connected, but no valid reply.", "error");
    }
  } catch (e) {
    console.error(e);
    showNotification("❌ Failed to connect.", "error");
  } finally {
    isConnecting.value = false;
  }
  connectWebSocket();
  if (!chatHistory.value.length && isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}
function clearAPI() {
  localStorage.removeItem("chatbot_api_key");
  apiKey.value = "";
  isConnected.value = false;
  chatHistory.value = [];
}

// --- WebSocket ---
function connectWebSocket() {
  socket = io(`${BASE_URL}/streaming-avatar`, { transports: ["websocket"] });
  socket.on("connect", () => console.log("WebSocket connected"));
}

// --- Chat Actions ---
function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
  }
}
function sendUserAudioMessage(text) {
  if (!isConnected.value || !text.trim() || !socket) return;
  chatHistory.value.push(newMessage("assistant", "⏳ Avatar is thinking..."));
  const idx = chatHistory.value.length - 1;
  socket.emit("user_message", {
    text,
    system_prompt: systemPrompt.value,
    api_key: apiKey.value,
    model: model.value,
    provider: selectedProvider.value,
    history: chatHistory.value.map(({ role, content }) => ({ role, content })),
  });
  socket.once("assistant_reply", async (reply) => {
    const responseText = reply?.content || "[No response]";
    chatHistory.value[idx] = {
      ...chatHistory.value[idx],
      content: responseText,
      timestamp: new Date(),
    };
    scrollToBottom();
    await speakReplySequentially(responseText);
  });
}
async function sendTextToChatbot() {
  if (!isConnected.value || !userText.value.trim() || isLoading.value) return;
  chatHistory.value.push(newMessage("user", userText.value.trim()));
  userText.value = "";
  chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."));
  const idx = chatHistory.value.length - 1;
  isLoading.value = true;
  avatarState.value = "thinking";
  try {
    let providerUrl =
      selectedProvider.value === "openrouter" ? "/chatbot/chat_openrouter" : "/chatbot/chat";
    const data = await apiCall(providerUrl, {
      chat_history: [
        { role: "system", content: systemPrompt.value },
        ...chatHistory.value.map(({ role, content }) => ({ role, content })),
      ],
      api_key: apiKey.value,
      model_name: model.value,
    });
    const reply = data?.choices?.[0]?.message?.content || data?.error || "[No response]";
    chatHistory.value[idx] = newMessage("assistant", reply);
    await speakReplySequentially(reply);
  } catch (e) {
    console.error(e);
    chatHistory.value[idx] = newMessage(
      "assistant",
      "❌ Sorry, an error occurred. Please try again."
    );
  } finally {
    isLoading.value = false;
    avatarState.value = "idle";
  }
}
</script>
