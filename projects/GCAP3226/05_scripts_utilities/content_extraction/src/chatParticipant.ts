import * as vscode from 'vscode';
import { OpenRouterClient, ChatMessage } from './openRouterClient';

export class OpenRouterChatParticipant {
    private client: OpenRouterClient | null = null;
    private context: vscode.ExtensionContext;

    constructor(context: vscode.ExtensionContext) {
        this.context = context;
        this.updateClientFromConfig();
        
        // Watch for configuration changes
        vscode.workspace.onDidChangeConfiguration((e) => {
            if (e.affectsConfiguration('openrouterCopilot')) {
                this.updateClientFromConfig();
            }
        });
    }

    private updateClientFromConfig(): void {
        const config = vscode.workspace.getConfiguration('openrouterCopilot');
        const apiKey = config.get<string>('apiKey', '');
        const model = config.get<string>('defaultModel', 'anthropic/claude-3.5-sonnet');
        const temperature = config.get<number>('temperature', 0.7);

        if (apiKey) {
            this.client = new OpenRouterClient({
                apiKey,
                model,
                temperature
            });
        } else {
            this.client = null;
        }
    }

    async handleChatRequest(
        request: vscode.ChatRequest,
        context: vscode.ChatContext,
        stream: vscode.ChatResponseStream,
        token: vscode.CancellationToken
    ): Promise<vscode.ChatResult> {
        if (!this.client) {
            stream.markdown('❌ **OpenRouter API key not configured**\n\nPlease set your API key in VS Code settings:\n1. Open Settings (Cmd/Ctrl + ,)\n2. Search for "OpenRouter Copilot"\n3. Enter your API key');
            return { metadata: { command: '', lastError: 'API key not configured' } };
        }

        if (!request.prompt?.trim()) {
            stream.markdown('Please provide a prompt to chat with the AI model.');
            return { metadata: { command: '' } };
        }

        try {
            // Handle model switching command
            if (request.command === 'model') {
                return await this.handleModelCommand(request, stream);
            }

            // Handle list models command
            if (request.command === 'models') {
                return await this.handleListModelsCommand(stream);
            }

            // Show typing indicator
            stream.progress('Thinking...');

            // Build conversation context
            const messages: ChatMessage[] = this.buildConversationContext(request, context);

            let fullResponse = '';
            
            // Use streaming for better user experience
            await this.client.streamChat(messages, (chunk: string) => {
                if (token.isCancellationRequested) {
                    return;
                }
                fullResponse += chunk;
                stream.markdown(chunk);
            });

            return { 
                metadata: { 
                    command: request.command || '',
                    model: vscode.workspace.getConfiguration('openrouterCopilot').get<string>('defaultModel'),
                    tokensUsed: fullResponse.length // Approximate
                } 
            };

        } catch (error) {
            const errorMessage = error instanceof Error ? error.message : 'Unknown error occurred';
            stream.markdown(`❌ **Error**: ${errorMessage}`);
            return { metadata: { command: request.command || '', lastError: errorMessage } };
        }
    }

    private async handleModelCommand(
        request: vscode.ChatRequest, 
        stream: vscode.ChatResponseStream
    ): Promise<vscode.ChatResult> {
        const availableModels = this.client?.getAvailableModels() || [];
        const requestedModel = request.prompt.trim();

        if (!requestedModel) {
            const currentModel = vscode.workspace.getConfiguration('openrouterCopilot').get<string>('defaultModel');
            stream.markdown(`**Current model**: \`${currentModel}\`\n\n**Available models**:\n${availableModels.map(m => `- \`${m}\``).join('\n')}\n\nUse \`@openrouter /model <model-name>\` to switch models.`);
            return { metadata: { command: 'model' } };
        }

        if (availableModels.includes(requestedModel)) {
            const config = vscode.workspace.getConfiguration('openrouterCopilot');
            await config.update('defaultModel', requestedModel, vscode.ConfigurationTarget.Global);
            stream.markdown(`✅ **Model switched to**: \`${requestedModel}\``);
            return { metadata: { command: 'model', model: requestedModel } };
        } else {
            stream.markdown(`❌ **Model not found**: \`${requestedModel}\`\n\n**Available models**:\n${availableModels.map(m => `- \`${m}\``).join('\n')}`);
            return { metadata: { command: 'model', lastError: 'Model not found' } };
        }
    }

    private async handleListModelsCommand(stream: vscode.ChatResponseStream): Promise<vscode.ChatResult> {
        const availableModels = this.client?.getAvailableModels() || [];
        const currentModel = vscode.workspace.getConfiguration('openrouterCopilot').get<string>('defaultModel');
        
        stream.markdown(`**Available OpenRouter Models**:\n\n${availableModels.map(model => 
            model === currentModel ? `- \`${model}\` ✓ (current)` : `- \`${model}\``
        ).join('\n')}\n\nUse \`@openrouter /model <model-name>\` to switch models.`);
        
        return { metadata: { command: 'models' } };
    }

    private buildConversationContext(
        request: vscode.ChatRequest, 
        context: vscode.ChatContext
    ): ChatMessage[] {
        const messages: ChatMessage[] = [];

        // Add system message
        messages.push({
            role: 'system',
            content: 'You are a helpful AI assistant integrated into VS Code. Provide clear, concise, and accurate responses. When discussing code, use appropriate markdown formatting with syntax highlighting.'
        });

        // Add conversation history (last few messages for context)
        const historyLimit = 5;
        const recentHistory = context.history.slice(-historyLimit);
        
        for (const turn of recentHistory) {
            if (turn instanceof vscode.ChatRequestTurn) {
                messages.push({
                    role: 'user',
                    content: turn.prompt
                });
            } else if (turn instanceof vscode.ChatResponseTurn) {
                // Extract text content from response
                const content = this.extractTextFromResponse(turn);
                if (content) {
                    messages.push({
                        role: 'assistant',
                        content: content
                    });
                }
            }
        }

        // Add current request
        messages.push({
            role: 'user',
            content: request.prompt
        });

        return messages;
    }

    private extractTextFromResponse(turn: vscode.ChatResponseTurn): string {
        // Extract text from various response parts
        let content = '';
        for (const part of turn.response) {
            if (part instanceof vscode.ChatResponseMarkdownPart) {
                content += part.value.value + '\n';
            } else if (part instanceof vscode.ChatResponseFileTreePart) {
                content += `[File tree: ${part.value.map(f => f.name).join(', ')}]\n`;
            }
        }
        return content.trim();
    }

    getFollowupProvider(): vscode.ChatFollowupProvider {
        return {
            provideFollowups: async (
                result: vscode.ChatResult,
                context: vscode.ChatContext,
                token: vscode.CancellationToken
            ) => {
                const followups: vscode.ChatFollowup[] = [];

                // Add model-specific followups
                if (result.metadata?.command !== 'model' && result.metadata?.command !== 'models') {
                    followups.push({
                        prompt: 'Can you explain this in more detail?',
                        label: '🔍 More details'
                    });

                    followups.push({
                        prompt: 'Can you provide a code example?',
                        label: '💻 Code example'
                    });
                }

                // Add utility followups
                followups.push({
                    prompt: '@openrouter /models',
                    label: '🤖 Available models'
                });

                return followups;
            }
        };
    }
}