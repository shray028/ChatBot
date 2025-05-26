import fitz  # PyMuPDF
import tkinter as tk
from tkinter import scrolledtext, filedialog
import requests
import os

class GroqChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Groq Chat Assistant")
        self.root.geometry("800x600")
        
        # Chat history
        self.messages = [
            {
                "role": "system", 
                "content": (
                    "You are a helpful AI assistant. When users attach files, "
                    "carefully analyze the content and answer questions based on it. "
                    "Always reference specific parts of the document when possible."
                )
            }
        ]
        self.attached_file = None
        
        # UI Elements
        self.create_widgets()
        
    def create_widgets(self):
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            state='disabled', 
            font=('Arial', 12) 
        )
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Attachment frame
        attachment_frame = tk.Frame(self.root)
        attachment_frame.pack(fill=tk.X, padx=10)
        
        self.attachment_label = tk.Label(
            attachment_frame, text="No file attached", fg="gray")
        self.attachment_label.pack(side=tk.LEFT)
        
        attach_btn = tk.Button(
            attachment_frame, text="Attach File", command=self.attach_file)
        attach_btn.pack(side=tk.RIGHT, padx=5)
        
        remove_btn = tk.Button(
            attachment_frame, text="Remove", command=self.remove_attachment)
        remove_btn.pack(side=tk.RIGHT)
        
        # Input frame
        input_frame = tk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.user_input = tk.Text(input_frame, height=3, font=('Arial', 12))
        self.user_input.pack(fill=tk.X, side=tk.LEFT, expand=True)
        
        send_btn = tk.Button(
            input_frame, text="Send", height=3, command=self.send_message)
        send_btn.pack(side=tk.RIGHT, padx=5)
        
        # Bind Enter key to send message
        self.user_input.bind("<Return>", lambda e: self.send_message())
        
    def attach_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.attached_file = file_path
            self.attachment_label.config(
                text=os.path.basename(file_path), fg="black")
            
    def remove_attachment(self):
        self.attached_file = None
        self.attachment_label.config(text="No file attached", fg="gray")
        

    def read_file_content(self, file_path):
        try:
            if file_path.lower().endswith('.pdf'):
                return self.read_pdf(file_path)
            elif file_path.lower().endswith(('.txt', '.md', '.csv')):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            else:
                return None
        except Exception as e:
            raise Exception(f"Error reading file: {str(e)}")

    def read_pdf(self, file_path):
        try:
            text = ""
            doc = fitz.open(file_path)
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            raise Exception(f"PDF read error: {str(e)}\nNote: Image-based PDFs cannot be read")

    def send_message(self, event=None):
        user_text = self.user_input.get("1.0", tk.END).strip()
        if not user_text:
            return
            
        full_prompt = user_text
        
        if self.attached_file:
            try:
                file_content = self.read_file_content(self.attached_file)
                if file_content is None:
                    raise Exception("Unsupported file type")
                    
                full_prompt = (
                    f"I have attached a {os.path.splitext(self.attached_file)[1]} file. "
                    f"Here is its content:\n```\n{file_content}\n```\n"
                    f"Now answer this question: {user_text}"
                )
            except Exception as e:
                self.display_message("System", str(e))
                return
        
        # Update message history
        self.messages.append({"role": "user", "content": full_prompt})
        self.display_message("You", user_text)
        self.user_input.delete("1.0", tk.END)
        
        # Get AI response
        self.get_ai_response()
    def get_ai_response(self):
        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
                json={
                    "messages": self.messages,
                    "model": "llama3-70b-8192",
                    "temperature": 0.7
                }
            )
            
            if response.status_code == 200:
                ai_reply = response.json()["choices"][0]["message"]["content"]
                self.display_message("Assistant", ai_reply)
                self.messages.append({"role": "assistant", "content": ai_reply})
            else:
                self.display_message("System", f"API Error: {response.text}")
                
        except Exception as e:
            self.display_message("System", f"Error: {str(e)}")
            
    def display_message(self, sender, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}:\n", 'sender')
        self.chat_display.insert(tk.END, f"{message}\n\n", 'message')
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
        # Configure tags for styling
        self.chat_display.tag_config('sender', foreground='blue', font=('Arial', 12, 'bold'))
        self.chat_display.tag_config('message', font=('Arial', 12))

if __name__ == "__main__":
    GROQ_API_KEY = ""  # Replace with your actual key
    
    root = tk.Tk()
    app = GroqChatApp(root)
    root.mainloop()