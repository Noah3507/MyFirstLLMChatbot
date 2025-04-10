import os
import json
import streamlit as st
from openai import OpenAI
from datetime import datetime

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def load_chat_history():
    try:
        with open('chat_history.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return [
            {
                "role": "system",
                "content": "You are a helpful assistant.",
            }
        ]

def save_chat_history(messages):
    with open('chat_history.json', 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)

def init_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = load_chat_history()

def main():
    st.title("🤖 AI 챗봇")
    
    init_session_state()
    
    # 채팅 이력 표시
    for message in st.session_state.messages[1:]:  # 시스템 메시지 제외
        role = "당신" if message["role"] == "user" else "챗봇"
        with st.chat_message(message["role"]):
            st.write(f"{message['content']}")

    # 사용자 입력
    if user_input := st.chat_input("메시지를 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        with st.chat_message("user"):
            st.write(user_input)

        # 챗봇 응답
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            assistant_message = []
            
            response = client.chat.completions.create(
                messages=st.session_state.messages,
                model=model_name,
                stream=True,
                stream_options={'include_usage': True}
            )
            
            for update in response:
                if update.choices and update.choices[0].delta:
                    content = update.choices[0].delta.content or ""
                    assistant_message.append(content)
                    response_placeholder.write("".join(assistant_message))
            
            final_response = "".join(assistant_message)
            st.session_state.messages.append({"role": "assistant", "content": final_response})
            
        # 대화 내용 저장
        save_chat_history(st.session_state.messages)

if __name__ == "__main__":
    main()