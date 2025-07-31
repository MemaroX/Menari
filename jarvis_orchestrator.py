import requests
import json
import subprocess

OLLAMA_API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "jarvis"

def run_tool(tool_name):
    if tool_name == "get_current_time":
        try:
            result = subprocess.run(["python", "get_current_time.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "get_system_info":
        try:
            result = subprocess.run(["python", "get_system_info.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "get_cpu_usage":
        try:
            result = subprocess.run(["python", "get_cpu_usage.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "get_memory_usage":
        try:
            result = subprocess.run(["python", "get_memory_usage.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "list_processes":
        try:
            result = subprocess.run(["python", "list_processes.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "get_disk_usage":
        try:
            result = subprocess.run(["python", "get_disk_usage.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    elif tool_name == "get_network_info":
        try:
            result = subprocess.run(["python", "get_network_info.py"], capture_output=True, text=True, check=True)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error executing tool: {e.stderr}"
    else:
        return f"Unknown tool: {tool_name}"

def chat_with_jarvis(messages):
    data = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=data)
        response.raise_for_status()
        result = response.json()
        
        full_response_content = result["message"]["content"]
        
        # Check for tool call
        if full_response_content.startswith("TOOL_CALL:"):
            tool_call_parts = full_response_content.split(":", 1)
            if len(tool_call_parts) > 1:
                tool_name = tool_call_parts[1].strip()
                print(f"J.A.R.V.I.S. requested tool: {tool_name}")
                tool_output = run_tool(tool_name)
                print(f"Tool output: {tool_output}")
                
                # Append J.A.R.V.I.S.'s tool call request to messages
                messages.append({"role": "assistant", "content": full_response_content})
                
                # Send tool output back to J.A.R.V.I.S. as a new user message
                messages.append({"role": "user", "content": f"Tool output for {tool_name}: {tool_output}"})
                
                # Make another call to Ollama with the tool output
                data["messages"] = messages
                response = requests.post(OLLAMA_API_URL, json=data)
                response.raise_for_status()
                result = response.json()
                
                # Append J.A.R.V.I.S.'s final response to messages
                final_jarvis_response = result["message"]["content"]
                messages.append({"role": "assistant", "content": final_jarvis_response})
                return final_jarvis_response, messages
            else:
                return "J.A.R.V.I.S. requested an invalid tool call format.", messages
        else:
            # If no tool call, append J.A.R.V.I.S.'s response to messages
            messages.append({"role": "assistant", "content": full_response_content})
            return full_response_content, messages

    except requests.exceptions.RequestException as e:
        return f"Error communicating with Ollama: {e}", messages

if __name__ == "__main__":
    print(f"Connecting to Ollama model: {MODEL_NAME}")
    print("Type 'exit' to quit.")
    messages = [] # Initialize messages list for conversation history
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        
        messages.append({"role": "user", "content": user_input}) # Add user message to history
        
        jarvis_response, messages = chat_with_jarvis(messages) # Pass and receive messages
        print(f"J.A.R.V.I.S.: {jarvis_response}")
