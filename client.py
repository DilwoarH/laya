import requests
from tabulate import tabulate

states = [
    "Do you provide an API for sending bulk SMS communications?",
    "Our invoice shows a duplicate charge for last month's messages.",
    "Messages are stuck in pending and are not being delivered.",
    "Please configure a new service to send password-reset notifications.",
    "Can someone demo the product for us?",
    "Where is the documentation for getting set up?",
    "I need help setting up a new Notify service for our team to send email alerts.",
    "We are getting an error saying the API key is invalid when sending a test message.",
    "Our SMS credits were used up unexpectedly and we need to understand the charge.",
    "Can you add a second team member to manage our service and update permissions?",
    "The delivery reports for our letters are missing for the last 24 hours.",
    "Is there a way to send template-based messages to a large customer list?",
    "One of our messages is marked as failed after being sent, can you investigate?",
    "We would like a walkthrough of the product and pricing for a government service.",
    "How do I create a new service and link it to our organisation?"
]

questions = {
    "type_of_request": {
        "type": "choice",
        "instructions": "What type of request is this?",
        "criteria": {
            "question": "A question that the customer is asking", 
            "incident": "An incident that has occurred",
            "problem": "A problem that the user is facing",
            "task": "A specific action that only the team can do, like configuring a system",
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
headers = ("Question", "Answer", "Confidence")

for state in states:
    response = requests.post(
        "http://127.0.0.1:8001/predict",
        json={"state": state, "questions": questions},
    )
    response.raise_for_status()
    answers = response.json()["answers"]

    rows = [
        (
            questions[question]["instructions"],
            answer["choice"],
            f"{answer.get('confidence', 0) * 100:.1f}%",
        )
        for question, answer in answers.items()
    ]

    print("\nQuery from customer:", state, "\n")
    print(tabulate(rows, headers=headers, tablefmt="simple"))
    print("\n" + "="*100 + "\n")
