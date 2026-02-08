#!/usr/bin/env python3
"""
Phi-2 Chatbot GUI optimized for Intel i3-1215U with 8GB RAM
"""

import os
import sys
import time
import re
import threading
from datetime import datetime
from pathlib import Path
import customtkinter as ctk
from tkinter import scrolledtext, filedialog, messagebox

try:
    from llama_cpp import Llama
except Exception as e:
    print("ERROR: llama_cpp not available. Install it with: pip install llama-cpp-python")
    print("Detail:", e)
    sys.exit(1)

# --------- Config ----------
MODELS_DIR = Path("")
MODEL_FILE = "phi-2.Q4_K_M.gguf"  # Your downloaded Phi-2 model

# Optimized for your i3-1215U with 8GB RAM
N_CTX = 2048
N_THREADS = 8  # Matches your CPU threads
N_BATCH = 256  # Reduced to save memory
MAX_TOKENS = 100  # Reduced to prevent long generations
TEMPERATURE = 0.2  # Lower for more focused responses
TOP_P = 0.8
TOP_K = 30
REPETITION_PENALTY = 1.2
HISTORY_LENGTH = 3  # Reduced for memory constraints

# Theme settings
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

# --------- Helpers ----------
def find_model_file(models_dir: Path, forced: str = None):
    if forced:
        p = models_dir / forced
        if p.exists():
            return str(p.resolve())
        raise FileNotFoundError(f"Forced model file not found: {p}")
    
    ggufs = sorted(models_dir.glob("*.gguf"))
    if not ggufs:
        ggufs = sorted(models_dir.rglob("*.gguf"))
    if not ggufs:
        raise FileNotFoundError(f"No .gguf found in {models_dir}")
    
    # Look for Phi-2 first
    for f in ggufs:
        if "phi-2" in f.name.lower() or "phi2" in f.name.lower():
            return str(f.resolve())
    
    return str(ggufs[0].resolve())

def clean_text(s: str) -> str:
    s = "".join(ch for ch in s if ch.isprintable())
    s = re.sub(r'\s+\n', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip()

def strip_markers(s: str):
    # Remove Phi-2 specific artifacts
    s = re.sub(r'(\n|^)\s*[\.:]\s*', '', s)
    s = re.sub(r'(\n|^)\s*[A-Z][a-z]+:\s*', '', s)
    s = re.sub(r'(\n|^)\s*\*+\s*', '', s)
    return s

def safe_postprocess(raw: str) -> str:
    t = clean_text(raw)
    t = strip_markers(t)
    
    # Remove anything after the first end of sentence if it's too long
    if len(t) > 150:
        end_pos = max(t.find('. '), t.find('? '), t.find('! '))
        if end_pos != -1:
            t = t[:end_pos+1]
    
    return t.strip()

# --------- GUI Application ----------
class ChatApp(ctk.CTk):
    def __init__(self, llm):
        super().__init__()
        
        self.llm = llm
        self.history = []
        self.generating = False
        
        self.title("Phi-2 Chatbot")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create chat text area
        self.chat_text = scrolledtext.ScrolledText(
            self, 
            wrap="word", 
            state="disabled",
            font=("Arial", 12),
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            padx=15,
            pady=15
        )
        self.chat_text.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")
        
        # Configure tags for different message types
        self.chat_text.tag_config("user", foreground="#4fc3f7", font=("Arial", 12, "bold"))
        self.chat_text.tag_config("ai", foreground="#81c784", font=("Arial", 12, "bold"))
        self.chat_text.tag_config("timestamp", foreground="#aaaaaa")
        
        # Create input field
        self.input_field = ctk.CTkEntry(
            self, 
            placeholder_text="Type your message here...",
            font=("Arial", 14),
            height=40
        )
        self.input_field.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        self.input_field.bind("<Return>", self.send_message)
        
        # Create send button
        self.send_button = ctk.CTkButton(
            self, 
            text="Send", 
            command=self.send_message,
            font=("Arial", 12, "bold"),
            height=40,
            width=80
        )
        self.send_button.grid(row=1, column=1, padx=5, pady=10, sticky="ew")
        
        # Create button frame for additional buttons
        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=5, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Create clear button
        self.clear_button = ctk.CTkButton(
            self.button_frame, 
            text="Clear Chat", 
            command=self.clear_chat,
            font=("Arial", 12),
            height=35
        )
        self.clear_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Create save button
        self.save_button = ctk.CTkButton(
            self.button_frame, 
            text="Save Chat", 
            command=self.save_chat,
            font=("Arial", 12),
            height=35
        )
        self.save_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Status label
        self.status_label = ctk.CTkLabel(
            self.button_frame,
            text="Ready",
            font=("Arial", 10),
            text_color="#aaaaaa"
        )
        self.status_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")
        
        # Focus on input field
        self.input_field.focus()
        
        # Add welcome message
        self.add_to_chat("AI", "Hello! I'm Phi-2, ready to assist you. How can I help you today?")
    
    def update_status(self, message):
        self.status_label.configure(text=message)
    
    def add_to_chat(self, sender, message):
        self.chat_text.configure(state="normal")
        
        # Add timestamp
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_text.insert("end", f"[{timestamp}] ", "timestamp")
        
        # Add sender tag
        if sender == "You":
            self.chat_text.insert("end", "You: ", "user")
        else:
            self.chat_text.insert("end", "AI: ", "ai")
        
        # Add message
        self.chat_text.insert("end", message + "\n\n")
        
        # Scroll to bottom
        self.chat_text.see("end")
        self.chat_text.configure(state="disabled")
    
    def send_message(self, event=None):
        if self.generating:
            return
            
        user_input = self.input_field.get().strip()
        if not user_input:
            return
        
        # Clear input field
        self.input_field.delete(0, "end")
        
        # Add user message to chat
        self.add_to_chat("You", user_input)
        
        # Start generation in a separate thread
        self.generating = True
        self.send_button.configure(state="disabled")
        self.input_field.configure(state="disabled")
        self.update_status("Generating response...")
        threading.Thread(target=self.generate_response, args=(user_input,), daemon=True).start()
    
    def build_prompt(self, user_message: str):
        # Build context from history
        context = ""
        for u, a in self.history[-HISTORY_LENGTH:]:
            context += f"Human: {u}\nAssistant: {a}\n"
        
        # Phi-2 prompt format
        prompt = f"""Instruction: Provide a helpful, concise response to the human's request.

{context}Human: {user_message}
Assistant:"""
        
        return prompt
    
    def generate_response(self, user_input):
        prompt = self.build_prompt(user_input)
        
        try:
            # Generate response with conservative parameters
            out = self.llm(
                prompt,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                top_k=TOP_K,
                repeat_penalty=REPETITION_PENALTY,
                stop=["Human:", "###", "\n\n", "<|endoftext|>"],
                echo=False
            )
            
            raw = out.get("choices", [{}])[0].get("text", "")
            response = safe_postprocess(raw)
            
            if not response:
                response = "[No response generated]"
            
            # Append to history
            self.history.append((user_input, response))
            
        except Exception as e:
            response = f"[Model error]: {e}"
            if "out of memory" in str(e).lower():
                response += "\nHint: Try reducing MAX_TOKENS or HISTORY_LENGTH"
        
        # Update GUI in the main thread
        self.after(0, self.show_response, response)
    
    def show_response(self, response):
        self.add_to_chat("AI", response)
        self.generating = False
        self.send_button.configure(state="normal")
        self.input_field.configure(state="normal")
        self.update_status("Ready")
        self.input_field.focus()
    
    def clear_chat(self):
        self.chat_text.configure(state="normal")
        self.chat_text.delete(1.0, "end")
        self.chat_text.configure(state="disabled")
        self.history = []
        self.add_to_chat("AI", "Chat history cleared. How can I help you?")
    
    def save_chat(self):
        """Save the chat conversation to a file"""
        try:
            # Get the chat content
            self.chat_text.configure(state="normal")
            chat_content = self.chat_text.get(1.0, "end-1c")
            self.chat_text.configure(state="disabled")
            
            if not chat_content.strip():
                messagebox.showwarning("Warning", "No chat content to save!")
                return
            
            # Ask user for file location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ],
                title="Save Chat Conversation"
            )
            
            if file_path:
                # Save as text file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("Phi-2 Chat Conversation\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(chat_content)
                
                messagebox.showinfo("Success", f"Chat saved successfully to:\n{file_path}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save chat: {str(e)}")

# --------- Main function ----------
def main():
    # Prepare model
    try:
        model_path = find_model_file(MODELS_DIR, MODEL_FILE)
    except Exception as e:
        print("Model file error:", e)
        print("Put a .gguf model file under:", MODELS_DIR)
        sys.exit(1)

    print("Using model:", model_path)
    print("Loading model (this can take a minute)...")

    try:
        llm = Llama(
            model_path=model_path,
            n_ctx=N_CTX,
            n_threads=N_THREADS,
            n_batch=N_BATCH,
            verbose=False
        )
    except Exception as e:
        print("Failed to initialize model:", e)
        sys.exit(1)

    print("✅ Model loaded. (CPU mode)")
    
    # Create and run GUI
    app = ChatApp(llm)
    app.mainloop()

if __name__ == "__main__":
    main()
