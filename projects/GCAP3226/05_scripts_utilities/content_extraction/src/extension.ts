import * as vscode from 'vscode';
import { OpenRouterChatParticipant } from './chatParticipant';

export function activate(context: vscode.ExtensionContext) {
    console.log('OpenRouter Copilot Agent is now active!');

    try {
        // Create the chat participant
        const chatParticipant = new OpenRouterChatParticipant(context);

        // Register the chat participant
        const participant = vscode.chat.createChatParticipant(
            'openrouter-agent',
            chatParticipant.handleChatRequest.bind(chatParticipant)
        );

        // Set participant properties
        participant.iconPath = new vscode.ThemeIcon('robot');
        participant.followupProvider = chatParticipant.getFollowupProvider();

        // Add to subscriptions for proper cleanup
        context.subscriptions.push(participant);

        // Register commands
        const showConfigCommand = vscode.commands.registerCommand(
            'openrouterCopilot.showConfig',
            () => {
                vscode.commands.executeCommand('workbench.action.openSettings', 'openrouterCopilot');
            }
        );

        const setApiKeyCommand = vscode.commands.registerCommand(
            'openrouterCopilot.setApiKey',
            async () => {
                const apiKey = await vscode.window.showInputBox({
                    prompt: 'Enter your OpenRouter API key',
                    password: true,
                    ignoreFocusOut: true,
                    placeHolder: 'sk-or-...'
                });

                if (apiKey) {
                    const config = vscode.workspace.getConfiguration('openrouterCopilot');
                    await config.update('apiKey', apiKey, vscode.ConfigurationTarget.Global);
                    vscode.window.showInformationMessage('OpenRouter API key updated successfully!');
                }
            }
        );

        const switchModelCommand = vscode.commands.registerCommand(
            'openrouterCopilot.switchModel',
            async () => {
                const models = [
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

                const selectedModel = await vscode.window.showQuickPick(models, {
                    placeHolder: 'Select an AI model',
                    ignoreFocusOut: true
                });

                if (selectedModel) {
                    const config = vscode.workspace.getConfiguration('openrouterCopilot');
                    await config.update('defaultModel', selectedModel, vscode.ConfigurationTarget.Global);
                    vscode.window.showInformationMessage(`Model switched to: ${selectedModel}`);
                }
            }
        );

        context.subscriptions.push(showConfigCommand, setApiKeyCommand, switchModelCommand);

        // Check if API key is configured
        const config = vscode.workspace.getConfiguration('openrouterCopilot');
        const apiKey = config.get<string>('apiKey', '');
        
        if (!apiKey) {
            vscode.window.showWarningMessage(
                'OpenRouter API key not configured. The chat participant will not work until you set your API key.',
                'Set API Key',
                'Open Settings'
            ).then(selection => {
                if (selection === 'Set API Key') {
                    vscode.commands.executeCommand('openrouterCopilot.setApiKey');
                } else if (selection === 'Open Settings') {
                    vscode.commands.executeCommand('openrouterCopilot.showConfig');
                }
            });
        }

        console.log('OpenRouter Copilot Agent registered successfully');
        
    } catch (error) {
        console.error('Failed to activate OpenRouter Copilot Agent:', error);
        vscode.window.showErrorMessage(`Failed to activate OpenRouter Copilot Agent: ${error}`);
    }
}

export function deactivate() {
    console.log('OpenRouter Copilot Agent is now deactivated');
}