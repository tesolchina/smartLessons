# Chatbot Simulation System

This system creates LLM-based simulated interactions between educational chatbots and student personas.

## Features

- **Dual-Agent System**: Teacher chatbot (from your bot configs) + Simulated student
- **Realistic Student Personas**: Different learning levels, styles, and personalities
- **Automatic Interaction**: Self-running conversations with natural flow
- **Comprehensive Logging**: Full conversation history with timestamps
- **Multiple Bot Support**: Works with any bot configuration from the repository

## Quick Start

1. **Setup OpenRouter** (if not already done):
   ```bash
   # Create .env file in project root with:
   OPENROUTER_API_KEY="sk-or-v1-your-api-key-here"
   OPENROUTER_MODEL="anthropic/claude-3.5-sonnet"
   ```

2. **Install Dependencies**:
   ```bash
   pip install python-dotenv requests
   ```

3. **Run Simulation**:
   ```bash
   python chatbot_simulation.py
   ```

4. **Select Configuration**:
   - Choose from available bot configurations (discussionPrep, ielts-writing, etc.)
   - Select student persona (beginner, intermediate, advanced)
   - Watch the automated conversation unfold

## Student Personas

### 1. Curious Beginner
- **Level**: Beginner
- **Style**: Visual and hands-on learning
- **Personality**: Curious but sometimes confused
- **Focus**: Basic skill building

### 2. Struggling Student  
- **Level**: Intermediate
- **Style**: Step-by-step explanations
- **Personality**: Frustrated, needs encouragement
- **Focus**: Overcoming learning obstacles

### 3. Advanced Learner
- **Level**: Advanced
- **Style**: Discussion and debate
- **Personality**: Confident and challenging
- **Focus**: Sophisticated analysis

## Output Format

Results are saved in `simulation_results/` as JSON files containing:

```json
{
  "simulation_metadata": {
    "teacher_config": "Bot name",
    "student_profile": {...},
    "total_exchanges": 10,
    "simulation_date": "2025-09-12T..."
  },
  "conversation": [
    {
      "timestamp": "2025-09-12T...",
      "speaker": "teacher",
      "message": "Welcome message..."
    },
    {
      "timestamp": "2025-09-12T...",
      "speaker": "student", 
      "message": "Student response..."
    }
  ]
}
```

## Bot Configurations Supported

The system works with all bot configurations in `botConfig/`:
- `discussionPrep.json` - Socratic dialogue partner
- `ielts-writing.json` - IELTS writing tutor
- `GCAPanalyst.json` - Social issues analyst
- `feedbackOnOutline.json` - Academic writing feedback
- `policy-discourse-analyst.json` - Policy analysis
- `fun.json` - Entertainment bot
- `learning.json` - General learning assistant

## Customization

### Adding New Student Personas

Edit the `create_student_profiles()` function in `chatbot_simulation.py`:

```python
{
    "name": "your_persona_name",
    "level": "beginner/intermediate/advanced",
    "learning_style": "description of how they learn",
    "personality": "personality traits",
    "subject": "subject area of interest",
    "goal": "learning objective",
    "initial_request": "first thing they'd say",
    "max_questions": 5
}
```

### Adjusting Simulation Parameters

In the `ChatbotSimulation.run_simulation()` method:
- `max_exchanges`: Maximum conversation turns
- `temperature`: Creativity level (0.1-1.0)
- `max_tokens`: Response length limit

## Analysis Use Cases

1. **Bot Performance Testing**: See how different bots handle various student types
2. **Conversation Flow Analysis**: Identify optimal interaction patterns
3. **Student Journey Mapping**: Understand learning progression
4. **Bot Comparison**: Compare effectiveness across configurations
5. **Edge Case Discovery**: Find unusual interaction scenarios

## Example Usage

```bash
$ python chatbot_simulation.py

✅ OpenRouter configuration found
📁 Found 7 bot configurations:
  1. discussionPrep
  2. ielts-writing
  3. GCAPanalyst
  4. feedbackOnOutline
  5. policy-discourse-analyst
  6. fun
  7. learning

Select bot configuration (1-7): 2

👥 Available student profiles:
  1. curious_beginner - beginner level, curious but sometimes confused
  2. struggling_student - intermediate level, frustrated and needs encouragement
  3. advanced_learner - advanced level, confident and challenging

Select student profile (1-3): 1

🚀 Starting simulation with ielts-writing and curious_beginner
```

## Troubleshooting

**API Key Issues**: Check `.env` file and OpenRouter account
**Import Errors**: Ensure OpenRouter tools are properly copied
**Empty Responses**: Check model availability and API quotas
**Long Responses**: Adjust `max_tokens` parameter

## Files Structure

```
Jackie/
├── chatbot_simulation.py          # Main simulation script
├── openrouter/                    # OpenRouter API tools
├── botConfig/                     # Educational bot configurations
├── simulation_results/            # Generated conversation logs
└── SIMULATION_GUIDE.md           # This guide
```
