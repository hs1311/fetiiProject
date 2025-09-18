#!/usr/bin/env python3
"""
GitHub repository setup helper
"""
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def main():
    """Setup GitHub repository"""
    print("🐙 GitHub Repository Setup")
    print("=" * 30)
    
    # Initialize git if not already done
    if not run_command("git status", "Checking git status"):
        if run_command("git init", "Initializing git repository"):
            print("✅ Git repository initialized")
        else:
            print("❌ Failed to initialize git")
            return
    
    # Add all files
    if not run_command("git add .", "Adding files to git"):
        print("❌ Failed to add files")
        return
    
    # Commit files
    if not run_command('git commit -m "Initial commit: GPT-4 LangChain SQL Chatbot"', "Committing files"):
        print("❌ Failed to commit files")
        return
    
    print("\n🎯 Next Steps:")
    print("1. Go to GitHub.com")
    print("2. Create a new repository")
    print("3. Copy the repository URL")
    print("4. Run these commands:")
    print("   git remote add origin <your-repo-url>")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n🚀 Then deploy to Railway using DEPLOYMENT_GUIDE.md")

if __name__ == "__main__":
    main()
