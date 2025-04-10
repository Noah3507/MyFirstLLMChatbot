import os
import json
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

def chat_with_bot():
    messages = load_chat_history()
    
    while True:
        user_input = input("\n당신: ")
        if user_input.lower() == 'bye':
            print("챗봇: 안녕히 가세요!")
            save_chat_history(messages)
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            stream=True,
            stream_options={'include_usage': True}
        )
        
        print("\n챗봇: ", end="")
        assistant_message = []
        usage = None
        for update in response:
            if update.choices and update.choices[0].delta:
                content = update.choices[0].delta.content or ""
                print(content, end="")
                assistant_message.append(content)
            if update.usage:
                usage = update.usage
                
        messages.append({
            "role": "assistant",
            "content": "".join(assistant_message)
        })
        
        # 매 응답 후 대화 내용 저장
        save_chat_history(messages)

if __name__ == "__main__":
    print("챗봇과 대화를 시작합니다. 종료하려면 'bye'를 입력하세요.")
    chat_with_bot()