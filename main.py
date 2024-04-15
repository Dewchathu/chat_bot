import re
import search_online as so
import json

with open('chatbot_data.json', 'r') as f:
    data = json.load(f)

functions = data['functions']
responses = data['responses']


def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Counts how many words are presents in each predefined message
    for word in user_message:
        if word in recognised_words:
            message_certainty += 1

    # Calculated the percent of recognised words in a user message
    percentage = float(message_certainty) / float(len(recognised_words))

    # Checks that the required words are in the string
    for word in required_words:
        if word not in user_message:
            has_required_words = False
            break
    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0


def check_all_messages(message):
    highest_prob_list = {}

    for response_id, response_data in responses.items():
        keywords = response_data.get("keywords", [])
        required_words = response_data.get("required_words", [])
        prob = message_probability(message, keywords, response_data.get("single_response", False), required_words)
        highest_prob_list[response_id] = prob

    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return responses[best_match]["response"] if highest_prob_list[best_match] > 0 else so.unknown(massage=message)


def get_response(userInput):
    split_message = re.split(r'\s+|[,;?!.-]\s*', userInput.lower())
    response = check_all_messages(split_message)
    return response


print('Bot: Hey, I am ChatBot. How can I help you today?')

while True:
    user_input = input('You: ')
    if user_input.lower() == 'exit':
        print('Bot: Goodbye!')
        break
    print('Bot: ' + get_response(user_input))
