# GCAP3226 Course Repository

**Government and Civil Service Analytics Program**
*Reorganized Structure for Teaching and Learning*

---

## 📁 **Clean Directory Structure**

```
GCAP3226/
├── 📚 00_documentation/          # Project documentation and notes
│   ├── project_notes/            # Course planning and notes
│   └── setup_reports/            # Setup and progress reports
├── 📖 01_course_content/         # Primary course materials
│   ├── week01_introduction/
│   ├── week02_foundations/
│   ├── week03_methods/
│   ├── week04_simulation/        # ← Current week (Bus Route Case Study)
│   └── week05_advanced/
├── 👥 02_student_workspace/      # Student work areas
│   ├── individual_work/
│   ├── group_projects/
│   ├── submissions/
│   └── practice_exercises/
├── 🎓 03_instructor_tools/       # Teaching and administrative tools
│   ├── grading_rubrics/
│   ├── student_management/
│   ├── budget_planning/
│   └── ai_assistants/
├── 📊 04_data_resources/         # Data sources and analysis
│   ├── open_data_inventory/
│   ├── datasets/
│   └── external_apis/
├── ⚙️ 05_scripts_utilities/      # Code utilities and automation
│   ├── data_processing/
│   ├── content_extraction/
│   └── automation/
├── ⚙️ 98_technical/              # Technical configuration
│   ├── config/                   # VS Code, venv, etc.
│   └── logs_backups/            # System logs and backups
└── 🗃️ 99_archive/               # Archived and legacy materials
```

---

## 🚀 **Quick Start**

### **📖 For Teaching Week 4:**

```bash
cd 01_course_content/week04_simulation/
# Access: lectures, assignments, resources, extracted_materials
```

### **👥 For Student Work:**

```bash
cd 02_student_workspace/
# Access: individual_work, group_projects, submissions
```

### **🛠️ For Content Extraction:**

```bash
cd 05_scripts_utilities/content_extraction/
python simple_ppt_extractor.py
```

---

## 📋 **Current Course Status**

- **✅ Week 4:** Bus Route Simulation Case Study (Complete)
- **🔧 Structure:** Fully reorganized and cleaned
- **📊 Data:** Hong Kong open data integrated
- **🤖 Tools:** PPT extraction, AI assistants ready

---

## � **Key Resources**

| Resource               | Location                                     | Description                   |
| ---------------------- | -------------------------------------------- | ----------------------------- |
| Course Structure Guide | `README_NEW_STRUCTURE.md`                  | Detailed navigation guide     |
| Week 4 Materials       | `01_course_content/week04_simulation/`     | Current simulation case study |
| PPT Extraction Tools   | `05_scripts_utilities/content_extraction/` | Automated content processing  |
| Project Documentation  | `00_documentation/`                        | All project notes and reports |

---

## 📈 **Recent Updates**

- **Sept 22, 2025:** Complete repository reorganization
- **Sept 22, 2025:** PowerPoint extraction system implemented
- **Sept 22, 2025:** Week 4 simulation case study structured
- **Sept 22, 2025:** Data governance framework integrated

---

**Repository maintained by:** Simon Wang
**Course:** GCAP3226 - Government Analytics
**Last updated:** September 22, 2025

## Configuration

### Setting up OpenRouter API Key

1. Get your API key from [OpenRouter.ai](https://openrouter.ai)
2. In VS Code, open Settings (Cmd/Ctrl + ,)
3. Search for "OpenRouter Copilot"
4. Enter your API key in the "Api Key" field

### Available Settings

- **openrouterCopilot.apiKey**: Your OpenRouter API key
- **openrouterCopilot.defaultModel**: Default AI model to use
- **openrouterCopilot.temperature**: Temperature for AI responses (0-2)

## Usage

### Basic Chat

1. Open GitHub Copilot Chat panel
2. Type `@openrouter` followed by your question
3. The AI will respond using the configured model

### Commands

- `@openrouter /models` - List available models
- `@openrouter /model <model-name>` - Switch to a specific model

### Examples

```
@openrouter How do I implement a binary search in TypeScript?

@openrouter /model anthropic/claude-3-opus
@openrouter Explain the differences between async/await and Promises

@openrouter /models
```

## Supported Models

- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Opus, Claude 3 Haiku
- **OpenAI**: GPT-4 Turbo, GPT-4, GPT-3.5 Turbo
- **Meta**: Llama 2 70B Chat
- **Google**: Gemini Pro
- **Mistral**: Mixtral 8x7B Instruct

## Development

### Prerequisites

- Node.js 16+
- VS Code 1.74+
- TypeScript

### Building

```bash
# Install dependencies
npm install

# Compile TypeScript
npm run compile

# Watch for changes
npm run watch
```

### Debugging

1. Open the project in VS Code
2. Press F5 to launch Extension Development Host
3. Test the extension in the new VS Code window

### Project Structure

```
src/
├── extension.ts          # Main extension entry point
├── chatParticipant.ts    # Chat participant implementation
└── openRouterClient.ts   # OpenRouter API client

.vscode/
├── launch.json          # Debug configuration
└── tasks.json           # Build tasks

package.json             # Extension manifest
tsconfig.json           # TypeScript configuration
```

## Troubleshooting

### Common Issues

1. **"API key not configured"**

   - Ensure you've set your OpenRouter API key in VS Code settings
2. **"Cannot find module 'vscode'"**

   - Run `npm install` to install dependencies
3. **Chat participant not appearing**

   - Make sure the extension is activated and GitHub Copilot is enabled

### Getting Help

- Check the VS Code Developer Console for error messages
- Verify your OpenRouter API key is valid
- Ensure you have GitHub Copilot enabled in VS Code

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [OpenRouter](https://openrouter.ai) for providing access to multiple AI models
- [VS Code Extension API](https://code.visualstudio.com/api) for the platform
- [GitHub Copilot](https://github.com/features/copilot) for the chat interface
