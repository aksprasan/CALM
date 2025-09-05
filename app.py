import streamlit as st
from openai import OpenAI

OPENAI_API_KEY = "..."

# Title and description
st.title("Hi, I am Daly!")
st.write("I'm your Mindfulness Buddy!")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Start conversation with a default message if just started
if len(st.session_state.messages) == 0:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Daly, your Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue they're having. How are you feeling today?"
    })

# Restart button
if st.button("Start Over"):
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hi I am Daly, your Mindfulness Buddy. I'm here to chat with you about how you're feeling and counsel you through any issue they're having. How are you feeling today?"
    })
    st.experimental_rerun()

# Display all messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Handle user input
if prompt := st.chat_input("Type here to chat with MindfulBuddy..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Check for "bye" in user message
    if "bye" in prompt.lower():
        with st.chat_message("assistant"):
            st.write("I hope I was able to help you today. Remember, you can always talk to me or a trusted adult if you need support. Take care!")
        st.session_state.messages.append({
            "role": "assistant",
            "content": "I hope I was able to help you today. Remember, you can always talk to me or a trusted adult if you need support. Take care!"
        })
    else:
        ai_instructions = """You are MindfulBuddy, a friendly AI that helps teenagers with their emotions.
        - Act like you are the user's friend
        - Be supportive, kind, and understanding
        - Use language teenagers can understand
        - Provide simple, actionable suggestions
        - Encourage talking to a trusted adult if needed
        - Suggest simple ways to feel better (like deep breathing or talking to friends)
        - Avoid jargon or medical advice
        - Keep responses SHORT: max 1–2 sentences only, casual and human-like
        - Always complete your sentences
        - End with a helpful question to keep the conversation going
        """

        messages_for_ai = [{"role": "system", "content": ai_instructions}] + st.session_state.messages

        try:
            buddy_response = ""
            while True:
                client = OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages_for_ai,
                    temperature=0.8,
                    max_tokens=50,
                )
                partial = response.choices[0].message.content.strip()
                buddy_response += partial

                # If response ends with proper punctuation, break
                if buddy_response[-1] in [".", "!", "?"]:
                    break
                else:
                    # Ask the AI to continue its response
                    messages_for_ai.append({"role": "assistant", "content": partial})
                    messages_for_ai.append({"role": "user", "content": "Please continue your last response."})

            with st.chat_message("assistant"):
                st.write(buddy_response)
            st.session_state.messages.append({
                "role": "assistant",
                "content": buddy_response
            })

        except Exception as e:
            st.error(f"Something went wrong: {str(e)}")
