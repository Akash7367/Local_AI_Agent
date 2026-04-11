import os
import json

OUTPUT_DIR = "output"

def ensure_output_dir():
    """Ensure the safe output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def create_file(filename: str) -> str:
    """Creates an empty file within the restricted output directory."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, os.path.basename(filename))
    
    try:
        if os.path.exists(filepath):
            return f"File '{filename}' already exists."
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("")
        return f"Successfully created empty file: {filename} in {OUTPUT_DIR}/ folder."
    except Exception as e:
        return f"Error creating file '{filename}': {str(e)}"

def write_code(filename: str, code: str) -> str:
    """Generates a file and writes code to it within the restricted output directory."""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, os.path.basename(filename))
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)
        return f"Successfully wrote code to {filename} in {OUTPUT_DIR}/ folder."
    except Exception as e:
        return f"Error writing code to '{filename}': {str(e)}"

def summarize_text(client, original_text: str) -> str:
    """Uses Groq API to summarize a given text."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes text concisely."},
                {"role": "user", "content": f"Summarize the following text:\n\n{original_text}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error summarizing text: {str(e)}"

def chat(client, message: str) -> str:
    """Uses Groq API for general chat if no specific tools are triggered."""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Answer the user's query directly and concisely."},
                {"role": "user", "content": message}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error processing chat: {str(e)}"

def delete_file(filename: str) -> str:
    """Deletes a file from the restricted output directory."""
    filepath = os.path.join(OUTPUT_DIR, os.path.basename(filename))
    
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            return f"Successfully deleted file: {filename} from {OUTPUT_DIR}/ folder."
        else:
            return f"File '{filename}' does not exist in {OUTPUT_DIR}/ folder."
    except Exception as e:
        return f"Error deleting file '{filename}': {str(e)}"

def execute_intent(client, intent_data: dict, original_text: str) -> dict:
    """Routes the intent to the correct action and returns the results."""
    intent_name = intent_data.get("intent", "general_chat")
    action_taken = ""
    result = ""

    if intent_name == "create_file":
        filename = intent_data.get("filename", "new_file.txt")
        result = create_file(filename)
        action_taken = f"Created File: {filename}"
        
    elif intent_name == "write_code":
        filename = intent_data.get("filename", "script.py")
        code = intent_data.get("code", "# No code provided")
        result = write_code(filename, code)
        action_taken = f"Wrote Code to: {filename}"
        
    elif intent_name == "delete_file":
        filename = intent_data.get("filename", "remove_file.py")
        result = delete_file(filename)
        action_taken = f"Deleted File: {filename}"
        
    elif intent_name == "summarize_text":
        text_to_summarize = intent_data.get("text_to_summarize", original_text)
        result = summarize_text(client, text_to_summarize)
        action_taken = "Summarized Text"
        
    elif intent_name == "general_chat":
        result = chat(client, original_text)
        action_taken = "General Chat Response"
        
    else:
        result = f"Unsupported intent: {intent_name}"
        action_taken = "Error"

    system_msg = intent_data.get("message", "")
    final_output = f"{system_msg}\n\n[System Log: {result}]" if system_msg else result

    return {
        "intent": intent_name,
        "action": action_taken,
        "result": final_output
    }
