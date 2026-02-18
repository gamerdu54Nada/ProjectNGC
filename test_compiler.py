#!/usr/bin/env python3
"""
Test simple du compilateur ConnectScript
"""

import sys
import os

# Add compiler to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'compiler'))

try:
    from compiler import compile_script
    
    # Simple test
    code = """
page Home
-background
--color blue

-button btn
--text "Click"
--color green
"""
    
    print("=" * 70)
    print("🚀 Testing ConnectScript Compiler")
    print("=" * 70)
    
    print("\n📝 Code to compile:")
    print(code)
    
    print("\n⏳ Compiling...")
    result = compile_script(code)
    
    print("\n✅ Compilation Result:")
    print(f"  Success: {result['success']}")
    print(f"  Errors: {len(result['errors'])}")
    print(f"  Warnings: {len(result['warnings'])}")
    
    if result['success']:
        print(f"  JavaScript generated: {len(result['javascript'])} chars")
        print("\n💻 Generated JavaScript (first 500 chars):")
        print(result['javascript'][:500] + "...")
    else:
        print("\n❌ Errors:")
        for error in result['errors']:
            print(f"  - {error}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
