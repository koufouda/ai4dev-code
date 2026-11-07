"""Βήμα 1: η ελάχιστη κλήση σε LLM."""
from dotenv import load_dotenv
load_dotenv()
from litellm import completion

message = {"role": "user", "content": "Ποια είναι η πρωτεύουσα της Κρήτης;"}
resp = completion(model="anthropic/claude-haiku-5-5", messages=[message])
print(resp.choices[0].message.content)
