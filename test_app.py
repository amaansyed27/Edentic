#!/usr/bin/env python3
"""
Test script to verify Edentic app structure without running Streamlit
"""

import sys
import ast

def test_app_structure():
    """Test that the app has all required functions"""
    
    print("🧪 Testing Edentic App Structure...")
    
    try:
        # Parse the app.py file
        with open('app.py', 'r', encoding='utf-8') as f:
            tree = ast.parse(f.read())
        
        # Extract function names
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        
        # Required functions for multimedia support
        required_functions = [
            'init_clients',
            'upload_and_analyze_mixed_media',
            'create_comprehensive_content_plan', 
            'generate_missing_content',
            'assemble_multimedia_video',
            'main'
        ]
        
        print(f"📊 Found {len(functions)} functions in app.py")
        print("Functions:", ', '.join(functions))
        
        # Check for required functions
        missing_functions = []
        for func in required_functions:
            if func in functions:
                print(f"✅ {func} - Found")
            else:
                print(f"❌ {func} - Missing")
                missing_functions.append(func)
        
        if missing_functions:
            print(f"\n❌ Missing {len(missing_functions)} required functions!")
            return False
        else:
            print(f"\n✅ All {len(required_functions)} required functions found!")
            
        # Check imports
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend([alias.name for alias in node.names])
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
        
        required_imports = ['streamlit', 'videodb', 'google.genai', 'PIL']
        print(f"\n📦 Checking imports...")
        for imp in required_imports:
            if any(imp in imported for imported in imports):
                print(f"✅ {imp} - Imported")
            else:
                print(f"⚠️ {imp} - Not found (may be conditional)")
        
        print(f"\n🎬 Edentic App Structure Test: PASSED!")
        print("✨ Ready for multimedia content creation!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing app structure: {e}")
        return False

if __name__ == "__main__":
    success = test_app_structure()
    sys.exit(0 if success else 1)
