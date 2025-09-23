<template>
  <aside
    class="bg-white/90 backdrop-blur shadow-xl flex flex-col transition-all duration-300 overflow-hidden"
    :class="isOpen ? 'w-80' : 'w-0'"
  >
    <!-- Header -->
    <div
      v-if="isOpen"
      class="p-5 border-b bg-gradient-to-r from-indigo-500 to-purple-600 text-white flex justify-between items-center"
    >
      <h2 class="text-lg font-bold flex items-center gap-2">🤖 Chatbot Configuration</h2>
      <button class="text-white hover:text-gray-200" @click="$emit('update:isOpen', false)">
        ✖
      </button>
    </div>

    <!-- Content -->
    <div v-if="isOpen" class="p-5 space-y-6 flex-1 overflow-y-auto">
      <!-- Provider Selector -->
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 class="font-semibold mb-3">🌐 Provider</h3>
        <select
          :value="selectedProvider"
          @change="$emit('update:selectedProvider', $event.target.value)"
          class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
        >
          <option value="openrouter">OpenRouter</option>
        </select>
      </div>

      <!-- Model Selector -->
      <div class="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <h3 class="font-semibold mb-3">🤖 Choose Model</h3>
        <select
          :value="model"
          @change="$emit('update:model', $event.target.value)"
          class="w-full border rounded-lg p-2 text-sm focus:ring focus:ring-indigo-300"
        >
          <option value="openai/gpt-4.1-nano">GPT-4.1 Nano</option>
          <option value="openai/gpt-4.1-mini">GPT-4.1 Mini</option>
          <option value="openai/gpt-5-chat">GPT-5 Chat</option>
          <option value="meta-llama/llama-4-scout">Llama-4 Scout</option>
          <option value="google/gemini-2.5-flash-lite-preview-06-17">Gemini-2.5 Flash</option>
          <option value="deepseek/deepseek-chat-v3.1:free">Deepseek V3.1</option>
        </select>
      </div>

      <!-- Buttons -->
      <div class="flex gap-2 mt-3">
        <button
          class="px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium"
          @click="$emit('connectAPI')"
          :disabled="isConnecting || isConnected"
        >
          <span v-if="isConnecting">🔄 Connecting...</span>
          <span v-else-if="isConnected">✔️ Connected</span>
          <span v-else>✅ Connect</span>
        </button>
        <button
          class="px-4 py-2 rounded-lg bg-gray-300 hover:bg-gray-400 text-gray-700 text-sm font-medium"
          @click="$emit('clearAPI')"
          :disabled="isConnecting"
        >
          🗑️ Clear
        </button>
      </div>

      <!-- Prompts -->
      <div>
        <h3 class="font-semibold mb-2">⚙️ System Prompt</h3>
        <div class="bg-gray-100 p-3 rounded-lg text-sm shadow-inner">
          {{ systemPrompt }}
        </div>
      </div>

      <!-- Token Usage -->
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4">
        <h3 class="font-semibold text-blue-800 mb-2">📊 Token Usage</h3>
        <p class="text-sm text-blue-900">
          Estimated tokens used:
          <span class="font-bold">{{ tokenUsage }}</span>
        </p>
      </div>
    </div>

    <!-- Footer -->
    <div v-if="isOpen" class="p-4 border-t text-xs text-gray-600 bg-gray-50 space-y-1">
      <div class="font-semibold text-gray-800">Created by:</div>
      <div>Dr. Simon Wang</div>
      <div>Innovation Officer, Language Centre</div>
      <div>Hong Kong Baptist University</div>
      <div>
        📧
        <a href="mailto:simonwang@hkbu.edu.hk" class="text-indigo-600 hover:underline">
          simonwang@hkbu.edu.hk
        </a>
      </div>
    </div>
  </aside>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  systemPrompt: String,
  welcomePrompt: String,
  model: String,
  apiKey: String,
  isConnected: Boolean,
  tokenUsage: Number,
  selectedProvider: String,
  isConnecting: Boolean,
});

defineEmits([
  "update:isOpen",
  "update:apiKey",
  "update:model",
  "update:selectedProvider",
  "connectAPI",
  "clearAPI",
]);
</script>
