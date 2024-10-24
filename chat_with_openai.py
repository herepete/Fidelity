#!/usr/bin/python3
import openai
import os


# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_ai():
    messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

    print("Start chatting with the AI! Type 'exit' to end the conversation.")
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Exit the chat loop if the user types 'exit'
        if user_input.lower() == 'exit':
            print("Ending the conversation. Goodbye!")
            break

        # Add the user's message to the conversation history
        messages.append({"role": "user", "content": user_input})

        # Get the AI's response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150  # Set the maximum number of tokens for each response
        )

        # Extract and print the AI's response
        ai_response = response['choices'][0]['message']['content']
        print(f"AI: {ai_response}")

        # Add the AI's response to the conversation history
        messages.append({"role": "assistant", "content": ai_response})


chat_with_ai()
