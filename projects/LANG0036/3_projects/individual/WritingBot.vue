<template>
  <div class="bg-white text-gray-900 transition-colors duration-300 min-h-screen flex flex-col">
    <div class="container mx-auto max-w-6xl p-4 flex-1">
      <!-- Header -->
      <div class="text-center mb-6">
        <h1 class="text-3xl font-bold mb-2">EEGC Human-AI Collaboration Chatbot</h1>
        <p class="text-gray-600">Practice and assess your AI interaction skills</p>
      </div>

      <!-- Mode Selection -->
      <div class="mb-6 p-4 bg-gray-50 rounded-lg">
        <div class="flex flex-col md:flex-row gap-4 items-center justify-between">
          <div class="flex gap-4">
            <button
              @click="switchMode('training')"
              :class="currentMode === 'training' ? activeBtn : inactiveBtn"
            >
              Training Mode
            </button>
            <button
              @click="switchMode('assessment')"
              :class="currentMode === 'assessment' ? activeBtn : inactiveBtn"
            >
              Assessment Mode
            </button>
          </div>
          <div
            class="px-4 py-2 rounded-full text-sm font-medium"
            :class="
              currentMode === 'training' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
            "
          >
            {{ currentMode === "training" ? "Training Mode Active" : "Assessment Mode Active" }}
          </div>
        </div>
      </div>

      <!-- Main Grid -->
      <div
        class="gap-6 mb-6 grid"
        :class="currentMode === 'assessment' ? 'md:grid-cols-3' : 'md:grid-cols-2'"
      >
        <!-- Left: Skills and Progress -->
        <div class="md:col-span-2 space-y-6">
          <!-- Skills Dashboard -->
          <div class="grid md:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2
                class="text-xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent"
              >
                Skills Being Developed
              </h2>

              <SkillBadge
                borderColor="border-blue-500"
                title="In-Depth Conversation"
                textColor="text-blue-600"
                :points="[
                  'Ask follow-up questions',
                  'Engage in multi-level dialogue',
                  'Maintain conversation depth',
                ]"
              />
              <SkillBadge
                borderColor="border-purple-500"
                title="Critical Review"
                textColor="text-purple-600"
                :points="[
                  'Evaluate AI suggestions critically',
                  'Provide evidence-based justification',
                  'Accept/reject with reasoning',
                ]"
              />
              <SkillBadge
                borderColor="border-green-500"
                title="Iterative Refinement"
                textColor="text-green-600"
                :points="[
                  'Multiple revision cycles',
                  'Build on previous feedback',
                  'Progressive improvement',
                ]"
              />
            </div>

            <!-- Session Progress -->
            <div class="bg-white p-6 rounded-lg shadow-lg">
              <h2 class="text-xl font-bold mb-4">Session Progress</h2>
              <div class="space-y-3">
                <SessionStat label="Total Exchanges" :value="stats.exchanges" color="blue" />
                <SessionStat label="Follow-up Questions" :value="stats.questions" color="purple" />
                <SessionStat label="Revision Cycles" :value="stats.revisions" color="green" />
              </div>
              <button
                @click="exportChatHistory"
                class="w-full mt-4 px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:opacity-90 transition-opacity"
              >
                Export Chat History
              </button>
            </div>
          </div>

          <!-- Sample Essay -->
          <div class="mb-6 p-4 bg-gray-50 rounded-lg">
            <h3 class="font-bold mb-2">Sample Essay for Practice:</h3>
            <div class="text-sm bg-white p-4 rounded border italic">
              "As a university student, I agree with that internet has positive impact on our lives.
              During the Covid-19, schools were using Zoom to maintain their teaching. Until now,
              students had discovered many side of zoom. They use zoom to take tutorial classes,
              have meeting with group mates and so on. Internet not only allow students to study at
              home, but also provide a new learning style. Apart from that, the internet is also
              contributes to our health. With the rapid development of the 5G technology, doctors
              are able to operate more precisely Robot-Assist surgery (RAs). This means we can have
              less trauma, less covery time and better surgery effect. And it all thanks to the high
              speed and stable internet. Some people may worried about their privacy issue while
              using the internet. However, in my opinion, as long as we pay more attention to our
              behaviour such as not viewing strange website, not giving out our personal information
              and so on. We can protect our privacy to a certain extent. (170 words)"
            </div>
          </div>
        </div>

        <!-- Right: Assessment Inputs -->
        <div v-if="currentMode === 'assessment'" class="space-y-6">
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-lg font-bold mb-2">Original Draft</h2>
            <textarea
              v-model="originalDraft"
              rows="8"
              placeholder="Paste or write the original draft here..."
              class="w-full border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
            ></textarea>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-lg font-bold mb-2">Final Draft</h2>
            <textarea
              v-model="finalDraft"
              rows="8"
              placeholder="Paste or write the improved draft here..."
              class="w-full border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <!-- Chat Section -->
    <div class="border-t bg-gray-50 p-4">
      <div class="max-w-6xl mx-auto flex flex-col h-96">
        <!-- Message list -->
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
        <div class="mt-2 flex gap-2">
          <input
            v-model="userMessage"
            type="text"
            placeholder="Type your message..."
            class="flex-1 border rounded-lg p-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed"
            @keyup.enter="sendMessage"
            :disabled="isThinking"
          />
          <button
            @click="sendMessage"
            class="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
            :disabled="isThinking"
          >
            {{ isThinking ? "Thinking..." : "Send" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, h, defineComponent, nextTick } from "vue";
import { BASE_URL } from "../components/base_url";
import MarkdownIt from "markdown-it";

// ✅ Only use markdown-it (no katex plugin)
const markdown = new MarkdownIt({
  html: false, // disallow raw HTML in user messages
  linkify: true, // auto-detect URLs
  typographer: true, // nicer quotes & dashes
});
/* ------------ State ------------ */
const currentMode = ref("training");
const stats = ref({ exchanges: 0, questions: 0, revisions: 0 });
const originalDraft = ref("");
const finalDraft = ref("");

const chatHistory = ref([]);
const userMessage = ref("");
const chatMessages = ref(null);
const isThinking = ref(false); // ✅ new state

const greetings = {
  training: `Hello! I'm here to help you improve your essay through AI collaboration. Let's start by choosing which aspect of your essay you'd like to work on. Would you like to focus on:\n1) Content & Ideas\n2) Organisation & Structure\n3) Vocabulary\n4) Grammar & Sentence Structure`,
  assessment: `I am here to help you revise the essay. Please share an essay draft.`,
};

const activeBtn =
  "px-6 py-3 bg-indigo-600 text-white rounded-lg font-semibold hover:opacity-90 transition-opacity";
const inactiveBtn =
  "px-6 py-3 bg-gray-300 text-gray-700 rounded-lg font-semibold hover:opacity-90 transition-opacity";

/* ------------ Components ------------ */
const SkillBadge = defineComponent({
  name: "SkillBadge",
  props: { borderColor: String, title: String, textColor: String, points: Array },
  setup(props) {
    return () =>
      h("div", { class: `border-l-4 pl-4 mb-4 ${props.borderColor}` }, [
        h("h3", { class: `font-semibold ${props.textColor}` }, props.title),
        h(
          "ul",
          { class: "text-sm text-gray-600 mt-1" },
          props.points?.map((p, i) => h("li", { key: i }, `• ${p}`))
        ),
      ]);
  },
});

const SessionStat = defineComponent({
  name: "SessionStat",
  props: { label: String, value: Number, color: String },
  setup(props) {
    const map = {
      blue: "bg-blue-100 text-blue-800",
      purple: "bg-purple-100 text-purple-800",
      green: "bg-green-100 text-green-800",
    };
    const colorClasses = computed(() => map[props.color] || "bg-gray-100 text-gray-800");

    return () =>
      h("div", { class: "flex justify-between items-center" }, [
        h("span", { class: "text-sm font-medium" }, props.label),
        h(
          "span",
          { class: `px-3 py-1 rounded-full text-sm font-semibold ${colorClasses.value}` },
          props.value
        ),
      ]);
  },
});

/* ------------ Chat Helpers ------------ */
function msgSenderLabel(role) {
  return role === "user" ? "You" : "AI Assistant";
}
function msgClasses(msg) {
  return msg.role === "user"
    ? "bg-indigo-600 text-white rounded-br-none"
    : "bg-gray-100 text-gray-800 rounded-bl-none";
}

function renderMarkdown(text) {
  return markdown.render(text || "");
}

/* ------------ Methods ------------ */
function switchMode(mode) {
  currentMode.value = mode;
  stats.value = { exchanges: 0, questions: 0, revisions: 0 };
  chatHistory.value = [{ role: "assistant", content: greetings[mode], timestamp: new Date() }];
  scrollToBottom();
}

async function sendMessage() {
  if (!userMessage.value.trim() || isThinking.value) return;

  chatHistory.value.push({
    role: "user",
    content: userMessage.value,
    timestamp: new Date(),
  });
  stats.value.exchanges++;
  userMessage.value = "";
  scrollToBottom();

  isThinking.value = true;

  try {
    // --- Build payload history separately from visible chatHistory ---
    let payloadHistory = [...chatHistory.value];

    if (currentMode.value === "assessment") {
      // Insert **system message with both drafts** only for backend
      payloadHistory = [
        {
          role: "system",
          content:
            "You are in *Assessment Mode*. Your task is to evaluate the user's drafts.\n\n" +
            "Here are the drafts:\n" +
            "Original Draft:\n---\n" +
            "${originalDraft.value || '(empty)'}\n---\n\n" +
            "Final Draft:\n---\n" +
            "${finalDraft.value || '(empty)'}\n---\n\n" +
            "Please provide a critical reflection that:\n" +
            "1. Identifies key differences between the drafts.\n" +
            "2. Highlights specific improvements (clarity, structure, tone, persuasiveness, etc.).\n" +
            "3. Points out remaining weaknesses or areas that could still be enhanced.\n" +
            "4. Offers constructive, actionable suggestions for revision.",
        },
        ...payloadHistory,
      ];
    } else if (currentMode.value === "training") {
      // Insert system message  for backend
      payloadHistory = [
        {
          role: "system",
          content: greetings[currentMode.value],
        },
        ...payloadHistory,
      ];
    }

    const res = await fetch(`${BASE_URL}/chatbot/chat_openrouter`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_history: payloadHistory }),
    });

    const data = await res.json();
    const reply = data?.choices?.[0]?.message?.content || data?.response || data?.message || "";

    if (reply) {
      chatHistory.value.push({ role: "assistant", content: reply, timestamp: new Date() });
      scrollToBottom();
    }
  } catch {
    chatHistory.value.push({
      role: "assistant",
      content: "⚠️ Error connecting to server.",
      timestamp: new Date(),
    });
  } finally {
    isThinking.value = false;
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatMessages.value) {
      chatMessages.value.scrollTop = chatMessages.value.scrollHeight;
    }
  });
}

function exportChatHistory() {
  const blob = new Blob([JSON.stringify(chatHistory.value, null, 2)], {
    type: "application/json",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "chat_history.json";
  a.click();
  URL.revokeObjectURL(url);
}

// ✅ Auto-init
switchMode(currentMode.value);
</script>
