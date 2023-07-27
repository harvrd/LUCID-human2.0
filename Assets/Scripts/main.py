# main script that calls and sends messages to headset

import openai
import time
from langchain.text_splitter import CharacterTextSplitter
import UdpComms as U
# from dotenv import load_dotenv
import key

# load_dotenv()

sock = U.UdpComms(udpIP="127.0.0.1", portTX=8000, portRX=8001, enableRX=True, suppressWarnings=True)

# Set up OpenAI API key
# openai.api_key = os.environ.get("OPENAI_API_KEY")
# print("key", os.environ.get("OPENAI_API_KEY"))

openai.api_key = key.key()

def getLatestConversation():
    with open("Assets/Scripts/transcript.txt", "r") as f:
        conversation = f.read()

    return conversation

text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=3800, chunk_overlap=0)

counts = [0, 0, 0, 0, 0]
labels = ["Long Summarize", "Fact Check", "Ideate", "Define Terms", "Short Summarize"]
   
def counter(user_input):
    if user_input == "1":
        counts[0] += 1
    elif user_input == "2":
        counts[1] += 1
    elif user_input == "3":
        counts[2] += 1
    elif user_input == "4":
        counts[3] += 1
    elif user_input == "5":
        counts[4] += 1
    else:
        print("Invalid input")
        exit()
    with open("Assets/Scripts/report.txt", "w") as f:
        for i, label in enumerate(labels):
            f.write(f"{label}: {counts[i]}\n")

def getHelp(user_input):
    # Get Current Conversation
    prompt=""
    conversation = getLatestConversation()
    texts = text_splitter.split_text(conversation)
    # get last element of texts
    conversationCut = texts[-1]
    # Get the response based on the user's input
    prompts_map = {
        "1": "Summarize the entire conversation in a concise bulleted response between 65-85 words.",
        "2": "Please point out any possible assumptions or errors in the last few sentences. Respond in a concise bulleted response between 65-85 words.",
        "3": "Ideate based on the last few sentences to assist the user in this conversation in a concise bulleted response between 65-85 words.",
        "4": "Define any terms in the last few sentences that may not have immediately obvious meanings or aren't commonly known. Respond in a concise bulleted response between 65-85 words.",
        "5": "Summarize the last few sentences in a concise bulleted response between 65-85 words.",
    }
    
    if user_input not in prompts_map:
        sock.SendData("Invalid input")
        return "Invalid input"
    
    counter(user_input)

    # Get the model's response to the chosen prompt
    print("Thinking...")
    fullPrompt = "\"\"\"" + conversationCut + "\"\"\"\n" + prompts_map[user_input]
    full_string = ""
    for chunk in openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "This is a conversation with an AI assistant. Assistant is listening to a conversation between two people, and is instructed to assist the user in conversation in 1. summarizing conversation 2. fact checking 3. ideation. Based on one of the three things, the AI gives its best answer. The conversation is below"},
            {"role": "user", "content": fullPrompt}
        ],
        stream=True,
    ):
        content = chunk["choices"][0].get("delta", {}).get("content")
        if content is not None:
            # check for new prompt from user
            input = sock.ReadReceivedData()
            if input != None:
                print("got new prompt")
                getHelp(input)
                return "exited early"
            
            full_string += content
            sock.SendData(full_string)
            print(content, end="")
    return full_string


i = 0
sock.SendData("Project LUCID: Please Enter a Thought Command.")

print("Program started...")
while True:
    input = sock.ReadReceivedData()
    if input != None:
        print("input", input)
        getHelp(input)
        time.sleep(1)

