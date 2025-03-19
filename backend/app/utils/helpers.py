from transformers import pipeline, Conversation

def load_chatbot():
    # Load a pre-trained conversational model from Hugging Face
    chatbot = pipeline("conversational", model="microsoft/DialoGPT-medium")
    return chatbot

def get_chatbot_response(chatbot, message, chat_history=None):
    # Create a Conversation object
    if chat_history:
        # If chat history exists, pass it as past_user_inputs and generated_responses
        conversation = Conversation(
            past_user_inputs=chat_history["past_user_inputs"],
            generated_responses=chat_history["generated_responses"]
        )
        conversation.add_user_input(message)  # Add the new user message
    else:
        # If no chat history, start a new conversation
        conversation = Conversation(message)

    # Get the chatbot's response
    conversation = chatbot(conversation)

    # Extract the chatbot's response
    response = conversation.generated_responses[-1]

    # Return the response and updated conversation state
    return response, {
        "past_user_inputs": conversation.past_user_inputs,
        "generated_responses": conversation.generated_responses
    }