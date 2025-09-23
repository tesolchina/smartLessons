#!/usr/bin/env python3
"""
Basic OpenRouter API Usage Example

This script demonstrates the simplest way to use the OpenRouter module
for basic LLM interactions.

Usage:
    python basic_example.py

Requirements:
    - OPENROUTER_API_KEY set in .env file
    - python-dotenv installed
"""

import sys
from pathlib import Path

# Add parent directory to import openRouterAI
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def test_basic_api_call():
    """Test basic API functionality with simple examples"""
    
    print("🤖 Basic OpenRouter API Example")
    print("=" * 40)
    
    try:
        from openRouterAI.client import post_chat_completions
        from openRouterAI.env import get_openrouter_config
        
        # Check configuration
        config = get_openrouter_config()
        print(f"🔧 Using model: {config['model']}")
        print(f"🔑 API key configured: {config['has_key']}")
        
        if config['has_key'] != 'True':
            print("❌ API key not found. Please check your .env file.")
            return False
        
        print("\\n📡 Making API call...")
        
        # Simple example
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user", 
                    "content": "Explain the concept of machine learning in exactly 2 sentences."
                }
            ],
            "max_tokens": 100,
            "temperature": 0.7
        }
        
        response = post_chat_completions(payload)
        answer = response["choices"][0]["message"]["content"]
        
        print("✅ Response received!")
        print("\\n💬 LLM Response:")
        print("-" * 40)
        print(answer)
        print("-" * 40)
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you're running from the examples directory")
        return False
    except Exception as e:
        print(f"❌ API call failed: {e}")
        print("💡 Check your API key and internet connection")
        return False

def test_structured_analysis():
    """Example of using structured prompts for analysis"""
    
    print("\\n🔍 Structured Analysis Example")
    print("=" * 40)
    
    try:
        from openRouterAI.client import post_chat_completions
        from openRouterAI.env import get_openrouter_config
        
        config = get_openrouter_config()
        
        sample_text = """
        Climate change is one of the most pressing challenges of our time. 
        The scientific consensus is clear: human activities, particularly the 
        burning of fossil fuels, are the primary driver of recent climate change. 
        However, there is still debate about the best solutions, with some 
        advocating for renewable energy transitions while others propose 
        technological solutions like carbon capture.
        """
        
        # Structured analysis prompt
        payload = {
            "model": config['model'],
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Analyze the following text and provide a structured response:

TEXT:
{sample_text.strip()}

Please provide:
1. MAIN_TOPIC: [One sentence summary]
2. TONE: [Objective/Subjective/Neutral/etc.]
3. KEY_CLAIMS: [List 2-3 main claims]
4. EVIDENCE_LEVEL: [High/Medium/Low]
5. PERSPECTIVE: [Balanced/One-sided/Mixed]

Format as structured output.
                    """
                }
            ],
            "max_tokens": 300,
            "temperature": 0.1  # Lower temperature for consistent analysis
        }
        
        print("📡 Analyzing sample text...")
        response = post_chat_completions(payload)
        analysis = response["choices"][0]["message"]["content"]
        
        print("✅ Analysis complete!")
        print("\\n📊 Structured Analysis:")
        print("-" * 40)
        print(analysis)
        print("-" * 40)
        
        return True
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

def test_conversation_flow():
    """Example of multi-turn conversation"""
    
    print("\\n💬 Conversation Flow Example")
    print("=" * 40)
    
    try:
        from openRouterAI.client import post_chat_completions
        from openRouterAI.env import get_openrouter_config
        
        config = get_openrouter_config()
        
        # Multi-turn conversation
        messages = [
            {"role": "user", "content": "What are the main benefits of renewable energy?"},
        ]
        
        # First turn
        payload = {
            "model": config['model'],
            "messages": messages,
            "max_tokens": 150,
            "temperature": 0.7
        }
        
        print("💬 Turn 1: Asking about renewable energy...")
        response1 = post_chat_completions(payload)
        answer1 = response1["choices"][0]["message"]["content"]
        
        print("✅ Response 1 received")
        print(f"🤖 Assistant: {answer1[:100]}...")
        
        # Add response to conversation history
        messages.append({"role": "assistant", "content": answer1})
        messages.append({"role": "user", "content": "What are the main challenges in implementing these solutions?"})
        
        # Second turn
        payload["messages"] = messages
        
        print("\\n💬 Turn 2: Following up on challenges...")
        response2 = post_chat_completions(payload)
        answer2 = response2["choices"][0]["message"]["content"]
        
        print("✅ Response 2 received")
        print(f"🤖 Assistant: {answer2[:100]}...")
        
        print("\\n✅ Conversation flow successful!")
        return True
        
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 OpenRouter Basic Examples")
    print("=" * 50)
    print()
    
    # Run all tests
    tests = [
        ("Basic API Call", test_basic_api_call),
        ("Structured Analysis", test_structured_analysis), 
        ("Conversation Flow", test_conversation_flow)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\\n🧪 Running: {test_name}")
        success = test_func()
        results.append((test_name, success))
    
    # Summary
    print("\\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    successful = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            successful += 1
    
    print(f"\\n🎯 Results: {successful}/{len(tests)} tests passed")
    
    if successful == len(tests):
        print("\\n🎉 All tests passed! Your OpenRouter setup is working correctly.")
        print("\\n💡 Next steps:")
        print("   - Try the LLM Text Analyzer: llm_text_analyzer.py")
        print("   - Check Speaker Separation: speaker_separation_example.py") 
        print("   - Read the full guide: USAGE_GUIDE.md")
    else:
        print("\\n⚠️  Some tests failed. Check your API key and network connection.")
        print("   - Run: python test_environment.py")
        print("   - Check: .env file in repository root")
        print("   - Verify: OPENROUTER_API_KEY is set correctly")
