from sentence_transformers import SentenceTransformer
import pinecone
import openai
import os
import streamlit as st
openai.api_key = "your api key"
model = SentenceTransformer('all-MiniLM-L6-v2')



#pinecone_api_key = os.environ.get("PINECONE_API_KEY")
# Create an instance of the Pinecone class
pc = pinecone.Pinecone(api_key="your api key")



#index = pc.Index("quickstart")

# Now you can perform operations using the 'pc' instance, such as creating an index
if 'my-index-name' not in pc.list_indexes().names():
    pc.create_index(
        name='my-index-name',
        dimension=1536,
        metric='euclidean',
        spec=pinecone.ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

def find_match(input):
    input_em = model.encode(input).tolist()
    result = index.query(input_em, top_k=2, includeMetadata=True)
    return result['matches'][0]['metadata']['text']+"\n"+result['matches'][1]['metadata']['text']

def query_refiner(conversation, query):

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Given the following user query and conversation log, formulate a question that would be the most relevant to provide the user with an answer from a knowledge base.\n\nCONVERSATION LOG: \n{conversation}\n\nQuery: {query}\n\nRefined Query:",
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return response['choices'][0]['text']

def get_conversation_string():
    conversation_string = ""
    for i in range(len(st.session_state['responses'])-1):

        conversation_string += "Human: "+st.session_state['requests'][i] + "\n"
        conversation_string += "Bot: "+ st.session_state['responses'][i+1] + "\n"
    return conversation_string
