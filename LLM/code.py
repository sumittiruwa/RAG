from groq import Groq

client = Groq(api_key="GROQ_API_KEY")

question = input("Ask something: ")

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "user", "content": question}
    ]
)

print("\nLLM Response:")
print(response.choices[0].message.content)