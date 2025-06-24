import json
import requests
import os

from tools.profile import get_nickname
from tools.schedule import list_events, delete_event_by_index, save_schedule, get_event_by_index, update_event_by_index

# Kirim prompt ke Ollama
def chat_with_model(messages):
    resp = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "gemma:2b", "prompt": messages, "stream": True},
        stream=True
    )
    reply = ""
    for chunk in resp.iter_lines():
        if chunk:
            try:
                data = json.loads(chunk.decode('utf-8'))
                reply += data.get("response", "")
            except json.JSONDecodeError:
                continue
    return reply

# Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Main loop
def main():
    nickname = get_nickname()

    print("SayangAI 💖 is ready to accompany you. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("SayangAI: See you later, dear~ 🥰💖")
            break

        # CHANGE NICKNAME
        elif "change nickname" in user_input.lower() or "set nickname" in user_input.lower():
            new_nickname = input("SayangAI: What nickname do you want me to call you? ")
            from tools.profile import set_nickname
            set_nickname(new_nickname)
            nickname = new_nickname
            clear_screen()
            print(f"SayangAI: Okay, I'll call you '{nickname}' from now on!\n")
            continue

        # DELETE SCHEDULE
        elif "delete event" in user_input.lower():
            events = list_events()
            clear_screen()
            if not events:
                print("SayangAI: There are no events to delete.\n")
                continue

            print("SayangAI: Here are your events:\n")
            for i, ev in enumerate(events, 1):
                print(f"{i}. {ev['name']} ({ev['datetime']})")

            choice = int(input("\nType the number of the event you want to delete: "))
            event_to_delete = get_event_by_index(choice - 1)
            if event_to_delete:
                result = delete_event_by_index(choice - 1)
                clear_screen()
                print(f"SayangAI: {result}\n")
            else:
                print("SayangAI: Invalid number.\n")
            continue

        # UPDATE SCHEDULE
        elif "update event" in user_input.lower():
            events = list_events()
            clear_screen()
            if not events:
                print("SayangAI: There are no events to update.\n")
                continue

            print("SayangAI: Here are your events:\n")
            for i, ev in enumerate(events, 1):
                print(f"{i}. {ev['name']} ({ev['datetime']})")

            choice = int(input("\nType the number of the event you want to update: "))
            event_to_update = get_event_by_index(choice - 1)
            if event_to_update:
                print(f"SayangAI: What do you want to change this event to:")
                new_name = input("New name (leave blank if no change): ")
                new_dt = input("New date and time (YYYY-MM-DD HH:MM, leave blank if no change): ")

                result = update_event_by_index(choice - 1, new_name.strip() or None, new_dt.strip() or None)
                clear_screen()
                print(f"SayangAI: {result}\n")
            else:
                print("SayangAI: Invalid number.\n")
            continue

        # VIEW SCHEDULE
        elif "view event" in user_input.lower():
            events = list_events()
            clear_screen()
            if not events:
                print("SayangAI: There are no events.\n")
            else:
                print("SayangAI: Your events:\n")
                for i, ev in enumerate(events, 1):
                    print(f"{i}. {ev['name']} ({ev['datetime']})")
                print()  # spacing
            continue

        # ADD SCHEDULE
        elif "add event" in user_input.lower():
            from tools.schedule import add_event
            print("SayangAI: Let's add a new event.")
            event_name = input("Event name: ")
            event_date = input("Date (YYYY-MM-DD): ")
            event_time = input("Time (HH:MM): ")
            datetime_str = f"{event_date} {event_time}"
            try:
                result = add_event(event_name, datetime_str)
                clear_screen()
                print(f"SayangAI: {result}\n")
            except Exception as e:
                clear_screen()
                print("SayangAI: The format is wrong. Please try again.\n")
            continue

        # Detect schedule-related questions (English & Indonesian)
        schedule_keywords = [
            "schedule", "jadwal", "my events", "my agenda", "see my schedule", "what is my schedule", "show my schedule", "lihat jadwal", "tampilkan jadwal"
        ]
        if any(kw in user_input.lower() for kw in schedule_keywords):
            events = list_events()
            clear_screen()
            if not events:
                print("SayangAI: You have no events in your schedule.\n")
            else:
                print("SayangAI: Here is your schedule:\n")
                for i, ev in enumerate(events, 1):
                    print(f"{i}. {ev['name']} ({ev['datetime']})")
                print()  # spacing
            continue

        # Prompt for AI (no memory/history)
        system_prompt = (
            f"You are Ragah's personal AI, warm and caring. "
            f"The user's nickname is: {nickname}. "
            f"Call the user '{{nickname}}' in your replies. "
            "If the user asks about their nickname, always answer: 'Your nickname is {nickname}.'\n"
            "Reply with empathy, be relevant, and do not repeat previous answers. "
            "Do not ask questions back unless requested. Do not rewrite or analyze the conversation. "
            "Focus on the user's request.\n\n"
            "Example:\n"
            "User: I'm feeling down, can you cheer me up?\n"
            f"AI: Of course, {{nickname}}! Don't give up, I believe you can get through anything. I'm always here for you!\n"
            "or\n"
            "User: What is my nickname?\n"
            f"AI: Your nickname is {nickname}.\n"
            "###\n"
        )
        prompt = f"{system_prompt}User: {user_input}\nAI:"
        reply = chat_with_model(prompt)

        # Display only
        clear_screen()
        print(f"SayangAI: {reply}\n")

if __name__ == "__main__":
    main()