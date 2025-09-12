#!/usr/bin/env python3
"""
Chatbot Simulation System
Creates two LLM-based agents (student and teacher) that interact with each other
based on educational chatbot configurations.
"""

import sys
import json
import time
import random
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

# Add openrouter to path
openrouter_path = Path(__file__).parent / "openrouter"
sdk_path = openrouter_path / "sdk"
sys.path.insert(0, str(openrouter_path))
sys.path.insert(0, str(sdk_path))

try:
    from client import post_chat_completions
    from env import get_openrouter_config
except ImportError as e:
    print(f"Error: Could not import OpenRouter modules: {e}")
    print("Checking paths:")
    print(f"  OpenRouter path exists: {openrouter_path.exists()}")
    print(f"  SDK path exists: {sdk_path.exists()}")
    print(f"  client.py exists: {(sdk_path / 'client.py').exists()}")
    print(f"  env.py exists: {(sdk_path / 'env.py').exists()}")
    sys.exit(1)

class ChatbotAgent:
    """Represents a chatbot agent with a specific configuration and role."""
    
    def __init__(self, config: Dict[str, Any], agent_type: str = "agent"):
        self.config = config
        self.agent_type = agent_type
        self.conversation_history = []
        self.model = config.get("model", "anthropic/claude-3.5-sonnet")
        
    def generate_response(self, message: str, context: Optional[List[Dict]] = None) -> str:
        """Generate a response based on the agent's configuration."""
        
        # Build messages for the API call
        messages = []
        
        # Add system prompt
        system_prompt = self.config.get("systemPrompt", "You are a helpful assistant.")
        messages.append({"role": "system", "content": system_prompt})
        
        # Add conversation context if provided
        if context:
            messages.extend(context)
        
        # Add the current message
        messages.append({"role": "user", "content": message})
        
        # Prepare API payload
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 800,
            "temperature": 0.7
        }
        
        try:
            response = post_chat_completions(payload)
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def get_welcome_message(self) -> str:
        """Get the welcome message for this agent."""
        return self.config.get("welcomePrompt", "Hello! How can I help you today?")

class SimulatedStudent:
    """Creates a simulated student agent with learning characteristics."""
    
    def __init__(self, student_profile: Dict[str, Any]):
        self.profile = student_profile
        self.model = "anthropic/claude-3.5-sonnet"
        self.questions_asked = 0
        self.max_questions = student_profile.get("max_questions", 5)
        
    def generate_student_message(self, teacher_response: Optional[str] = None, topic: Optional[str] = None) -> str:
        """Generate a student message based on profile and context."""
        
        # Build student persona system prompt
        system_prompt = f"""
You are a {self.profile['level']} student with the following characteristics:
- Learning style: {self.profile['learning_style']}
- Personality: {self.profile['personality']}
- Subject interest: {self.profile['subject']}
- Goal: {self.profile['goal']}

You are interacting with an educational chatbot. Act naturally as a student would.
Ask questions, show confusion when appropriate, and engage with the material.
Keep responses concise and realistic for your level.
"""
        
        messages = [{"role": "system", "content": system_prompt}]
        
        if teacher_response is None:
            # Initial message
            content = f"Hi! I'm working on {topic or self.profile['subject']} and need help. {self.profile.get('initial_request', 'Can you help me?')}"
        else:
            # Response to teacher
            content = f"Teacher said: {teacher_response}\n\nAs a student, respond naturally. Ask follow-up questions or show understanding."
        
        messages.append({"role": "user", "content": content})
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": 300,
            "temperature": 0.8
        }
        
        try:
            response = post_chat_completions(payload)
            self.questions_asked += 1
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Sorry, I'm having trouble expressing myself: {str(e)}"
    
    def should_continue(self) -> bool:
        """Determine if the student should continue the conversation."""
        return self.questions_asked < self.max_questions

class ChatbotSimulation:
    """Orchestrates the interaction between student and teacher chatbots."""
    
    def __init__(self, teacher_config_path: str, student_profile: Dict[str, Any]):
        # Load teacher configuration
        with open(teacher_config_path, 'r') as f:
            teacher_config = json.load(f)
        
        self.teacher = ChatbotAgent(teacher_config, "teacher")
        self.student = SimulatedStudent(student_profile)
        self.conversation = []
        self.topic = student_profile.get('topic', 'general learning')
        
    def run_simulation(self, max_exchanges: int = 10) -> List[Dict[str, Any]]:
        """Run the chatbot simulation and return conversation history."""
        
        print(f"🎭 Starting chatbot simulation")
        print(f"📚 Topic: {self.topic}")
        print(f"🎓 Student: {self.student.profile['level']} level, {self.student.profile['personality']}")
        print(f"🤖 Teacher: {self.teacher.config['name']}")
        print("=" * 50)
        
        # Start with teacher's welcome message
        teacher_message = self.teacher.get_welcome_message()
        self.log_message("teacher", teacher_message)
        
        # Generate initial student response
        student_message = self.student.generate_student_message(teacher_message, self.topic)
        self.log_message("student", student_message)
        
        # Continue conversation
        exchanges = 1
        while exchanges < max_exchanges and self.student.should_continue():
            time.sleep(1)  # Brief pause between exchanges
            
            # Teacher responds to student
            context = self.get_recent_context()
            teacher_response = self.teacher.generate_response(student_message, context)
            self.log_message("teacher", teacher_response)
            
            # Check if teacher ended the conversation
            if any(phrase in teacher_response.lower() for phrase in ["goodbye", "session complete", "that's all", "end of"]):
                break
            
            # Student responds to teacher
            student_message = self.student.generate_student_message(teacher_response)
            self.log_message("student", student_message)
            
            exchanges += 1
        
        print(f"\n✅ Simulation complete after {exchanges} exchanges")
        return self.conversation
    
    def log_message(self, speaker: str, message: str):
        """Log a message to the conversation history."""
        timestamp = datetime.now().isoformat()
        entry = {
            "timestamp": timestamp,
            "speaker": speaker,
            "message": message
        }
        self.conversation.append(entry)
        
        # Print to console
        speaker_emoji = "🎓" if speaker == "student" else "🤖"
        print(f"\n{speaker_emoji} {speaker.upper()}:")
        print(f"{message}")
        print("-" * 30)
    
    def get_recent_context(self, num_messages: int = 4) -> List[Dict[str, str]]:
        """Get recent conversation context for the teacher."""
        context = []
        recent_messages = self.conversation[-num_messages:] if len(self.conversation) > num_messages else self.conversation
        
        for entry in recent_messages:
            role = "user" if entry["speaker"] == "student" else "assistant"
            context.append({"role": role, "content": entry["message"]})
        
        return context
    
    def save_results(self, output_path: str):
        """Save the conversation results to a file."""
        results = {
            "simulation_metadata": {
                "teacher_config": self.teacher.config["name"],
                "student_profile": self.student.profile,
                "topic": self.topic,
                "total_exchanges": len(self.conversation),
                "simulation_date": datetime.now().isoformat()
            },
            "conversation": self.conversation
        }
        
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {output_path}")

def create_student_profiles() -> List[Dict[str, Any]]:
    """Create different student profiles for testing."""
    return [
        {
            "name": "curious_beginner",
            "level": "beginner",
            "learning_style": "visual and hands-on",
            "personality": "curious but sometimes confused",
            "subject": "writing skills",
            "goal": "improve academic writing",
            "initial_request": "I need help with essay structure.",
            "max_questions": 6
        },
        {
            "name": "struggling_student", 
            "level": "intermediate",
            "learning_style": "step-by-step explanations",
            "personality": "frustrated and needs encouragement",
            "subject": "critical thinking",
            "goal": "understand how to analyze arguments",
            "initial_request": "I don't understand how to break down complex arguments.",
            "max_questions": 5
        },
        {
            "name": "advanced_learner",
            "level": "advanced",
            "learning_style": "discussion and debate",
            "personality": "confident and challenging",
            "subject": "policy analysis",
            "goal": "develop sophisticated analytical skills",
            "initial_request": "I want to analyze this policy issue more deeply.",
            "max_questions": 8
        }
    ]

def main():
    """Main function to run chatbot simulations."""
    
    # Check OpenRouter setup
    config = get_openrouter_config()
    if not config['has_key']:
        print("❌ OpenRouter API key not found. Please set up your environment.")
        print("See openrouter/sdk/examples/USAGE_GUIDE.md for setup instructions.")
        return
    
    print("✅ OpenRouter configuration found")
    
    # Get available bot configurations
    bot_config_dir = Path(__file__).parent / "botConfig"
    bot_configs = list(bot_config_dir.glob("*.json"))
    
    if not bot_configs:
        print("❌ No bot configurations found in botConfig directory")
        return
    
    print(f"📁 Found {len(bot_configs)} bot configurations:")
    for i, config_path in enumerate(bot_configs):
        print(f"  {i+1}. {config_path.stem}")
    
    # Select bot configuration
    while True:
        try:
            choice = input(f"\nSelect bot configuration (1-{len(bot_configs)}): ")
            selected_config = bot_configs[int(choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
    
    # Select student profile
    student_profiles = create_student_profiles()
    print(f"\n👥 Available student profiles:")
    for i, profile in enumerate(student_profiles):
        print(f"  {i+1}. {profile['name']} - {profile['level']} level, {profile['personality']}")
    
    while True:
        try:
            choice = input(f"\nSelect student profile (1-{len(student_profiles)}): ")
            selected_profile = student_profiles[int(choice) - 1]
            break
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")
    
    # Run simulation
    print(f"\n🚀 Starting simulation with {selected_config.stem} and {selected_profile['name']}")
    
    simulation = ChatbotSimulation(str(selected_config), selected_profile)
    conversation = simulation.run_simulation()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_filename = f"simulation_{selected_config.stem}_{selected_profile['name']}_{timestamp}.json"
    output_path = Path(__file__).parent / "simulation_results" / output_filename
    output_path.parent.mkdir(exist_ok=True)
    
    simulation.save_results(str(output_path))
    
    print(f"\n📊 Simulation Summary:")
    print(f"   • Total exchanges: {len(conversation)}")
    print(f"   • Bot used: {selected_config.stem}")
    print(f"   • Student type: {selected_profile['name']}")
    print(f"   • Results: {output_path}")

if __name__ == "__main__":
    main()
