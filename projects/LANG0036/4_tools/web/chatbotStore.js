import { defineStore } from 'pinia';

export const useChatbotStore = defineStore('chatbot', {
  // 1. ADD `availableBots` to the state
  state: () => ({
    selectedBot: null,
    availableBots: [], // This will hold our list of bots from the JSON files
    currentState: {
      mode: null, // 'welcome', 'menu', 'brainstorm', 'review', 'feedback'
      context: null, // Store current context (e.g., essay topic)
    },
  }),

  actions: {
    selectBot(bot) {
      this.selectedBot = bot;
    },

    /**
     * 2. ADD a new action to load all bot configs automatically.
     * This uses Vite's glob import feature.
     */
    async loadBots() {
      // If we've already loaded them, don't do it again.
      if (this.availableBots.length > 0) return;

      const modules = import.meta.glob('../botConfig/*.json');
      const bots = [];

      for (const path in modules) {
        const module = await modules[path]();
        // Get a unique 'id' from the filename (e.g., 'learning' from 'learning.json')
        const id = path.split('/').pop().replace('.json', '');
        
        bots.push({
          id, // e.g., 'learning'
          ...module.default, // The content of the JSON file
        });
      }
      this.availableBots = bots;
    },

    setConversationState(mode, context = null) {
      this.currentState = {
        mode,
        context,
      };
    },

    getConversationState() {
      return this.currentState;
    },
  },
});