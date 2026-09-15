import json
from pydantic import BaseModel


# 1. Pydantic schema
class SupportTicket(BaseModel):
    name: str
    email: str
    phone: str
    issue: str


# 2. Original sentence
sentence = """
My name is Absaar Khan, my email is absaar@gmail.com,
my phone number is 9876543210 and I am unable to login to my account.
"""


# 3. Extract the information from the sentence
# For now, we manually extract it.
# Later, we will make an LLM do this extraction.

ticket_data = {
    "name": "Absaar Khan",
    "email": "absaar@gmail.com",
    "phone": "9876543210",
    "issue": "Unable to login to my account"
}


# 4. Validate the extracted data using Pydantic
ticket = SupportTicket.model_validate(ticket_data)

print("Pydantic Object:")
print(ticket)


# 5. Convert Pydantic object → JSON
ticket_json = ticket.model_dump_json()

print("\nJSON:")
print(ticket_json)


# 6. Read JSON → Python dictionary
ticket_dict = json.loads(ticket_json)

print("\nPython Dictionary:")
print(ticket_dict)


# 7. Access individual fields
print("\nTicket Details:")
print("Name:", ticket_dict["name"])
print("Email:", ticket_dict["email"])
print("Phone:", ticket_dict["phone"])
print("Issue:", ticket_dict["issue"])

