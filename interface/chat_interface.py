from engine.inference_engine import match_intent

def run_chat():
    print("💬 Welcome to the Smart Banking Assistant!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit']:
            print("Assistant: Goodbye! 👋")
            break
        
        intent, response = match_intent(user_input)
        print("Assistant:", response)
