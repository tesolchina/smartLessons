<template>
  <div class="space-y-8">
    <!-- API Key Input with Enhanced Design -->
    <div class="bg-gradient-to-r from-gray-50 to-blue-50 rounded-2xl p-8 border border-gray-200">
      <div class="flex items-center mb-6">
        <div class="bg-gradient-to-r from-blue-500 to-purple-600 rounded-xl p-3 mr-4">
          <span class="text-2xl text-white">🔑</span>
        </div>
        <h3 class="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          API Key Configuration
        </h3>
      </div>
      <div class="flex flex-col md:flex-row gap-4">
        <div class="flex-1">
          <input
            v-model="apiKey"
            type="password"
            placeholder="Enter your OpenAI API Key (sk-...)"
            class="w-full px-6 py-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200 text-lg"
            @input="saveApiKey"
          />
        </div>
        <button
          @click="testApiKey"
          :disabled="!apiKey || isTestingKey"
          class="px-8 py-4 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-xl transition-all duration-200 transform hover:scale-105 disabled:scale-100"
        >
          <span v-if="isTestingKey" class="flex items-center">
            <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Testing...
          </span>
          <span v-else>Test Key</span>
        </button>
      </div>
      <div v-if="apiKeyStatus" class="mt-4">
        <div 
          :class="apiKeyStatus.type === 'success' 
            ? 'bg-green-50 border border-green-200 text-green-800' 
            : 'bg-red-50 border border-red-200 text-red-800'"
          class="rounded-lg p-4 flex items-center"
        >
          <span v-if="apiKeyStatus.type === 'success'" class="text-green-500 mr-3">✅</span>
          <span v-else class="text-red-500 mr-3">❌</span>
          <span class="font-medium">{{ apiKeyStatus.message }}</span>
        </div>
      </div>
    </div>

    <!-- Tutor Selection with Enhanced Cards -->
    <div v-if="apiKey && apiKeyValid">
      <div class="text-center mb-8">
        <h3 class="text-3xl font-bold bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent mb-4">
          Choose Your AI Tutor
        </h3>
        <p class="text-gray-600 text-lg">Select the specialist that best matches your current needs</p>
      </div>
      
      <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mb-8">
        <!-- Data Governance Tutor -->
        <div 
          @click="selectTutor('data-governance')"
          :class="[
            selectedTutor === 'data-governance' 
              ? `ring-4 ${tutorConfigs['data-governance'].ringColor} ${tutorConfigs['data-governance'].bgColor}` 
              : 'hover:shadow-xl hover:scale-105',
            'group cursor-pointer transition-all duration-300 transform'
          ]"
          class="bg-white border-2 border-amber-200 rounded-2xl p-6 shadow-lg"
        >
          <div class="text-center">
            <div class="bg-gradient-to-br from-amber-500 to-rose-500 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-3xl text-white">🏛️</span>
            </div>
            <h4 class="text-xl font-bold text-gray-900 mb-3">Data Governance Expert</h4>
            <p class="text-gray-600 text-sm mb-4 leading-relaxed">
              Government transparency & policy analysis specialist
            </p>
            <div class="bg-gradient-to-r from-amber-100 to-rose-100 text-amber-800 px-4 py-2 rounded-full text-xs font-semibold">
              Perfect for: Policy research, transparency assessment
            </div>
          </div>
        </div>

        <!-- Statistical Analysis Tutor -->
        <div 
          @click="selectTutor('statistical-analysis')"
          :class="[
            selectedTutor === 'statistical-analysis' 
              ? `ring-4 ${tutorConfigs['statistical-analysis'].ringColor} ${tutorConfigs['statistical-analysis'].bgColor}` 
              : 'hover:shadow-xl hover:scale-105',
            'group cursor-pointer transition-all duration-300 transform'
          ]"
          class="bg-white border-2 border-blue-200 rounded-2xl p-6 shadow-lg"
        >
          <div class="text-center">
            <div class="bg-gradient-to-br from-blue-500 to-indigo-600 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-3xl text-white">📊</span>
            </div>
            <h4 class="text-xl font-bold text-gray-900 mb-3">Statistical Analysis Guide</h4>
            <p class="text-gray-600 text-sm mb-4 leading-relaxed">
              Data analysis, visualization & statistical modeling expert
            </p>
            <div class="bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-800 px-4 py-2 rounded-full text-xs font-semibold">
              Perfect for: Data analysis, survey insights, modeling
            </div>
          </div>
        </div>

        <!-- Community Engagement Tutor -->
        <div 
          @click="selectTutor('community-engagement')"
          :class="[
            selectedTutor === 'community-engagement' 
              ? `ring-4 ${tutorConfigs['community-engagement'].ringColor} ${tutorConfigs['community-engagement'].bgColor}` 
              : 'hover:shadow-xl hover:scale-105',
            'group cursor-pointer transition-all duration-300 transform'
          ]"
          class="bg-white border-2 border-emerald-200 rounded-2xl p-6 shadow-lg"
        >
          <div class="text-center">
            <div class="bg-gradient-to-br from-emerald-500 to-teal-500 rounded-2xl w-20 h-20 flex items-center justify-center mx-auto mb-6 group-hover:scale-110 transition-transform duration-300">
              <span class="text-3xl text-white">🤝</span>
            </div>
            <h4 class="text-xl font-bold text-gray-900 mb-3">Community Impact Advisor</h4>
            <p class="text-gray-600 text-sm mb-4 leading-relaxed">
              Citizen empowerment & public engagement strategist
            </p>
            <div class="bg-gradient-to-r from-emerald-100 to-teal-100 text-emerald-800 px-4 py-2 rounded-full text-xs font-semibold">
              Perfect for: Public engagement, impact assessment
            </div>
          </div>
        </div>
        
        <!-- Future bots can be easily added here following the same pattern -->
        <!-- Just copy one of the above blocks and modify the:
             - tutorId in @click and :class
             - colors (styleClass, borderColor, ringColor, bgColor)
             - emoji, name, description, and use case text
        -->
      </div>

      <!-- Chat Interface with Enhanced Design -->
      <div v-if="selectedTutor" class="bg-white border border-gray-200 rounded-2xl shadow-2xl overflow-hidden">
        <!-- Chat Header -->
        <div :class="`bg-gradient-to-r ${tutorConfigs[selectedTutor].styleClass}`" class="px-6 py-6 text-white">
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-white/20 backdrop-blur-sm rounded-xl flex items-center justify-center">
                <span class="text-2xl">{{ getTutorEmoji(selectedTutor) }}</span>
              </div>
              <div>
                <h4 class="font-bold text-lg">{{ getTutorName(selectedTutor) }}</h4>
                <p class="text-white/90 text-sm">{{ getTutorDescription(selectedTutor) }}</p>
              </div>
            </div>
            <button 
              @click="clearChat"
              class="bg-white/20 hover:bg-white/30 backdrop-blur-sm rounded-lg px-4 py-2 text-sm font-medium transition-colors duration-200"
            >
              Clear Chat
            </button>
          </div>
        </div>

        <!-- Chat Messages -->
        <div class="h-96 overflow-y-auto p-6 space-y-4 bg-gray-50" ref="chatContainer">
          <div v-if="chatMessages.length === 0" class="text-center py-12">
            <div class="mb-6">
              <div :class="`bg-gradient-to-br ${tutorConfigs[selectedTutor].styleClass}`" class="w-16 h-16 rounded-2xl flex items-center justify-center mx-auto mb-4">
                <span class="text-2xl text-white">{{ getTutorEmoji(selectedTutor) }}</span>
              </div>
              <div class="bg-white rounded-2xl p-6 shadow-sm border border-gray-200 max-w-md mx-auto">
                <p class="text-gray-700 mb-2">
                  👋 Hi! I'm your <strong>{{ getTutorName(selectedTutor) }}</strong>.
                </p>
                <p class="text-gray-600 text-sm">
                  Share your project context, data, or any questions about data governance and I'll help guide your analysis!
                </p>
              </div>
            </div>
          </div>
          
          <div 
            v-for="(message, index) in chatMessages" 
            :key="index"
            :class="message.type === 'user' ? 'flex justify-end' : 'flex justify-start'"
          >
            <div 
              :class="message.type === 'user' 
                ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white ml-12' 
                : 'bg-white text-gray-900 mr-12 border border-gray-200'"
              class="max-w-xs lg:max-w-md px-6 py-4 rounded-2xl shadow-sm"
            >
              <p class="text-sm whitespace-pre-wrap leading-relaxed">{{ message.content }}</p>
              <p :class="message.type === 'user' ? 'text-blue-100' : 'text-gray-500'" class="text-xs mt-2 font-medium">
                {{ formatTime(message.timestamp) }}
              </p>
            </div>
          </div>

          <div v-if="isTyping" class="flex justify-start">
            <div class="bg-white text-gray-900 mr-12 border border-gray-200 max-w-xs lg:max-w-md px-6 py-4 rounded-2xl shadow-sm">
              <div class="flex items-center space-x-2">
                <div class="flex space-x-1">
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                  <div class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                </div>
                <span class="text-xs text-gray-500">{{ getTutorName(selectedTutor) }} is typing...</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Chat Input -->
        <div class="border-t border-gray-200 p-6 bg-white">
          <div class="flex space-x-4">
            <input
              v-model="userMessage"
              @keypress.enter="sendMessage"
              type="text"
              placeholder="Type your message about data governance, your project, or ask any questions..."
              class="flex-1 px-6 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-colors duration-200"
            />
            <button
              @click="sendMessage"
              :disabled="!userMessage.trim() || isTyping"
              class="px-8 py-3 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 disabled:from-gray-400 disabled:to-gray-500 text-white font-medium rounded-xl transition-all duration-200 transform hover:scale-105 disabled:scale-100"
            >
              Send
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- No API Key Message with Enhanced Design -->
    <div v-else class="text-center py-16">
      <div class="max-w-md mx-auto">
        <div class="bg-gradient-to-br from-blue-100 to-purple-100 rounded-full w-24 h-24 flex items-center justify-center mx-auto mb-6">
          <span class="text-4xl">🔒</span>
        </div>
        <h3 class="text-2xl font-bold text-gray-900 mb-3">API Key Required</h3>
        <p class="text-gray-600 mb-6 leading-relaxed">
          Please enter your OpenAI API key above to unlock the full power of our AI tutoring system.
        </p>
        <div class="bg-blue-50 border border-blue-200 rounded-xl p-4">
          <p class="text-blue-800 text-sm">
            <span class="font-semibold">🛡️ Your Privacy:</span> All conversations are processed securely and stored locally in your browser.
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'

// Reactive data
const apiKey = ref('')
const apiKeyValid = ref(false)
const apiKeyStatus = ref(null)
const isTestingKey = ref(false)
const selectedTutor = ref('')
const userMessage = ref('')
const isTyping = ref(false)
const chatMessages = reactive([])
const chatContainer = ref(null)

// Tutor configurations with enhanced styling
const tutorConfigs = {
  'data-governance': {
    name: 'Data Governance Expert',
    emoji: '🏛️',
    description: 'Government transparency & policy analysis specialist',
    styleClass: 'from-amber-500 to-rose-500',
    bgColor: 'bg-gradient-to-br from-amber-50 to-rose-50',
    borderColor: 'border-amber-200',
    ringColor: 'ring-amber-500',
    systemPrompt: `You are a Data Governance Expert helping GCAP3226 students analyze Hong Kong government data transparency and policy effectiveness. Your role is to guide students in:

1. Assessing data governance practices of Hong Kong government agencies
2. Evaluating transparency and accessibility of public data
3. Analyzing policy implementation through a data lens
4. Understanding institutional accountability and reporting practices

Focus on helping students develop critical thinking about:
- How data collection and disclosure affects public policy
- The role of transparency in citizen empowerment
- Evaluation frameworks for data governance
- Policy recommendations based on data analysis

Be encouraging, detailed, and practical in your guidance. Ask probing questions to help students think deeper about data governance implications.`
  },
  'statistical-analysis': {
    name: 'Statistical Analysis Guide',
    emoji: '📊',
    description: 'Data analysis, visualization & statistical modeling expert',
    styleClass: 'from-blue-500 to-indigo-600',
    bgColor: 'bg-gradient-to-br from-blue-50 to-indigo-50',
    borderColor: 'border-blue-200',
    ringColor: 'ring-blue-500',
    systemPrompt: `You are a Statistical Analysis Guide helping GCAP3226 students with data analysis, visualization, and statistical modeling for policy research. Your expertise includes:

1. Survey data analysis and interpretation
2. Regression modeling for policy insights
3. Data visualization best practices
4. Statistical significance and practical implications

Help students with:
- Analyzing survey responses and questionnaire data
- Creating meaningful visualizations for policy communication
- Understanding statistical relationships in governance data
- Interpreting results in the context of citizen empowerment

Be methodical, clear about statistical concepts, and always connect analysis back to policy implications and citizen impact.`
  },
  'community-engagement': {
    name: 'Community Impact Advisor',
    emoji: '🤝',
    description: 'Citizen empowerment & public engagement strategist',
    styleClass: 'from-emerald-500 to-teal-500',
    bgColor: 'bg-gradient-to-br from-emerald-50 to-teal-50',
    borderColor: 'border-emerald-200',
    ringColor: 'ring-emerald-500',
    systemPrompt: `You are a Community Impact Advisor helping GCAP3226 students understand how data governance affects citizen empowerment and community engagement. Your focus areas:

1. Citizen access to government data and information
2. Community-level impact of policy decisions
3. Public engagement strategies and effectiveness
4. Empowerment through data literacy and transparency

Guide students in:
- Evaluating how data practices affect different communities
- Understanding barriers to citizen participation in data governance
- Developing recommendations for improved public engagement
- Assessing the real-world impact of data transparency on citizens

Be empathetic, community-focused, and help students connect data governance to human impact and social justice.`
  }
}

// Lifecycle
onMounted(() => {
  loadApiKey()
})

// Methods
const saveApiKey = () => {
  localStorage.setItem('gcap3226-api-key', apiKey.value)
  apiKeyValid.value = false
  apiKeyStatus.value = null
}

const loadApiKey = () => {
  const savedKey = localStorage.getItem('gcap3226-api-key')
  if (savedKey) {
    apiKey.value = savedKey
    testApiKey()
  }
}

const testApiKey = async () => {
  if (!apiKey.value) return
  
  isTestingKey.value = true
  apiKeyStatus.value = null
  
  try {
    const response = await fetch('https://api.openai.com/v1/models', {
      headers: {
        'Authorization': `Bearer ${apiKey.value}`
      }
    })
    
    if (response.ok) {
      apiKeyValid.value = true
      apiKeyStatus.value = { type: 'success', message: '✅ API key is valid!' }
    } else {
      apiKeyValid.value = false
      apiKeyStatus.value = { type: 'error', message: '❌ Invalid API key. Please check and try again.' }
    }
  } catch (error) {
    apiKeyValid.value = false
    apiKeyStatus.value = { type: 'error', message: '❌ Error testing API key. Please check your connection.' }
  }
  
  isTestingKey.value = false
}

const selectTutor = (tutorId) => {
  selectedTutor.value = tutorId
  chatMessages.length = 0 // Clear messages when switching tutors
}

const getTutorName = (tutorId) => tutorConfigs[tutorId]?.name || ''
const getTutorEmoji = (tutorId) => tutorConfigs[tutorId]?.emoji || '🤖'
const getTutorDescription = (tutorId) => tutorConfigs[tutorId]?.description || ''

const getUseCaseText = (tutorId) => {
  const useCases = {
    'data-governance': 'Policy research, transparency assessment',
    'statistical-analysis': 'Data analysis, survey insights, modeling',
    'community-engagement': 'Public engagement, impact assessment'
  }
  return useCases[tutorId] || 'General guidance'
}

const sendMessage = async () => {
  if (!userMessage.value.trim() || isTyping.value) return
  
  const message = userMessage.value.trim()
  userMessage.value = ''
  
  // Add user message
  chatMessages.push({
    type: 'user',
    content: message,
    timestamp: new Date()
  })
  
  // Scroll to bottom
  await nextTick()
  scrollToBottom()
  
  // Start typing indicator
  isTyping.value = true
  
  try {
    const config = tutorConfigs[selectedTutor.value]
    const response = await fetch('https://api.openai.com/v1/chat/completions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey.value}`
      },
      body: JSON.stringify({
        model: 'gpt-4',
        messages: [
          { role: 'system', content: config.systemPrompt },
          ...chatMessages.filter(m => m.type === 'user' || m.type === 'assistant').map(m => ({
            role: m.type === 'user' ? 'user' : 'assistant',
            content: m.content
          }))
        ],
        max_tokens: 1000,
        temperature: 0.7
      })
    })
    
    const data = await response.json()
    
    if (data.choices && data.choices[0]) {
      chatMessages.push({
        type: 'assistant',
        content: data.choices[0].message.content,
        timestamp: new Date()
      })
    } else {
      chatMessages.push({
        type: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again.',
        timestamp: new Date()
      })
    }
  } catch (error) {
    console.error('Error:', error)
    chatMessages.push({
      type: 'assistant',
      content: 'I apologize, but I encountered a connection error. Please check your API key and try again.',
      timestamp: new Date()
    })
  }
  
  isTyping.value = false
  await nextTick()
  scrollToBottom()
}

const clearChat = () => {
  chatMessages.length = 0
}

const scrollToBottom = () => {
  if (chatContainer.value) {
    chatContainer.value.scrollTop = chatContainer.value.scrollHeight
  }
}

const formatTime = (timestamp) => {
  return timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}
</script>