<template>
  <div class="flex h-screen items-center justify-center bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 text-gray-800">
    <div class="bg-white/90 backdrop-blur-xl p-10 rounded-2xl shadow-2xl space-y-6 w-full max-w-lg">
      <h1 class="text-2xl font-bold text-center text-indigo-700">
        🤖 Choose Your Chatbot
      </h1>
      <p class="text-center text-gray-500">
        Select a chatbot to start a conversation.
      </p>

      <!-- Mode Toggle -->
      <div class="flex justify-center items-center space-x-2">
        <span :class="['font-semibold transition-colors', isAvatarMode ? 'text-gray-400' : 'text-indigo-700']">Chatbot</span>
        <button
          @click="toggleMode"
          :class="['relative inline-flex h-6 w-11 items-center rounded-full transition-colors', isAvatarMode ? 'bg-purple-600' : 'bg-gray-200']"
        >
          <span
            :class="['inline-block h-4 w-4 transform rounded-full bg-white transition-transform', isAvatarMode ? 'translate-x-6' : 'translate-x-1']"
          ></span>
        </button>
        <span :class="['font-semibold transition-colors', isAvatarMode ? 'text-purple-700' : 'text-gray-400']">Avatar</span>
      </div>

      <!-- Bot List -->
      <div class="space-y-4">
        <button
          v-for="bot in paginatedBots"
          :key="bot.id"
          :class="['w-full p-5 rounded-xl bg-gradient-to-r text-white font-semibold shadow hover:opacity-90 transition', bot.styleClass]"
          @click="chooseBot(bot)"
        >
          {{ bot.name }}
        </button>
      </div>

      <!-- Pagination Controls -->
      <div v-if="totalPages > 1" class="flex justify-center items-center space-x-2 pt-4">
        <button
          @click="prevPage"
          :disabled="currentPage === 1"
          class="px-3 py-1 rounded-lg bg-indigo-600 text-white disabled:opacity-40"
        >
          Prev
        </button>

        <div class="flex space-x-1">
          <button
            v-for="page in totalPages"
            :key="page"
            @click="goToPage(page)"
            :class="['px-3 py-1 rounded-lg',
              page === currentPage
                ? 'bg-purple-600 text-white'
                : 'bg-gray-200 hover:bg-gray-300']"
          >
            {{ page }}
          </button>
        </div>

        <button
          @click="nextPage"
          :disabled="currentPage === totalPages"
          class="px-3 py-1 rounded-lg bg-indigo-600 text-white disabled:opacity-40"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useChatbotStore } from '../components/chatbotStore';

const router = useRouter();
const chatbotStore = useChatbotStore();

// Toggle state
const isAvatarMode = ref(false);

// Pagination state
const currentPage = ref(1);
const itemsPerPage = 6; // adjust how many bots per page

// Load bots
onMounted(() => {
  chatbotStore.loadBots();
});

// Toggle Chatbot/Avatar mode
function toggleMode() {
  isAvatarMode.value = !isAvatarMode.value;
}

// Go to bot
function chooseBot(bot) {
  if (isAvatarMode.value) {
    router.push({ name: 'Avatar', params: { avatarId: bot.id } });
  } else {
    router.push({ name: 'Chat', params: { botId: bot.id } });
  }
}

// Computed pagination
const totalPages = computed(() =>
  Math.ceil(chatbotStore.availableBots.length / itemsPerPage)
);

const paginatedBots = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return chatbotStore.availableBots.slice(start, end);
});

// Navigation functions
function prevPage() {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
}
function nextPage() {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
}
function goToPage(page) {
  currentPage.value = page;
}
</script>
