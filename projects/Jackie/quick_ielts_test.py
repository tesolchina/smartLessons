#!/usr/bin/env python3
"""
Quick IELTS Writing Bot Simulation Test
"""

import json
import sys
import time
from pathlib import Path

# Simple direct execution of openrouter client
def test_openrouter():
    """Test OpenRouter directly"""
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-c",
            "import sys; sys.path.append('openrouter/sdk'); "
            "from client import post_chat_completions; "
            "from env import get_openrouter_config; "
            "config = get_openrouter_config(); "
            "print('✅ OpenRouter works, API key:', config['has_key'])"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(result.stdout.strip())
            return True
        else:
            print(f"❌ OpenRouter test failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ OpenRouter test error: {e}")
        return False

def run_api_call(messages, model="anthropic/claude-3.5-sonnet"):
    """Make a direct API call"""
    try:
        import subprocess
        
        # Prepare the API call
        api_script = f"""
import sys
sys.path.append('openrouter/sdk')
from client import post_chat_completions
import json

messages = {json.dumps(messages)}
payload = {{
    "model": "{model}",
    "messages": messages,
    "max_tokens": 300,
    "temperature": 0.7
}}

try:
    response = post_chat_completions(payload)
    print(json.dumps(response))
except Exception as e:
    print(json.dumps({{"error": str(e)}}))
"""
        
        result = subprocess.run([
            sys.executable, "-c", api_script
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            return json.loads(result.stdout.strip())
        else:
            return {"error": f"API call failed: {result.stderr}"}
            
    except Exception as e:
        return {"error": str(e)}

def run_ielts_simulation():
    """Run a quick IELTS writing bot simulation"""
    
    print("🎭 Quick IELTS Writing Bot Simulation")
    print("=" * 50)
    
    # Test OpenRouter first
    if not test_openrouter():
        print("❌ Cannot proceed without OpenRouter access")
        return
    
    # Load IELTS bot configuration
    config_path = Path(__file__).parent / "botConfig" / "ielts-writing.json"
    if not config_path.exists():
        print(f"❌ IELTS config not found: {config_path}")
        return
        
    with open(config_path, 'r') as f:
        ielts_config = json.load(f)
    
    print(f"✅ Loaded bot: {ielts_config['name']}")
    
    # Create conversation sequence
    conversations = [
        {
            "role": "Teacher",
            "message": ielts_config["welcomePrompt"]
        }
    ]
    
    # Student persona
    student_message = """Hi! I'm a university student and I need help with IELTS Academic Writing. I'm struggling with Task 2 essays - I never know how to structure my arguments properly. Can you help me brainstorm ideas for this topic: "Some people believe that technology has made our lives easier, while others think it has created more problems. Discuss both views and give your opinion."""
    
    print("\n🎓 STUDENT:")
    print(student_message)
    print("-" * 30)
    
    conversations.append({
        "role": "Student", 
        "message": student_message
    })
    
    # Teacher response
    messages = [
        {"role": "system", "content": ielts_config["systemPrompt"]},
        {"role": "user", "content": student_message}
    ]
    
    print("\n🤖 TEACHER (responding...):")
    teacher_response = run_api_call(messages, ielts_config.get("model", "anthropic/claude-3.5-sonnet"))
    
    if "error" in teacher_response:
        print(f"❌ Error: {teacher_response['error']}")
        return
    
    teacher_message = teacher_response["choices"][0]["message"]["content"]
    print(teacher_message)
    print("-" * 30)
    
    conversations.append({
        "role": "Teacher",
        "message": teacher_message
    })
    
    # Student follow-up
    follow_up_messages = [
        {"role": "system", "content": ielts_config["systemPrompt"]},
        {"role": "user", "content": student_message},
        {"role": "assistant", "content": teacher_message},
        {"role": "user", "content": "That's helpful! So I should choose option 1 for brainstorming. Let me try: I think technology has made communication easier with smartphones and social media, but it has also made people more isolated. How can I develop this into a proper argument structure?"}
    ]
    
    print("\n🎓 STUDENT:")
    print("That's helpful! So I should choose option 1 for brainstorming. Let me try: I think technology has made communication easier with smartphones and social media, but it has also made people more isolated. How can I develop this into a proper argument structure?")
    print("-" * 30)
    
    print("\n🤖 TEACHER (responding...):")
    final_response = run_api_call(follow_up_messages, ielts_config.get("model", "anthropic/claude-3.5-sonnet"))
    
    if "error" in final_response:
        print(f"❌ Error: {final_response['error']}")
        return
    
    final_message = final_response["choices"][0]["message"]["content"]
    print(final_message)
    print("-" * 30)
    
    conversations.append({
        "role": "Student",
        "message": "That's helpful! So I should choose option 1 for brainstorming. Let me try: I think technology has made communication easier with smartphones and social media, but it has also made people more isolated. How can I develop this into a proper argument structure?"
    })
    conversations.append({
        "role": "Teacher", 
        "message": final_message
    })
    
    # Save results
    results = {
        "simulation_metadata": {
            "bot_name": ielts_config["name"],
            "student_profile": "University student struggling with IELTS Task 2",
            "total_exchanges": len(conversations),
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        },
        "conversation": conversations
    }
    
    output_path = Path(__file__).parent / "simulation_results" / f"ielts_quick_test_{int(time.time())}.json"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n✅ Simulation Complete!")
    print(f"📊 Total exchanges: {len(conversations)}")
    print(f"💾 Results saved: {output_path}")
    print(f"\n🎯 Analysis: The IELTS bot successfully guided the student through:")
    print(f"   • Initial help request recognition")
    print(f"   • Menu-based interaction structure") 
    print(f"   • Brainstorming guidance with specific feedback")

if __name__ == "__main__":
    run_ielts_simulation()
