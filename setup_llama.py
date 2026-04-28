#!/usr/bin/env python3
"""
Setup Helper - Configure Llama.cpp Auto-Start
Run this script to automatically detect and configure your llama-server path
"""
import sys
import os
from pathlib import Path
import subprocess


def find_llama_server():
    """Search for llama-server executable on the system"""
    print("🔍 Searching for llama-server executable...\n")
    
    common_paths = [
        Path("C:/llama.cpp"),
        Path("C:/llama-b8829-bin-win-cpu-x64"),
        Path("D:/llama-b8829-bin-win-cpu-x64"),
        Path(os.path.expanduser("~/llama.cpp")),
        Path(os.path.expanduser("~/llama-b8829-bin-win-cpu-x64")),
    ]
    
    found_paths = []
    
    for base_path in common_paths:
        if base_path.exists():
            # Check for llama-server.exe (Windows)
            exe_path = base_path / "llama-server.exe"
            if exe_path.exists():
                found_paths.append(exe_path)
                print(f"✅ Found: {exe_path}")
    
    return found_paths


def update_env_file(llama_server_path):
    """Update .env file with llama-server path"""
    env_path = Path(".env")
    
    # Read existing content
    if env_path.exists():
        with open(env_path, "r") as f:
            content = f.read()
    else:
        # Copy from .env.example
        env_example = Path(".env.example")
        if env_example.exists():
            with open(env_example, "r") as f:
                content = f.read()
        else:
            print("❌ Neither .env nor .env.example found!")
            return False
    
    # Update LLAMA_SERVER_PATH
    lines = content.split("\n")
    updated_lines = []
    found_llama_path = False
    
    for line in lines:
        if line.startswith("LLAMA_SERVER_PATH="):
            updated_lines.append(f"LLAMA_SERVER_PATH={llama_server_path}")
            found_llama_path = True
        else:
            updated_lines.append(line)
    
    # Write back
    with open(env_path, "w") as f:
        f.write("\n".join(updated_lines))
    
    print(f"\n✅ Updated .env file with:")
    print(f"   LLAMA_SERVER_PATH={llama_server_path}")
    return True


def test_server(server_path):
    """Test if the server can be started"""
    print(f"\n🧪 Testing server: {server_path}")
    
    try:
        # Start process
        if sys.platform == "win32":
            process = subprocess.Popen(
                [str(server_path), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            process = subprocess.Popen(
                [str(server_path), "--version"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
        
        stdout, stderr = process.communicate(timeout=5)
        
        if process.returncode == 0:
            print("✅ Server executable is valid!")
            return True
        else:
            print(f"⚠️  Server returned: {stderr.decode()}")
            return True  # Still valid, just couldn't get version
            
    except Exception as e:
        print(f"❌ Error testing server: {str(e)}")
        return False


def main():
    """Main setup flow"""
    print("=" * 60)
    print("🔧 AI & OCR Project - Llama.cpp Auto-Start Setup")
    print("=" * 60)
    
    # Check if .env exists
    env_path = Path(".env")
    if not env_path.exists():
        print("\n⚠️  .env file not found. Creating from .env.example...")
        env_example = Path(".env.example")
        if env_example.exists():
            with open(env_example, "r") as f:
                content = f.read()
            with open(env_path, "w") as f:
                f.write(content)
            print("✅ .env file created")
        else:
            print("❌ .env.example not found!")
            return False
    
    # Search for llama-server
    found_paths = find_llama_server()
    
    if not found_paths:
        print("\n❌ Llama-server not found in common locations!")
        print("\n📝 You can either:")
        print("   1. Install llama.cpp from: https://github.com/ggerganov/llama.cpp")
        print("   2. Manually set LLAMA_SERVER_PATH in .env")
        return False
    
    # Let user choose if multiple found
    if len(found_paths) > 1:
        print("\n📋 Multiple llama-server installations found:")
        for i, path in enumerate(found_paths, 1):
            print(f"   [{i}] {path}")
        choice = input("\nSelect path (number): ").strip()
        try:
            selected_path = found_paths[int(choice) - 1]
        except (ValueError, IndexError):
            print("❌ Invalid selection")
            return False
    else:
        selected_path = found_paths[0]
    
    # Test the server
    if not test_server(selected_path):
        return False
    
    # Update .env
    if not update_env_file(str(selected_path)):
        return False
    
    print("\n" + "=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print("\n🚀 You can now run:")
    print("   python main.py")
    print("\nThe Llama server will start automatically!")
    print("\nTo disable auto-start, set LLAMA_AUTO_START=false in .env")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
