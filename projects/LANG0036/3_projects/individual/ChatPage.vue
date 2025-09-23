<template>
  <div
    v-if="selectedBot"
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800"
  >
    <!-- Sidebar -->
    <LeftSidebar
      v-bind="{
        isOpen: isSidebarOpen,
        systemPrompt,
        welcomePrompt,
        model,
        apiKey,
        isConnected,
        tokenUsage,
        selectedProvider,
        isConnecting,
      }"
      @update:isOpen="isSidebarOpen = $event"
      @update:apiKey="apiKey = $event"
      @update:model="model = $event"
      @update:selectedProvider="selectedProvider = $event"
      @connectAPI="connectAPI"
      @clearAPI="clearAPI"
    />

    <!-- Main Chat -->
    <div class="flex flex-col flex-1 bg-white shadow-lg overflow-hidden">
      <!-- Header -->
      <div
        class="chat-header flex justify-between items-center p-5 bg-gradient-to-r from-indigo-500 to-purple-600 text-white"
      >
        <div>
          <h1 class="text-xl font-bold">{{ selectedBot.name }}</h1>
          <div class="text-sm opacity-80">💬 Text Chat with your AI assistant</div>
        </div>
        <div class="flex gap-2">
          <button
            class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30"
            @click="isSidebarOpen = !isSidebarOpen"
          >
            {{ isSidebarOpen ? "⬅ Hide Left" : "➡ Show Left" }}
          </button>
          <button
            class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30"
            @click="startNewSession"
          >
            🔄 New Session
          </button>
          <button class="px-3 py-1 rounded-lg bg-white/20 hover:bg-white/30" @click="goBack">
            ⬅ Back
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div ref="chatMessages" class="chat-messages flex-1 overflow-y-auto p-5 space-y-4">
        <div
          v-for="(msg, i) in chatHistory"
          :key="i"
          class="flex"
          :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
        >
          <div
            class="max-w-lg md:max-w-md lg:max-w-lg px-4 py-3 rounded-2xl shadow text-base break-words"
            :class="msgClasses(msg, i)"
          >
            <div class="font-semibold text-xs mb-1">
              {{ msgSenderLabel(msg.role) }}
            </div>
            <div
              class="prose prose-sm max-w-none break-words [&_pre]:whitespace-pre-wrap [&_pre]:break-words [&_code]:whitespace-pre-wrap [&_ol]:list-decimal [&_ol]:ml-6 [&_ul]:list-disc"
              v-html="renderMarkdown(msg.content)"
            />
            <div class="text-xs text-gray-400 mt-2 text-right">
              {{ msg.timestamp.toLocaleTimeString() }}
            </div>
          </div>
        </div>
      </div>

      <!-- Input -->
      <div class="chat-input-container p-4 border-t bg-gray-50 relative">
        <!-- ✨ Input Overlay Update -->
        <div
          v-if="!isConnected && selectedProvider === 'hkbu'"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect your HKBU API key first
        </div>
        <div
          v-else-if="!isConnected && selectedProvider === 'openrouter'"
          class="absolute inset-0 flex items-center justify-center bg-white/70 text-gray-600 text-sm font-medium z-10"
        >
          🔑 Please connect to Open Router first
        </div>

        <div class="flex items-end space-x-2">
          <textarea
            ref="chatInput"
            v-model="userText"
            @keydown.enter.exact.prevent="sendTextToChatbot"
            @keydown.shift.enter.stop
            rows="1"
            placeholder="Type your message..."
            class="flex-1 p-3 rounded-2xl border border-gray-300 focus:ring-2 focus:ring-indigo-500 resize-none disabled:bg-gray-100"
            :disabled="!isConnected || isLoading"
            @input="autoResize"
          ></textarea>

          <button
            class="px-6 py-3 rounded-full bg-indigo-600 text-white font-bold shadow-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
            @click="sendTextToChatbot"
            :disabled="!isConnected || !userText.trim() || isLoading"
          >
            Send
          </button>

          <button
            class="px-4 py-2 rounded-lg bg-green-600 text-white hover:bg-green-700 disabled:bg-gray-300 disabled:cursor-not-allowed shadow transition transform hover:scale-105"
            @click="showReport = true"
            :disabled="!chatHistory.length"
            title="Finish & View Report"
          >
            ✓
          </button>
        </div>
      </div>

      <!-- Report -->
      <ReportModal
        v-bind="{
          show: showReport,
          chatHistory,
          reportGenerationInstructions,
          bccEmail,
          ccEmail,
        }"
        @close="showReport = false"
      />
    </div>
  </div>

  <!-- Loading -->
  <div
    v-else
    class="flex h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 items-center justify-center"
  >
    <div class="flex items-center space-x-3">
      <svg
        class="animate-spin h-8 w-8 text-white"
        xmlns="http://www.w3.org/2000/svg"
        fill="none"
        viewBox="0 0 24 24"
      >
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
        <path
          class="opacity-75"
          fill="currentColor"
          d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
        />
      </svg>
      <span class="text-white text-2xl font-semibold">Loading Chatbot...</span>
    </div>
  </div>
  <!-- Notification -->
  <div
    v-if="notification.visible"
    class="fixed top-5 right-5 z-50 px-4 py-3 rounded-lg shadow-lg text-white"
    :class="notification.type === 'success' ? 'bg-green-500' : 'bg-red-500'"
  >
    {{ notification.message }}
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { useChatbotStore } from "../components/chatbotStore";
import { BASE_URL } from "../components/base_url";
import LeftSidebar from "../components/text_chatbot/LeftSidebar.vue";
import ReportModal from "../components/ReportModal.vue";
import MarkdownIt from "markdown-it";

// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});

const props = defineProps({ botId: String });
const router = useRouter();
const chatbotStore = useChatbotStore();

const selectedBot = computed(() => chatbotStore.availableBots.find((b) => b.id === props.botId));

const chatHistory = ref([]);
const apiKey = ref("");
const systemPrompt = ref("");
const welcomePrompt = ref("");
const model = ref("");
const reportGenerationInstructions = ref("");
const bccEmail = ref([]);
const ccEmail = ref([]);
const isConnected = ref(false);
const isSidebarOpen = ref(true);
const userText = ref("");
const isLoading = ref(false);
const isConnecting = ref(false);
const showReport = ref(false);
const selectedProvider = ref("hkbu");

const chatMessages = ref(null);
const chatInput = ref(null);
const notification = ref({ message: "", type: "success", visible: false });

function showNotification(msg, type = "success") {
  notification.value = { message: msg, type, visible: true };
  setTimeout(() => (notification.value.visible = false), 3000);
}

function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  });
}
function focusInput() {
  nextTick(() => {
    chatInput.value?.focus();
  });
}
function renderMarkdown(text) {
  return markdown.render(text || "");
}

const tokenUsage = computed(() => {
  let total = 0;
  chatHistory.value.forEach((m, i) => {
    if (m.role === "user") total += m.content?.length || 0;
    if (
      m.role === "assistant" &&
      i !== chatHistory.value.findIndex((x) => x.role === "assistant")
    ) {
      total += m.content?.length || 0;
    }
  });
  return Math.floor((total * 3) / 4);
});

onMounted(async () => {
  await chatbotStore.loadBots();
  if (!selectedBot.value) return router.push("/");

  ({
    systemPrompt: systemPrompt.value,
    welcomePrompt: welcomePrompt.value,
    model: model.value,
    reportGenerationInstructions: reportGenerationInstructions.value,
    bccEmail: bccEmail.value,
    ccEmail: ccEmail.value,
  } = selectedBot.value);

  const savedApiKey = localStorage.getItem("chatbot_api_key");
  if (savedApiKey) {
    apiKey.value = savedApiKey;
    connectAPI(true);
  }
  focusInput();
});

const goBack = () => router.push("/");

async function connectAPI(auto = false) {
  if (selectedProvider.value === "openrouter") {
    isConnected.value = true;
  } else {
    if (!apiKey.value && !auto) return;
    localStorage.setItem("chatbot_api_key", apiKey.value);
    isConnected.value = true;
  }
  isConnecting.value = true;
  // 🔍 test provider connection by sending a dummy message
  try {
    let providerUrl = "";
    if (selectedProvider.value === "hkbu") {
      providerUrl = `${BASE_URL}/chatbot/chat`;
    } else if (selectedProvider.value === "openrouter") {
      providerUrl = `${BASE_URL}/chatbot/chat_openrouter`;
    }

    const res = await fetch(providerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history: [
          { role: "system", content: "connection test, return 1 if you can read the text." },
          { role: "user", content: "Hello!" },
        ],
        api_key: apiKey.value,
        model_name: model.value,
      }),
    });

    const data = await res.json();

    // ✅ check if provider replied with content
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";

    if (reply && reply.trim().length > 0) {
      showNotification("✅ Connected and working!", "success");
    } else {
      showNotification("⚠️ Connected, but no valid reply received.", "error");
      isConnected.value = false;
    }
  } catch (err) {
    console.error(err);
    showNotification("❌ Failed to connect.", "error");
    isConnected.value = false;
  } finally {
    isConnecting.value = false;
  }

  // welcome message only if chat is empty
  if (!chatHistory.value.length && isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}

function clearAPI() {
  if (selectedProvider.value === "hkbu") {
    localStorage.removeItem("chatbot_api_key");
    apiKey.value = "";
  }
  isConnected.value = false;
  chatHistory.value = [];
}

function startNewSession() {
  chatHistory.value = [];
  if (isConnected.value) {
    chatHistory.value.push(newMessage("assistant", welcomePrompt.value));
    scrollToBottom();
  }
}

async function sendTextToChatbot() {
  if (!userText.value.trim()) return;
  chatHistory.value.push(newMessage("user", userText.value));
  userText.value = "";
  scrollToBottom();
  focusInput();

  chatHistory.value.push(newMessage("assistant", "⏳ Thinking..."));
  const idx = chatHistory.value.length - 1;
  scrollToBottom();

  isLoading.value = true;
  try {
    let providerUrl = "";
    if (selectedProvider.value == "hkbu") {
      providerUrl = `${BASE_URL}/chatbot/chat`;
    } else if (selectedProvider.value == "openrouter") {
      providerUrl = `${BASE_URL}/chatbot/chat_openrouter`;
    }
    const res = await fetch(providerUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        chat_history: [
          { role: "system", content: systemPrompt.value }, // wrap systemPrompt as system role
          ...chatHistory.value.map(({ role, content }) => ({
            role,
            content,
          })),
        ],
        api_key: apiKey.value,
        model_name: model.value,
      }),
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);

    const data = await res.json();
    chatHistory.value[idx] = newMessage(
      "assistant",
      data?.choices?.[0]?.message?.content || data?.error || "[No response]"
    );
  } catch (e) {
    console.error(e);
    chatHistory.value[idx] = newMessage(
      "assistant",
      "❌ Sorry, an error occurred. Please try again."
    );
  } finally {
    isLoading.value = false;
    scrollToBottom();
    focusInput();
  }
}

const newMessage = (role, content) => ({
  role,
  content,
  timestamp: new Date(),
});
const msgSenderLabel = (role) => (role === "user" ? "👤 You" : "🤖 Assistant");
const msgClasses = (msg) =>
  msg.role === "user"
    ? "bg-gradient-to-r from-indigo-500 to-purple-600 text-white rounded-br-none"
    : "bg-gray-100 border border-gray-200 text-gray-800 rounded-bl-none";
</script>
