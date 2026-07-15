#!/usr/bin/env python3
"""
Fact Fusion Automation - Security Verification Script

Run this BEFORE pushing to GitHub to ensure no secrets are leaked.

Usage:
    python scripts/verify_security.py
"""

import os
import re
import sys
from pathlib import Path

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{text:^60}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*60}{Colors.RESET}\n")

def print_success(text):
    print(f"{Colors.GREEN}✅ {text}{Colors.RESET}")

def print_error(text):
    print(f"{Colors.RED}❌ {text}{Colors.RESET}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.RESET}")

def check_gitignore():
    """Verify .gitignore exists and covers sensitive files"""
    print_header("Checking .gitignore")
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print_error(".gitignore not found!")
        return False
    
    content = gitignore_path.read_text()
    
    required_patterns = [
        ".env",
        "*.key",
        "*.pem",
        "client_secret.json",
        "youtube_token.pickle",
        "__pycache__",
        "*.log",
    ]
    
    all_good = True
    for pattern in required_patterns:
        if pattern in content:
            print_success(f"Pattern '{pattern}' in .gitignore")
        else:
            print_error(f"Pattern '{pattern}' MISSING from .gitignore!")
            all_good = False
    
    return all_good

def check_env_files():
    """Ensure .env files are not committed"""
    print_header("Checking .env files")
    
    # Check if .env exists in repo
    env_files = list(Path(".").rglob(".env"))
    
    if env_files:
        print_error("Found .env files (should be gitignored):")
        for f in env_files:
            print_error(f"  - {f}")
        return False
    else:
        print_success("No .env files found in repo")
    
    # Check .env.example exists
    env_example = Path("config/.env.example")
    if env_example.exists():
        print_success("config/.env.example exists (good template)")
    else:
        print_warning("config/.env.example not found (recommended)")
    
    return True

def check_api_keys_in_code():
    """Scan for potential API keys in code"""
    print_header("Scanning for API keys in code")
    
    # Patterns that indicate real API keys (not placeholders)
    dangerous_patterns = [
        (r'api_key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', 'API key with 20+ chars'),
        (r'apikey\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', 'API key with 20+ chars'),
        (r'secret\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', 'Secret with 20+ chars'),
        (r'token\s*=\s*["\'][a-zA-Z0-9]{20,}["\']', 'Token with 20+ chars'),
        (r'sk_live_[a-zA-Z0-9]{24,}', 'Stripe live key'),
        (r'ghp_[a-zA-Z0-9]{36,}', 'GitHub personal token'),
        (r'xoxb-[a-zA-Z0-9-]{10,}', 'Slack bot token'),
        (r'AIza[a-zA-Z0-9_-]{35}', 'Google API key'),
    ]
    
    # Safe patterns (placeholders)
    safe_patterns = [
        'your_',
        'YOUR_',
        'example',
        'Example',
        'placeholder',
        'xxx',
        '""',
        "''",
        'Get key',
        'get key',
    ]
    
    files_to_scan = list(Path(".").glob("**/*.py")) + \
                    list(Path(".").glob("**/*.toml")) + \
                    list(Path(".").glob("**/*.md"))
    
    found_issues = False
    
    for file_path in files_to_scan:
        # Skip .git directory
        if '.git' in str(file_path):
            continue
        
        try:
            content = file_path.read_text()
            
            for pattern, description in dangerous_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    line_content = match.group(0)
                    
                    # Check if it's a safe placeholder
                    is_safe = any(safe in line_content for safe in safe_patterns)
                    
                    if not is_safe:
                        print_error(f"{file_path}:{line_num} - {description}")
                        print(f"         {line_content}")
                        found_issues = True
                        
        except Exception as e:
            continue
    
    if not found_issues:
        print_success("No exposed API keys found in code")
    
    return not found_issues

def check_oauth_credentials():
    """Check for OAuth credential files"""
    print_header("Checking OAuth credentials")
    
    oauth_files = [
        "client_secret.json",
        "client_secret_*.json",
        "oauth_*.json",
        "youtube_token.pickle",
        "credentials.json",
    ]
    
    found = False
    for pattern in oauth_files:
        files = list(Path(".").glob(f"**/{pattern}"))
        if files:
            print_error(f"OAuth credential file found: {files[0]}")
            found = True
    
    if not found:
        print_success("No OAuth credential files found")
    
    return not found

def check_personal_paths():
    """Check for hardcoded personal paths"""
    print_header("Checking for personal paths")
    
    personal_patterns = [
        r'/home/[a-zA-Z0-9_]+/',
        r'C:\\Users\\[a-zA-Z0-9_]+\\',
        r'/Users/[a-zA-Z0-9_]+/',
    ]
    
    files_to_scan = list(Path(".").glob("**/*.py")) + \
                    list(Path(".").glob("**/*.toml"))
    
    found_issues = False
    
    for file_path in files_to_scan:
        if '.git' in str(file_path):
            continue
        
        try:
            content = file_path.read_text()
            
            for pattern in personal_patterns:
                matches = re.finditer(pattern, content)
                
                for match in matches:
                    # Skip if it's in a comment or example
                    line = content[match.start():match.end()]
                    if 'example' in line.lower() or '#' in line:
                        continue
                    
                    line_num = content[:match.start()].count('\n') + 1
                    print_warning(f"{file_path}:{line_num} - Personal path found: {match.group(0)}")
                    # Don't fail, just warn
                    
        except Exception as e:
            continue
    
    print_success("No critical personal paths found (warnings above are OK)")
    return True

def main():
    print_header("🔒 FACT FUSION SECURITY VERIFICATION")
    print("Running pre-push security checks...\n")
    
    checks = [
        ("Gitignore", check_gitignore),
        (".env Files", check_env_files),
        ("API Keys in Code", check_api_keys_in_code),
        ("OAuth Credentials", check_oauth_credentials),
        ("Personal Paths", check_personal_paths),
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"{name} check failed: {str(e)}")
            results.append((name, False))
    
    # Summary
    print_header("📊 SECURITY CHECK SUMMARY")
    
    all_passed = True
    for name, result in results:
        if result:
            print_success(f"{name}: PASSED")
        else:
            print_error(f"{name}: FAILED")
            all_passed = False
    
    print("\n" + "="*60)
    
    if all_passed:
        print_success("🎉 ALL SECURITY CHECKS PASSED!")
        print("\n✅ This repo is SAFE to push to GitHub")
        print("\nNext steps:")
        print("  1. git add -A")
        print("  2. git commit -m 'Security verified'")
        print("  3. git push -u origin main")
        return 0
    else:
        print_error("❌ SOME SECURITY CHECKS FAILED!")
        print("\n⚠️  DO NOT PUSH until you fix the issues above")
        print("\nTo fix:")
        print("  1. Remove or redact exposed secrets")
        print("  2. Add sensitive files to .gitignore")
        print("  3. Run this script again to verify")
        return 1

if __name__ == "__main__":
    sys.exit(main())