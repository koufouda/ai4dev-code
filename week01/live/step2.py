"""Βήμα 2: τι πραγματικά επιστρέφει το API."""
from dotenv import load_dotenv
load_dotenv()
from litellm import completion

message = {"role": "user", "content": "Ποια είναι η πρωτεύουσα της Κρήτης;"}
resp = completion(model="anthropic/claude-haiku-5-5", messages=[message])
print(resp)
