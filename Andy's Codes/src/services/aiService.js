import { config } from './config.js';

// Placeholder for HKBU GenAI API integration
// Expose minimal surface so UI can call AI later without refactors

export function isAiConfigured() {
  return config.isAiEnabled() && !!config.getAiApiKey();
}

export async function sendChatMessage(messages, options = {}) {
  // messages: [{ role: 'system'|'user'|'assistant', content: string }]
  // options: { model?: string, apiKey?: string }
  if (!isAiConfigured()) {
    console.warn('[aiService] Not configured. Returning placeholder response.');
    return { success: false, response: 'AI is disabled or missing API key.', error: 'NOT_CONFIGURED' };
  }
  const apiKey = options.apiKey || config.getAiApiKey();
  const model = options.model || config.getAiModel();
  const apiVersion = config.getAiApiVersion();
  const proxy = config.getAiProxyUrl(); // optional

  // Prepend system prompt if configured
  let finalMessages = [...messages];
  const systemPrompt = config.getSystemPrompt();
  if (systemPrompt && systemPrompt.trim()) {
    finalMessages = [{ role: 'system', content: systemPrompt.trim() }, ...messages];
  }
  
  // Special hardcoded system prompt for reflection tasks
  const isReflectionTask = messages.some(msg => 
    msg.content && msg.content.includes('Task:') && msg.content.includes('Student\'s Response:')
  );
  
  if (isReflectionTask) {
    const reflectionSystemPrompt = `You are an expert academic tutor and research mentor specializing in UCLC 1008 Research Foundations. Your role is to provide constructive, encouraging feedback on student reflection responses.

Guidelines for feedback:
- Be encouraging and supportive while maintaining academic rigor
- Identify strengths in the student's thinking and approach
- Suggest specific areas for improvement or deeper exploration
- Keep feedback concise (2-3 sentences) and actionable
- Use a warm, mentoring tone appropriate for undergraduate students
- Focus on research thinking, critical analysis, and academic growth

Provide feedback that helps the student develop their research mindset and academic confidence.`;

    finalMessages = [{ role: 'system', content: reflectionSystemPrompt }, ...messages];
  }

  const base = 'https://genai.hkbu.edu.hk/api/v0/rest';
  const targetUrl = `${base}/deployments/${encodeURIComponent(model)}/chat/completions?api-version=${encodeURIComponent(apiVersion)}`;
  const url = proxy ? `${proxy}${encodeURIComponent(targetUrl)}` : targetUrl;

  const payload = { messages: finalMessages, stream: false };

  try {
    const res = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'api-key': apiKey
      },
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const text = await res.text();
      return { success: false, error: `HTTP_${res.status}`, response: text };
    }
    const data = await res.json();
    const content = data?.choices?.[0]?.message?.content ?? '';
    return { success: true, response: content, raw: data };
  } catch (err) {
    return { success: false, error: 'NETWORK_ERROR', response: String(err) };
  }
}

