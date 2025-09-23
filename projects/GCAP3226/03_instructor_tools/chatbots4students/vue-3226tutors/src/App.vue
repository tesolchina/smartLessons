<script setup>
import { ref } from 'vue'
import IntroductionTab from './components/IntroductionTab.vue'
import TutorsTab from './components/TutorsTab.vue'

const activeTab = ref('introduction')
</script>

<template>
  <div id="app">
    <div class="bg-white text-gray-900 min-h-screen">
      <!-- Header with Enhanced Gradient -->
      <div class="bg-gradient-to-r from-purple-600 via-blue-600 to-cyan-500 text-white py-8 relative overflow-hidden">
        <div class="absolute inset-0 bg-black/10"></div>
        <div class="container mx-auto max-w-6xl px-4 relative">
          <div class="flex items-center space-x-4 mb-3">
            <div class="bg-white/20 backdrop-blur-sm rounded-xl p-3">
              <span class="text-3xl">🤖</span>
            </div>
            <h1 class="text-4xl font-bold">GCAP3226 AI Tutoring System</h1>
          </div>
          <p class="text-blue-100 text-lg">Empowering Citizens through Data - AI-Powered Learning Support</p>
        </div>
      </div>

      <!-- Navigation Tabs -->
      <div class="border-b border-gray-200">
        <nav class="container mx-auto max-w-6xl px-4">
          <div class="flex space-x-8">
            <button
              @click="activeTab = 'introduction'"
              :class="activeTab === 'introduction' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
            >
              Introduction & Setup
            </button>
            <button
              @click="activeTab = 'tutors'"
              :class="activeTab === 'tutors' ? 'border-blue-500 text-blue-600' : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'"
              class="whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm"
            >
              AI Tutors
            </button>
          </div>
        </nav>
      </div>

      <!-- Tab Content -->
      <div class="container mx-auto max-w-6xl px-4 py-8">
        <!-- Introduction Tab -->
        <div v-if="activeTab === 'introduction'" class="space-y-8">
          <IntroductionTab />
        </div>

        <!-- Tutors Tab -->
        <div v-if="activeTab === 'tutors'" class="space-y-8">
          <TutorsTab />
        </div>
      </div>
    </div>
  </div>
</template>

<style>
#app {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
