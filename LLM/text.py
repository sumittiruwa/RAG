from groq import Groq

client = Groq(api_key="GROQ_API_KEY")

text = """
Artificial Intelligence is a branch of computer science.
It allows machines to learn from data and perform tasks
that normally require human intelligence.
"""

response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {
            "role": "user",
            "content": f"Summarize this text in 2 sentences:\n{text}"
        }
    ]
)

print(response.choices[0].message.content)