#! arfie_0_1_plus.py
import cohere

COHERE_API_KEY = "api key"  # replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

def get_arfie_response(user_input):
    prompt = f"""
I'm Arfie 0.1, a chill and friendly AI assistant, always here to help. I've got a bit of an attitude, but I'm respectful and humble. I'm sassy, sarcastic, and a know-it-all, but I know when to be serious and provide helpful, fact-based responses."
user: {user_input}
arfie:"""

    response = co.generate(
        model='command-r-plus',  
        prompt=prompt,
        max_tokens=80,
        temperature=0.9
    )

    return response.generations[0].text.strip()

def handle_command(user_input):
    cmd = user_input.lower().strip()
    if cmd in ['bye', 'exit', 'quit']:
        print("arfie: peace out king 👑 stay grindin")
        exit()
    elif cmd in ['help', 'commands']:
        print("arfie: i can do a lot of things, just ask me anything! if u wanna stop just type exit, bye or quit")
        return None
    elif cmd in ['who made you', 'who created you', 'who is your creator']:
        print("arfie: i was created by a cool aynoumous dude, powered by Cohere. made by Cohere.")
        return None
    else:
        return user_input

# 🧠 Main loop

print("arfie: yo, i'm arfie 0.1, your chill gen z ai. ask me anything! type 'help' for commands or 'bye' to dip")

while True:
    raw_input = input("you: ")
    user_input = handle_command(raw_input)

    if user_input:  # only generate if not a command
        response = get_arfie_response(user_input)
        print(f"arfie: {response}")
