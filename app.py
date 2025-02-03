import streamlit as st
import requests
import json
from datetime import datetime
import os
import base64

class QuantumAIChatApp:
    def __init__(self):
        # Set up page configuration
        st.set_page_config(
            page_title="Quantum AI Chat 🔬🧠",
            page_icon="🌐",
            layout="wide"
        )
        
        # Initialize session state
        self.initialize_session_state()
        
        # Create conversations directory
        self.conversations_dir = "quantum_conversations"
        os.makedirs(self.conversations_dir, exist_ok=True)

    def initialize_session_state(self):
        # Initialize session state variables
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        if 'conversation_history' not in st.session_state:
            st.session_state.conversation_history = []

    def generate_unique_filename(self):
        # Generate a unique filename for conversation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.conversations_dir}/quantum_chat_{timestamp}.json"

    def save_conversation(self):
        # Save current conversation to a file
        filename = self.generate_unique_filename()
        with open(filename, 'w') as f:
            json.dump(st.session_state.messages, f, indent=4)
        st.success(f"Conversation saved: {filename} 💾")

    def load_conversation(self, filename):
        # Load a specific conversation
        with open(filename, 'r') as f:
            st.session_state.messages = json.load(f)
        st.success(f"Conversation loaded: {filename} 📂")

    def validate_api_key(self, api_key):
        """Validate API key format"""
        return api_key and api_key.startswith("oneness_")

    def quantum_ai_request(self, user_message):
        # Get API key from session state
        api_key = st.session_state.get('api_key')
        if not api_key:
            return "Please enter your API key in the sidebar 🔑"
        
        if not self.validate_api_key(api_key):
            return "Invalid API key format. Key must start with 'oneness_' 🚫"

        # Send request to Quantum AI endpoint
        try:
            response = requests.post(
                "http://192.168.2.98:3000/chat", 
                json={
                    "message": user_message,
                    "api_key": api_key
                },
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 401:
                return "Invalid or expired API key 🔒"
            elif response.status_code == 429:
                return "Too many requests. Please wait a moment and try again ⏳"
            
            data = response.json()
            return data.get('response') or "No response from Quantum AI. Please try again 🤖"
        except Exception as e:
            return f"Error connecting to Quantum AI: {str(e)} 🚨"

    def quantum_script_execute(self, quantum_script):
        # Get API key from session state
        api_key = st.session_state.get('api_key')
        if not api_key:
            return {"error": "Please enter your API key in the sidebar 🔑"}
        
        if not self.validate_api_key(api_key):
            return {"error": "Invalid API key format. Key must start with 'oneness_' 🚫"}

        # Execute quantum script via endpoint
        try:
            response = requests.post(
                "http://192.168.2.98:3000/execute", 
                json={
                    "quantum_script": quantum_script,
                    "api_key": api_key
                },
                headers={
                    "X-API-Key": api_key,
                    "Content-Type": "application/json"
                },
                timeout=30
            )
            
            if response.status_code == 401:
                return {"error": "Invalid or expired API key 🔒"}
            elif response.status_code == 429:
                return {"error": "Too many requests. Please wait a moment and try again ⏳"}
            
            return response.json()
        except Exception as e:
            return {"error": f"Execution failed: {str(e)}"}

    def render_sidebar(self):
        # Sidebar for conversation management
        st.sidebar.title("Quantum AI Chat 🌈")
        
        # API Key Input
        api_key = st.sidebar.text_input(
            "Enter API Key 🔑",
            type="password",
            value=st.session_state.get('api_key', ''),
            help="Your API key should start with 'oneness_'"
        )
        
        if api_key:
            if self.validate_api_key(api_key):
                st.session_state.api_key = api_key
                st.sidebar.success("API key format valid ✅")
            else:
                st.sidebar.error("Invalid API key format. Key must start with 'oneness_' ❌")
        
        # Conversation saving
        if st.sidebar.button("Save Conversation 💾"):
            self.save_conversation()
        
        # Conversation loading
        saved_conversations = [
            f for f in os.listdir(self.conversations_dir) 
            if f.endswith('.json')
        ]
        
        selected_conversation = st.sidebar.selectbox(
            "Load Previous Conversation 📂", 
            ["Select a conversation"] + saved_conversations
        )
        
        if selected_conversation != "Select a conversation":
            full_path = os.path.join(self.conversations_dir, selected_conversation)
            if st.sidebar.button("Load Selected Conversation"):
                self.load_conversation(full_path)

        # Quantum Script Section
        st.sidebar.subheader("Quantum Script Executor 🔬")
        quantum_script = st.sidebar.text_area("Enter Quantum Cirq Script", height=200)
        
        if st.sidebar.button("Execute Quantum Script 🚀"):
            result = self.quantum_script_execute(quantum_script)
            st.sidebar.json(result)

    def render_chat_interface(self):
        # Main chat interface
        st.title("Quantum AI Conversational Interface 🌐🤖")
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Ask me anything about Quantum Computing! 🧠"):
            # Add user message to chat history
            st.session_state.messages.append(
                {"role": "user", "content": prompt}
            )
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Get AI response
            with st.chat_message("assistant"):
                with st.spinner("Quantum AI is thinking... 🤔"):
                    response = self.quantum_ai_request(prompt)
                    st.markdown(response)
            
            # Add AI response to chat history
            st.session_state.messages.append(
                {"role": "assistant", "content": response}
            )

    def run(self):
        # Render sidebar and main interface
        self.render_sidebar()
        self.render_chat_interface()

# Run the Quantum AI Chat App
if __name__ == "__main__":
    app = QuantumAIChatApp()
    app.run()
