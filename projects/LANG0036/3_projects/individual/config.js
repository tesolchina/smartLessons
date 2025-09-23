// Centralized config for AI and Email. Defaults keep integrations disabled.

const STORAGE_KEYS = {
  aiEnabled: 'hkbu.ai.enabled',
  aiApiKey: 'hkbu.ai.key',
  aiModel: 'hkbu.ai.model',
  aiApiVersion: 'hkbu.ai.apiVersion',
  aiProxyUrl: 'hkbu.ai.proxyUrl',
  systemPrompt: 'hkbu.ai.systemPrompt',
  emailEnabled: 'hkbu.email.enabled',
  emailTo: 'hkbu.email.to',
  emailCc: 'hkbu.email.cc',
  emailServiceId: 'hkbu.email.serviceId',
  emailTemplateId: 'hkbu.email.templateId',
  emailPublicKey: 'hkbu.email.publicKey'
};

export const config = {
  // AI
  isAiEnabled() {
    return localStorage.getItem(STORAGE_KEYS.aiEnabled) === 'true';
  },
  setAiEnabled(enabled) {
    localStorage.setItem(STORAGE_KEYS.aiEnabled, String(Boolean(enabled)));
  },
  getAiApiKey() {
    return localStorage.getItem(STORAGE_KEYS.aiApiKey) || '';
  },
  setAiApiKey(key) {
    localStorage.setItem(STORAGE_KEYS.aiApiKey, key || '');
  },
  getAiModel() {
    return localStorage.getItem(STORAGE_KEYS.aiModel) || 'gpt-4.1';
  },
  setAiModel(model) {
    localStorage.setItem(STORAGE_KEYS.aiModel, model || '');
  },
  getAiApiVersion() {
    return localStorage.getItem(STORAGE_KEYS.aiApiVersion) || '2024-05-01-preview';
  },
  setAiApiVersion(ver) {
    localStorage.setItem(STORAGE_KEYS.aiApiVersion, ver || '');
  },
  getAiProxyUrl() {
    // Default to Vercel edge function in this repo when not overridden
    return localStorage.getItem(STORAGE_KEYS.aiProxyUrl) || 'https://hkbu-chatbot.vercel.app/api/proxy?url=';
  },
  setAiProxyUrl(url) {
    localStorage.setItem(STORAGE_KEYS.aiProxyUrl, url || '');
  },

  // System Prompt
  getSystemPrompt() {
    return localStorage.getItem(STORAGE_KEYS.systemPrompt) || '';
  },
  setSystemPrompt(prompt) {
    localStorage.setItem(STORAGE_KEYS.systemPrompt, prompt || '');
  },

  // Email
  isEmailEnabled() {
    return localStorage.getItem(STORAGE_KEYS.emailEnabled) === 'true';
  },
  setEmailEnabled(enabled) {
    localStorage.setItem(STORAGE_KEYS.emailEnabled, String(Boolean(enabled)));
  },
  getEmailDefaults() {
    return {
      to: localStorage.getItem(STORAGE_KEYS.emailTo) || '',
      cc: localStorage.getItem(STORAGE_KEYS.emailCc) || ''
    };
  },
  setEmailDefaults({ to, cc }) {
    if (to != null) localStorage.setItem(STORAGE_KEYS.emailTo, to);
    if (cc != null) localStorage.setItem(STORAGE_KEYS.emailCc, cc);
  },
  getEmailJsConfig() {
    return {
      serviceId: localStorage.getItem(STORAGE_KEYS.emailServiceId) || '',
      templateId: localStorage.getItem(STORAGE_KEYS.emailTemplateId) || '',
      publicKey: localStorage.getItem(STORAGE_KEYS.emailPublicKey) || ''
    };
  },
  setEmailJsConfig({ serviceId, templateId, publicKey }) {
    if (serviceId != null) localStorage.setItem(STORAGE_KEYS.emailServiceId, serviceId);
    if (templateId != null) localStorage.setItem(STORAGE_KEYS.emailTemplateId, templateId);
    if (publicKey != null) localStorage.setItem(STORAGE_KEYS.emailPublicKey, publicKey);
  }
};

export { STORAGE_KEYS };


