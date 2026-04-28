"""
Server Management Module
Handles starting and monitoring Llama.cpp server
"""
import subprocess
import time
import requests
import sys
from pathlib import Path


class LlamaServerManager:
    """Manages Llama.cpp server lifecycle"""
    
    def __init__(self, server_path=None, port=8080):
        """
        Initialize server manager
        
        Args:
            server_path (str): Path to llama-server executable
            port (int): Port for the server
        """
        self.port = port
        self.server_path = Path(server_path) if server_path else None
        self.process = None
        self.server_url = f"http://localhost:{port}"
    
    def is_running(self):
        """
        Check if Llama.cpp server is currently running
        
        Returns:
            bool: True if server responds to health check
        """
        try:
            response = requests.get(f"{self.server_url}/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def start(self, model="LiquidAI/LFM2.5-VL-450M-GGUF:Q4_0", context_length=2048):
        """
        Start Llama.cpp server
        
        Args:
            model (str): HuggingFace model ID
            context_length (int): Context window size
            
        Returns:
            bool: True if successfully started or already running
        """
        # Check if already running
        if self.is_running():
            print(f"✅ Llama.cpp server already running on {self.server_url}")
            return True
        
        # If no server path provided, ask user
        if not self.server_path:
            print("\n⚠️  Llama.cpp server not running and path not configured")
            print("\nTo auto-start the server, please configure LLAMA_SERVER_PATH in .env")
            print("Example:")
            print('  LLAMA_SERVER_PATH=C:\\path\\to\\llama-b8829-bin-win-cpu-x64\\llama-server')
            return False
        
        # Check if executable exists
        if not self.server_path.exists():
            print(f"❌ Llama-server not found at: {self.server_path}")
            print("\nPlease install llama.cpp or update LLAMA_SERVER_PATH in .env")
            return False
        
        # Start server
        print(f"\n🚀 Starting Llama.cpp server...")
        print(f"   Model: {model}")
        print(f"   Context: {context_length}")
        print(f"   Port: {self.port}")
        
        try:
            cmd = [
                str(self.server_path),
                "-hf", model,
                "-c", str(context_length),
                "--port", str(self.port)
            ]
            
            # Start process (hide window on Windows)
            if sys.platform == "win32":
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                self.process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
            
            # Wait for server to be ready
            print("⏳ Waiting for server to start...")
            max_retries = 30  # 30 seconds timeout
            for i in range(max_retries):
                time.sleep(1)
                if self.is_running():
                    print(f"✅ Server started successfully!")
                    print(f"   URL: {self.server_url}")
                    return True
            
            print("❌ Server failed to start (timeout)")
            return False
            
        except Exception as e:
            print(f"❌ Error starting server: {str(e)}")
            return False
    
    def stop(self):
        """Stop the Llama.cpp server"""
        if self.process:
            print("🛑 Stopping Llama.cpp server...")
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
                print("✅ Server stopped")
            except subprocess.TimeoutExpired:
                self.process.kill()
                print("⚠️  Server forcefully terminated")
            self.process = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.stop()


def ensure_server_running(server_path=None, port=8080):
    """
    Convenience function to ensure Llama.cpp server is running
    
    Args:
        server_path (str): Path to llama-server executable
        port (int): Server port
        
    Returns:
        bool: True if server is running
    """
    manager = LlamaServerManager(server_path, port)
    if not manager.is_running():
        return manager.start()
    return True
