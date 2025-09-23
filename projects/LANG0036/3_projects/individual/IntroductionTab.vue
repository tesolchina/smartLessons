<template>
  <div class="space-y-8">
    <!-- Welcome Section with Gradient Background -->
    <div class="relative overflow-hidden rounded-2xl bg-gradient-to-br from-purple-600 via-blue-600 to-cyan-500 text-white">
      <div class="absolute inset-0 bg-black/10"></div>
      <div class="relative px-8 py-12 text-center">
        <div class="mb-6">
          <div class="inline-flex items-center justify-center w-20 h-20 bg-white/20 rounded-full mb-4 backdrop-blur-sm">
            <span class="text-3xl">🤖</span>
          </div>
          <h2 class="text-4xl font-bold mb-4">Welcome to GCAP3226 AI Tutoring System</h2>
          <p class="text-xl text-white/90 max-w-3xl mx-auto leading-relaxed">
            Your personalized AI tutors are here to guide you through data governance and public policy analysis. 
            Get ready to transform how you approach citizen empowerment through data!
          </p>
        </div>
        <div class="flex justify-center space-x-4">
          <div class="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 text-sm font-medium">
            <span class="text-yellow-300">✨</span> AI-Powered Learning
          </div>
          <div class="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 text-sm font-medium">
            <span class="text-green-300">📊</span> Data Governance Focus
          </div>
          <div class="bg-white/10 backdrop-blur-sm rounded-full px-4 py-2 text-sm font-medium">
            <span class="text-blue-300">🏛️</span> Policy Analysis
          </div>
        </div>
      </div>
    </div>

    <!-- Course Context with Enhanced Design -->
    <div class="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-xl p-8 border border-blue-100">
      <div class="flex items-center mb-6">
        <div class="bg-blue-500 rounded-lg p-3 mr-4">
          <span class="text-2xl text-white">🎓</span>
        </div>
        <h3 class="text-2xl font-bold text-blue-900">Course Context: Empowering Citizens through Data</h3>
      </div>
      <div class="grid md:grid-cols-2 gap-6">
        <div class="bg-white rounded-lg p-6 shadow-sm border border-blue-100">
          <h4 class="text-lg font-semibold text-blue-800 mb-4 flex items-center">
            <span class="text-blue-500 mr-2">📚</span>
            What You'll Learn
          </h4>
          <ul class="space-y-3 text-blue-700">
            <li class="flex items-start">
              <div class="bg-blue-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-blue-600 text-xs">●</span>
              </div>
              <span>Data governance principles and frameworks</span>
            </li>
            <li class="flex items-start">
              <div class="bg-blue-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-blue-600 text-xs">●</span>
              </div>
              <span>Public policy analysis through data</span>
            </li>
            <li class="flex items-start">
              <div class="bg-blue-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-blue-600 text-xs">●</span>
              </div>
              <span>Hong Kong government data transparency assessment</span>
            </li>
            <li class="flex items-start">
              <div class="bg-blue-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-blue-600 text-xs">●</span>
              </div>
              <span>Community engagement through data visualization</span>
            </li>
          </ul>
        </div>
        <div class="bg-white rounded-lg p-6 shadow-sm border border-blue-100">
          <h4 class="text-lg font-semibold text-blue-800 mb-4 flex items-center">
            <span class="text-blue-500 mr-2">🎯</span>
            Available Topics
          </h4>
          <ul class="space-y-3 text-blue-700">
            <li class="flex items-start">
              <div class="bg-green-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-green-600 text-xs">♻️</span>
              </div>
              <span>Municipal Solid Waste Charging Scheme</span>
            </li>
            <li class="flex items-start">
              <div class="bg-orange-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-orange-600 text-xs">🚌</span>
              </div>
              <span>Bus Route Optimization & Coordination</span>
            </li>
            <li class="flex items-start">
              <div class="bg-emerald-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-emerald-600 text-xs">🌱</span>
              </div>
              <span>Green Community Recycling Networks</span>
            </li>
            <li class="flex items-start">
              <div class="bg-purple-100 rounded-full w-6 h-6 flex items-center justify-center mr-3 mt-0.5">
                <span class="text-purple-600 text-xs">🌪️</span>
              </div>
              <span>Typhoon Signal Data Analysis</span>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <!-- How It Works - Enhanced with Colors -->
    <div class="grid md:grid-cols-3 gap-8">
      <div class="group hover:scale-105 transition-all duration-300">
        <div class="bg-gradient-to-br from-green-400 to-emerald-500 rounded-2xl p-8 text-white text-center shadow-lg">
          <div class="bg-white/20 backdrop-blur-sm rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
            <span class="text-3xl">📤</span>
          </div>
          <h4 class="text-xl font-bold mb-4">Share Your Context</h4>
          <p className="text-white/90 leading-relaxed">Upload your project materials, data, and research questions to your AI tutor</p>
        </div>
      </div>
      <div class="group hover:scale-105 transition-all duration-300">
        <div class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl p-8 text-white text-center shadow-lg">
          <div class="bg-white/20 backdrop-blur-sm rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
            <span class="text-3xl">🔍</span>
          </div>
          <h4 class="text-xl font-bold mb-4">Get Guided Analysis</h4>
          <p className="text-white/90 leading-relaxed">Receive personalized guidance on data governance assessment and policy analysis</p>
        </div>
      </div>
      <div class="group hover:scale-105 transition-all duration-300">
        <div class="bg-gradient-to-br from-purple-500 to-pink-500 rounded-2xl p-8 text-white text-center shadow-lg">
          <div class="bg-white/20 backdrop-blur-sm rounded-full w-20 h-20 flex items-center justify-center mx-auto mb-6">
            <span class="text-3xl">💡</span>
          </div>
          <h4 class="text-xl font-bold mb-4">Develop Insights</h4>
          <p className="text-white/90 leading-relaxed">Transform your analysis into actionable recommendations for citizen empowerment</p>
        </div>
      </div>
    </div>

    <!-- API Key Setup with Enhanced Design -->
    <div class="bg-gradient-to-r from-amber-50 to-orange-50 border-2 border-amber-200 rounded-xl overflow-hidden">
      <div class="bg-gradient-to-r from-amber-400 to-orange-400 px-6 py-4">
        <h3 class="text-xl font-bold text-white flex items-center">
          <span class="mr-3 text-2xl">🔑</span>
          API Key Setup Required
        </h3>
      </div>
      <div class="p-6 space-y-6">
        <p class="text-amber-800 text-lg">
          To use the AI tutors, you'll need to set up your own API key. This ensures your conversations remain private and you have control over usage.
        </p>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-amber-200">
          <h4 class="font-bold text-amber-800 mb-4 flex items-center">
            <span class="bg-amber-100 rounded-full w-8 h-8 flex items-center justify-center mr-3">
              <span class="text-amber-600">📋</span>
            </span>
            Step-by-Step Setup:
          </h4>
          <ol class="space-y-4">
            <li class="flex items-start">
              <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-4 mt-0.5 font-bold text-sm">1</div>
              <span class="text-amber-700">Visit <a href="https://platform.openai.com/api-keys" class="text-blue-600 hover:text-blue-800 underline font-medium" target="_blank">OpenAI API Keys</a></span>
            </li>
            <li class="flex items-start">
              <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-4 mt-0.5 font-bold text-sm">2</div>
              <span class="text-amber-700">Create a new API key (keep it secure!)</span>
            </li>
            <li class="flex items-start">
              <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-4 mt-0.5 font-bold text-sm">3</div>
              <span class="text-amber-700">Go to the "AI Tutors" tab and enter your API key</span>
            </li>
            <li class="flex items-start">
              <div class="bg-gradient-to-r from-blue-500 to-blue-600 text-white rounded-full w-8 h-8 flex items-center justify-center mr-4 mt-0.5 font-bold text-sm">4</div>
              <span class="text-amber-700">Start your personalized tutoring session!</span>
            </li>
          </ol>
        </div>

        <div class="bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-lg p-4">
          <div class="flex items-start">
            <div class="bg-red-100 rounded-full w-8 h-8 flex items-center justify-center mr-3 mt-0.5">
              <span class="text-red-600">🔒</span>
            </div>
            <div>
              <p class="text-red-800 text-sm font-medium mb-1">Privacy Note:</p>
              <p class="text-red-700 text-sm">
                Your API key and conversations are stored locally in your browser. 
                They are never sent to our servers. You maintain full control over your data.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Getting Started with Call-to-Action -->
    <div class="text-center bg-gradient-to-r from-gray-50 to-blue-50 rounded-xl p-8">
      <div class="mb-6">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mb-4">
          <span class="text-2xl text-white">🚀</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-4">Ready to Get Started?</h3>
        <p class="text-gray-600 mb-6 max-w-2xl mx-auto leading-relaxed">
          Tomorrow you'll be guided to write up a comprehensive project plan. 
          Your AI tutor will help you assess data governance practices of the Hong Kong government.
        </p>
      </div>
      <button 
        @click="$emit('switchTab', 'tutors')"
        class="group bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold py-4 px-8 rounded-xl transition-all duration-300 transform hover:scale-105 shadow-lg hover:shadow-xl"
      >
        <span class="flex items-center">
          Access AI Tutors 
          <span class="ml-2 group-hover:translate-x-1 transition-transform duration-300">→</span>
        </span>
      </button>
    </div>
  </div>
</template>

<script setup>
// Component for the introduction and setup instructions
defineEmits(['switchTab'])
</script>