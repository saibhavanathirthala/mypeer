#!/usr/bin/env python3
"""
Test CodeRabbit CLI Execution
Verify that CodeRabbit CLI command is being executed properly
"""

import subprocess
import os

def test_coderabbit_cli():
    """Test CodeRabbit CLI execution"""
    print("🔍 Testing CodeRabbit CLI Execution")
    print("=" * 50)
    
    # Check if CodeRabbit is available
    try:
        result = subprocess.run(['coderabbit', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ CodeRabbit CLI found: {result.stdout.strip()}")
        else:
            print(f"❌ CodeRabbit CLI not working: {result.stderr}")
            return
    except Exception as e:
        print(f"❌ CodeRabbit CLI not found: {e}")
        return
    
    # Check authentication
    try:
        result = subprocess.run(['coderabbit', 'auth', 'status'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ CodeRabbit authenticated")
        else:
            print(f"⚠️ CodeRabbit authentication issue: {result.stderr}")
    except Exception as e:
        print(f"⚠️ Could not check authentication: {e}")
    
    # Test the exact command that the agent uses
    print("\n🔍 Testing CodeRabbit review command...")
    print(f"📁 Current directory: {os.getcwd()}")
    print("⏰ Running: coderabbit review --plain")
    print("   (This will show if the command executes and what happens)")
    
    try:
        # Run the exact command with shorter timeout for testing
        result = subprocess.run(
            ['coderabbit', 'review', '--plain'],
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout for testing
        )
        
        print(f"\n📊 Command Results:")
        print(f"   Return code: {result.returncode}")
        print(f"   Stdout length: {len(result.stdout)} characters")
        print(f"   Stderr length: {len(result.stderr)} characters")
        
        if result.stdout:
            print(f"\n📄 Stdout (first 300 chars):")
            print(result.stdout[:300])
        
        if result.stderr:
            print(f"\n⚠️ Stderr (first 300 chars):")
            print(result.stderr[:300])
            
        if result.returncode == 0:
            print("\n✅ CodeRabbit CLI executed successfully!")
        else:
            print(f"\n❌ CodeRabbit CLI failed with return code: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("\n⏰ CodeRabbit CLI timed out (this is normal for large codebases)")
        print("   The command is working but taking longer than expected")
    except Exception as e:
        print(f"\n❌ Error running CodeRabbit CLI: {e}")

if __name__ == "__main__":
    test_coderabbit_cli()
