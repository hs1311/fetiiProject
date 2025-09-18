#!/usr/bin/env python3
"""
Quick deployment helper for FetiiPro GPT-4 Chatbot
"""
import os
import subprocess
import sys

def check_files():
    """Check if all required files exist"""
    required_files = [
        'src/langchain_chatbot.py',
        'src/langchain_web_app.py', 
        'src/simple_setup.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'app.json'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files present")
    return True

def check_git():
    """Check if git is initialized"""
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            return True
        else:
            print("❌ Git not initialized")
            return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def check_api_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found in environment")
        return True
    else:
        print("⚠️  OpenAI API key not found in environment")
        print("   You'll need to set it in Railway dashboard")
        return False

def main():
    """Main deployment check"""
    print("🚀 FetiiPro GPT-4 Chatbot Deployment Check")
    print("=" * 50)
    
    # Check files
    if not check_files():
        print("\n❌ Please ensure all required files are present")
        return
    
    # Check git
    if not check_git():
        print("\n❌ Please initialize git repository first")
        print("   Run: git init")
        return
    
    # Check API key
    check_api_key()
    
    print("\n🎯 Next Steps:")
    print("1. Create GitHub repository")
    print("2. Push your code to GitHub")
    print("3. Go to Railway.app")
    print("4. Connect GitHub repository")
    print("5. Set OPENAI_API_KEY environment variable")
    print("6. Deploy!")
    
    print("\n📖 For detailed instructions, see DEPLOYMENT_GUIDE.md")
    print("🚀 Your GPT-4 chatbot is ready for deployment!")

if __name__ == "__main__":
    main()
