import requests
from tabulate import tabulate

states = [
    "Do you provide an API for sending bulk SMS communications?",
    "Our invoice shows a duplicate charge for last month's messages.",
    "Messages are stuck in pending and are not being delivered.",
    "Please configure a new service to send password-reset notifications.",
]

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
