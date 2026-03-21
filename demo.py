from ollama import chat

response = chat(
    model='qwen2.5:0.5b',
    messages=[{'role': 'user', 'content': 'Hello!, you can speak spanish?'}],
)
print(response.message.content)

