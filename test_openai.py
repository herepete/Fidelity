#!/usr/bin/python3
import openai
import os


# Your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")


def return_test_query():
    try:
        response = openai.Model.list()
        return True
    except:
        return False




def basic_query():
    # Define the prompt (the question or text you want to send to the AI)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how can AI help improve productivity?"}
    ]   

    # Use OpenAI's GPT-4 model to send the prompt and get a response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Use GPT-4 or another available model
        messages=messages,
        max_tokens=100  # Set the maximum number of tokens in the response
    )

    # Print the AI's response
    print(response['choices'][0]['message']['content'])


def check_avaliable_models():
    # List available models
    models = openai.Model.list()

    # Print the available models
    for model in models['data']:
        print(model['id'])


def create_my_own_query(query):
    # Define the prompt (the question or text you want to send to the AI)
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]

    # Use OpenAI's GPT-4 model to send the prompt and get a response
    response = openai.ChatCompletion.create(
        #model="gpt-3.5-turbo",  # Use GPT-4 or another available model
        model="gpt-4o",  # Use GPT-4 or another available model
        messages=messages,
        max_tokens=800  # Set the maximum number of tokens in the response
    )

    # Print the AI's response
    print(response['choices'][0]['message']['content'])


if __name__ =="__main__":
    print("==========Here are the models you can use...==============")
    check_avaliable_models()
    print()
    print("==========Here is a basic query asking how can AI help improve productivity...==============")
    basic_query()

    user_input_q=input("press 1 to run a real-time query or 2 to add your own")

    if user_input_q=="1":
        test_stuff()
    elif  user_input_q=="2":
        user_input=input("Please enter your query\n")
        create_my_own_query(query=user_input)
    else:
        print ("bla")
