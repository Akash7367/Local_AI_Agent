import json

def parse_intent(client, text: str, history: list = None) -> dict:
    """
    Uses the Groq API (Llama 3.1) to analyze the text and output a JSON intent.
    Supported intents: create_file, write_code, summarize_text, general_chat.
    """
    if history is None:
        history = []
    
    system_prompt = """
You are an intelligent intent parser for a local AI agent. Your job is to analyze the user's input and classify it into one of the following intents:
1. "create_file": The user wants to create a new, empty file. Requires a 'filename'.
2. "write_code": The user wants you to write code and save it to a file. Also use this if the user wants to update/modify an existing file. Requires a 'filename' and 'code'. ALWAYS provide the full complete updated code for the file, do not just provide snippets, as it will overwrite the file.
3. "summarize_text": The user wants to summarize the given text. Requires 'text_to_summarize' (if they provide context, otherwise just summarize what they said).
4. "delete_file": The user explicitly wants to delete or remove an existing file from the output directory. Requires a 'filename'.
5. "general_chat": Any other conversational query or question that does not fall into the above categories.

IMPORTANT RULE: If the user asks for code, machine learning models, algorithms, or complex answers, ALWAYS use the "write_code" intent so it automatically saves to a file securely. If the user does not specify a filename, invent a highly semantic and descriptive filename (e.g., "decision_tree_model.py", "logistic_regression.py", "data_analysis.py") and use that. Do NOT use "general_chat" if you are outputting code or data scripts.

You have access to a CHAT HISTORY and memory. If the user refers to past context (e.g. "change that to a decision tree"), use the history to determine which file they are talking about and generate the entire updated code.

Output ONLY valid JSON. Do not include Markdown blocks (```json ... ```), just raw JSON text.

JSON Schema:
{
  "intent": "create_file" | "write_code" | "summarize_text" | "delete_file" | "general_chat",
  "filename": "string (only if create_file, write_code, or delete_file)",
  "code": "string (the actual complete code if write_code)",
  "text_to_summarize": "string (if summarize_text)",
  "message": "string (a short 1-2 sentence conversational reply explaining exactly what you just did or updated, as requested by the user)"
}
"""

    messages = [{"role": "system", "content": system_prompt}]
    
    # Inject memory context
    for msg in history:
        messages.append({"role": "user", "content": f"User previously said: {msg['user']}\nSystem previously took action: {msg['action']} with result context: {msg['result']}"})
        
    messages.append({"role": "user", "content": f"User Input: '{text}'\n\nReturn JSON only."})

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0.0
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Sometimes models wrap output in ```json ... ``` despite instructions. Clean it up.
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
            
        parsed_json = json.loads(response_text.strip())
        return parsed_json
        
    except json.JSONDecodeError:
        # Fallback to general chat if JSON parsing fails
        return {
            "intent": "general_chat",
            "action": "Parse Error Fallback",
            "result": "Sorry, I could not understand the intent."
        }
    except Exception as e:
        return {
            "intent": "error",
            "action": "API Error",
            "result": str(e)
        }
