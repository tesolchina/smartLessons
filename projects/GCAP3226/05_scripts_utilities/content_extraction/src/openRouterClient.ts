import axios, { AxiosResponse } from 'axios';

export interface OpenRouterConfig {
    apiKey: string;
    model: string;
    temperature: number;
    maxTokens?: number;
    baseURL?: string;
}

export interface ChatMessage {
    role: 'system' | 'user' | 'assistant';
    content: string;
}

export interface OpenRouterResponse {
    choices: Array<{
        message: {
            content: string;
            role: string;
        };
        finish_reason: string;
    }>;
    usage?: {
        prompt_tokens: number;
        completion_tokens: number;
        total_tokens: number;
    };
}

export class OpenRouterClient {
    private config: OpenRouterConfig;
    private baseURL: string;

    constructor(config: OpenRouterConfig) {
        this.config = config;
        this.baseURL = config.baseURL || 'https://openrouter.ai/api/v1';
    }

    async chat(messages: ChatMessage[]): Promise<string> {
        try {
            const response: AxiosResponse<OpenRouterResponse> = await axios.post(
                `${this.baseURL}/chat/completions`,
                {
                    model: this.config.model,
                    messages: messages,
                    temperature: this.config.temperature,
                    max_tokens: this.config.maxTokens || 4000,
                },
                {
                    headers: {
                        'Authorization': `Bearer ${this.config.apiKey}`,
                        'Content-Type': 'application/json',
                        'HTTP-Referer': 'https://code.visualstudio.com',
                        'X-Title': 'VS Code OpenRouter Copilot Agent',
                    },
                    timeout: 30000,
                }
            );

            if (response.data.choices && response.data.choices.length > 0) {
                return response.data.choices[0].message.content;
            } else {
                throw new Error('No response from OpenRouter API');
            }
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const status = error.response?.status;
                const statusText = error.response?.statusText;
                const errorData = error.response?.data;
                
                throw new Error(`OpenRouter API error (${status} ${statusText}): ${JSON.stringify(errorData)}`);
            } else {
                throw new Error(`OpenRouter client error: ${error}`);
            }
        }
    }

    async streamChat(messages: ChatMessage[], onChunk: (chunk: string) => void): Promise<void> {
        try {
            const response = await axios.post(
                `${this.baseURL}/chat/completions`,
                {
                    model: this.config.model,
                    messages: messages,
                    temperature: this.config.temperature,
                    max_tokens: this.config.maxTokens || 4000,
                    stream: true,
                },
                {
                    headers: {
                        'Authorization': `Bearer ${this.config.apiKey}`,
                        'Content-Type': 'application/json',
                        'HTTP-Referer': 'https://code.visualstudio.com',
                        'X-Title': 'VS Code OpenRouter Copilot Agent',
                    },
                    responseType: 'stream',
                    timeout: 30000,
                }
            );

            response.data.on('data', (chunk: Buffer) => {
                const lines = chunk.toString().split('\n');
                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = line.slice(6);
                        if (data === '[DONE]') {
                            return;
                        }
                        try {
                            const parsed = JSON.parse(data);
                            const content = parsed.choices?.[0]?.delta?.content;
                            if (content) {
                                onChunk(content);
                            }
                        } catch (e) {
                            // Skip invalid JSON chunks
                        }
                    }
                }
            });

            return new Promise((resolve, reject) => {
                response.data.on('end', resolve);
                response.data.on('error', reject);
            });
        } catch (error) {
            if (axios.isAxiosError(error)) {
                const status = error.response?.status;
                const statusText = error.response?.statusText;
                const errorData = error.response?.data;
                
                throw new Error(`OpenRouter streaming error (${status} ${statusText}): ${JSON.stringify(errorData)}`);
            } else {
                throw new Error(`OpenRouter streaming client error: ${error}`);
            }
        }
    }

    updateConfig(config: Partial<OpenRouterConfig>): void {
        this.config = { ...this.config, ...config };
    }

    getAvailableModels(): string[] {
        return [
            'anthropic/claude-3.5-sonnet',
            'anthropic/claude-3-opus',
            'anthropic/claude-3-haiku',
            'openai/gpt-4-turbo',
            'openai/gpt-4',
            'openai/gpt-3.5-turbo',
            'meta-llama/llama-2-70b-chat',
            'google/gemini-pro',
            'mistralai/mixtral-8x7b-instruct'
        ];
    }
}