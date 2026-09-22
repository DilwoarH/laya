import requests
import json

state = """
Hello, I work for a housing software provider, and we are onboarding a local authority for their Housing Register and Choice Based Lettings systems.
We are developing functionality for them to send bulk SMS communications to applicants directly from our system, and would like to integrate with the GOV.UK Notify API.
Can you advise if I need to create an account to set up and test the API or is there anything else I need to provide?
We also have other local authorities that may use this functionality in the future. Do we set up one account for our organisation and then separate API keys for each local authority, or do we need separate accounts?

Thanks in advance, I look forward to hearing from you.
"""

questions = {
    "type_of_request": {
        "type": "choice",
        "instructions": "What type of request is this?",
        "criteria": {
            "question": "A question that the customer is asking", 
            "incident": "An incident that has occurred",
            "problem": "A problem that the user is facing",
            "task": "A specific task that the team needs to do, like configuring a system",
        },
    },
    "notify_responder": {
        "type": "choice",
        "instructions": "Which team should handle this request?",
        "criteria": {
            "billing": "invoices, payments, refunds",
            "technical": "bugs, outages, system errors",
            "non-technical": "new features, improvements, user interviews, surveys, usability testing",
            "escalated": "urgent issues"
        }
    },
    "notify_topic": {
        "type": "choice",
        "instructions": "What is this GOV.UK Notify enquiry about?",
        "criteria": [
            "Accessing Notify",
            "Getting started with Notify",
            "Sending & receiving messages",
            "Managing Service",
            "Managing Organisation",
            "Technical enquiries",
            "Technical problems",
            "Pricing / free allowance",
            "Accessibility",
            "Delivery issues",
            "Something else",
        ]
    }
}

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json={"state": state, "questions": questions},
)
response.raise_for_status()
answers = response.json()["answers"]

for question, answer in answers.items():
    print(f"{question} :", answer["choice"])