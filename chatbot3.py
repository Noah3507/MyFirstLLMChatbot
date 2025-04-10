import os
from openai import OpenAI

token = os.environ["GITHUB_TOKEN"]
endpoint = "https://models.inference.ai.azure.com"
model_name = "gpt-4o"

client = OpenAI(
    base_url=endpoint,
    api_key=token,
)

def chat_with_bot():
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        }
    ]
    
    while True:
        user_input = input("\n당신: ")
        if user_input.lower() == 'bye':
            print("챗봇: 안녕히 가세요!")
            break
            
        messages.append({"role": "user", "content": user_input})
        
        response = client.chat.completions.create(
            messages=messages,
            model=model_name,
            stream=True,
            stream_options={'include_usage': True}
        )
        
        print("\n챗봇: ", end="")
        usage = None
        for update in response:
            if update.choices and update.choices[0].delta:
                print(update.choices[0].delta.content or "", end="")
            if update.usage:
                usage = update.usage
                
        messages.append({
            "role": "assistant",
            "content": "".join(update.choices[0].delta.content or "" for update in response if update.choices and update.choices[0].delta)
        })

if __name__ == "__main__":
    print("챗봇과 대화를 시작합니다. 종료하려면 'bye'를 입력하세요.")
    chat_with_bot()