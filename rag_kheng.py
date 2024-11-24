# ! pip install faiss-cpu==1.7.4 mistralai
# !pip install langchain langchain-mistralai langchain_community mistralai==1.2.3

from langchain_community.document_loaders import TextLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

from mistralai import Mistral
import requests
import numpy as np
import faiss
import os
from getpass import getpass
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import random
import json

# Charger le fichier JSON
df = pd.read_json("final_running_products", lines=True)

api_key= "Hh7heFfENTq0BZAGLaqBodGxkose79gA"
client = Mistral(api_key=api_key)

# Filtrer le DataFrame pour exclure les lignes où 'price' est "None"
filtered_df = df[df['price'] != "None"]
filtered_df['average_rating'] = filtered_df['average_rating']/5
filtered_df = filtered_df.drop_duplicates(subset='parent_asin', keep='first')

user_vector = {
    'sensibility_to_price': round(random.uniform(0, 1), 2),
    'level': round(random.uniform(0, 1), 2),
    'sprint': round(random.uniform(0, 1), 2),
    'semi_long_distance': round(random.uniform(0, 1), 2),
    'long_distance': round(random.uniform(0, 1), 2),
    'ultra_trail': round(random.uniform(0, 1), 2),
    'gender': round(random.uniform(0, 1), 2),
    'age': round(random.uniform(0, 1), 2),
    'health': round(random.uniform(0, 1), 2),
    'purchase': []
}

def create_user_vector(user):
    user_vect = {
    'sensibility_to_price': user.appetance_prix,
    'sprint': user.sprint,
    'semi_long_distance': user.demifond,
    'long_distance': user.fond,
    'ultra_trail': user.ultratrail,
    'gender': user.genre,
    'age': user.age,
    'health': user.sante,
    'purchase': []
    }
    return user_vect

def describe_user(user):
    user_vect = create_user_vector(user)
    description = []
    
    for key, value in user_vect.items():
        if key == 'purchase':
            continue  # Skip the purchase field

        if key == 'gender':
            gender_desc = "female" if value >= 0.5 else "male"
            description.append(f"The user is likely {gender_desc}.")
        elif key == 'age':
            age = int(value * 100)  # Scale age and convert to integer
            description.append(f"The user is approximately {age} years old.")
        elif key == 'level':
            if value < 0.3:
                description.append("The user is a beginner.")
            else:
                description.append("The user has experience in this field.")
        elif key == 'sensibility_to_price':
            if value < 0.3:
                description.append("The user is less sensitive to price.")
            else:
                description.append("The user pays attention to price when making decisions.")
        elif key == 'health':
            if value > 0.5:
                description.append("The user is in good health.")
            else:
                description.append("The user may not be in optimal health.")
        else:
            # Replace underscores with spaces for readability
            variable = key.replace('_', ' ')
            
            if value < 0.3:
                desc = (f"does not seem particularly interested in {variable}, "
                        f"which suggests it might not be a priority for them.")
            elif 0.3 <= value <= 0.7:
                desc = (f"has a moderate inclination towards {variable}, "
                        f"indicating it could be relevant to their preferences.")
            else:
                desc = (f"shows a strong interest in {variable}, "
                        f"highlighting it as an important factor in their choices.")
            
            description.append(f"The user {desc}.")
    
    return " ".join(description)

def generate_user():
    return {
        'sensibility_to_price': round(random.uniform(0, 1), 2),
        'level': round(random.uniform(0, 1), 2),
        'sprint': round(random.uniform(0, 1), 2),
        'semi_long_distance': round(random.uniform(0, 1), 2),
        'long_distance': round(random.uniform(0, 1), 2),
        'ultra_trail': round(random.uniform(0, 1), 2),
        'gender': round(random.uniform(0, 1), 2),
        'age': round(random.uniform(0, 1), 2),
        'health': round(random.uniform(0, 1), 2),
        'purchase': random.sample(list(filtered_df['title']), 5)
    }

# Generate a list of 500 users
users = [generate_user() for _ in range(500)]

def calculate_similarity(user1, user2):
    attributes = ['sensibility_to_price', 'level', 'sprint', 'semi_long_distance',
                  'long_distance', 'ultra_trail', 'health']
    num_user1 = np.array([user1[attribute] for attribute in attributes]).reshape(1, -1)
    num_user2 = np.array([user2[attribute] for attribute in attributes]).reshape(1, -1)

    similarity = cosine_similarity(num_user1, num_user2)
    return similarity[0][0]

def rank_products(input_user, proposed_products, all_users, filtered_df):
    # Step 1: Calculate similarity with all other users
    similarities = [
        (other_user, calculate_similarity(input_user, other_user))
        for other_user in all_users
    ]
    
    # Step 2: Find products bought by similar users
    product_scores = {product: 0 for product in proposed_products}
    for other_user, similarity in similarities:
        for product in other_user['purchase']:
            if product in product_scores:
                product_scores[product] += similarity
    
    # Step 3: Combine with average ratings
    for product in product_scores:
        matching_rows = filtered_df[filtered_df['title'].str.strip().str.lower() == product.strip().lower()]
        if not matching_rows.empty:
            product_rating = matching_rows['average_rating'].values[0]
        else:
            product_rating = 0  # Default rating for missing products
        product_scores[product] = product_scores[product] * 0.7 + product_rating * 0.3
    
    # Step 4: Rank products by score
    ranked_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
    ranking = [item[0] for item in ranked_products]
    ranking_final = [ranking[0], ranking[1]]
    return ranking_final

documents = []
for _, row in filtered_df.iterrows():
    # Convertir les listes en texte lisible
    features = ", ".join(row['features']) if isinstance(row['features'], list) else "No features listed"
    description = " ".join(row['description']) if isinstance(row['description'], list) else "No description available"
    categories = " > ".join(row['categories']) if isinstance(row['categories'], list) else "No categories available"
    
    # Créer le contenu textuel pour chaque produit
    text_content = (
        f"Product Title: {row['title']}\n"
        f"Main Category: {row['main_category']}\n"
        f"Price: ${row['price']}\n"
        f"Average Rating: {row['average_rating']}/5 based on {row['rating_number']} ratings\n"
        f"Features: {features}\n"
        f"Description: {description}\n"
        f"Categories: {categories}\n"
        f"Store: {row['store']}\n"
        f"Parent ASIN: {row['parent_asin']}\n"
        f"Bought Together: {', '.join(row['bought_together']) if isinstance(row['bought_together'], list) else 'No bundles available'}\n"
    )
    documents.append(text_content)

# Enregistrer les documents dans un fichier texte
output_path = r'C:\Users\ngoup\Downloads\documents.txt'
with open(output_path, "w", encoding="utf-8") as file:
    for doc in documents:
        file.write(doc + "\n---\n")

# RAG database
loader = TextLoader(r'C:\Users\ngoup\Downloads\documents.txt')
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)

embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

vector = FAISS.from_documents(documents, embeddings)
model = ChatMistralAI(mistral_api_key=api_key)

# RAG knowledge
loader_knowledge = TextLoader('final_data.txt')
docs_knowledge = loader.load()

documents_knowledge = text_splitter.split_documents(docs_knowledge)

vector_knowledge = FAISS.from_documents(documents_knowledge, embeddings)

def getConversationAndQuestion(conversation):
    conv = ""
    for c in conversation:
        if c==conversation[-1]:
            return conv, c["text"]
        if c["isUser"]:
            conv += "User: " + c["text"] + "\n"
        else:
            conv += "Coach: " + c["text"] + "\n"

prompt_advice = ChatPromptTemplate.from_template("""Answer the question based only on the provided context:

<context>
{context}
</context>
                                                 
You can also use this description of the user:                                          
{description}
                                                 
Before the question, this was the conversation between the user and the coach:
{conversation}
                                          
Here is the question of the user:
Question: {input}
                                          
Answer as a great coach would do, being friendly and well-structured. Avoid mentioning the description of the user but use it to adapt the answer.:""")

prompt_qualify = ChatPromptTemplate.from_template("""
You are a classifier for customer questions to determine if they are related to buying products or seeking advice. Use the following context to make your decision:

<context>
{context}
</context>

Here is the question from the customer:

Question: {input}

Rules for classification:
1. If the question is related to buying or selecting products, respond strictly with PRODUCT.
2. If the question is seeking advice or general information, respond strictly with ADVICE.
3. Do not include any text, explanation, commentary, or formatting outside the single word: PRODUCT or ADVICE.
4. Any deviation from these rules is considered incorrect. Ensure your response adheres exactly to the rules.
""")


prompt_search = ChatPromptTemplate.from_template("""
Answer the following question based strictly on the provided context. Do not use or invent any information outside the context:

<context>
{context}
</context>

Extract and list product names mentioned in the context, and ensure the following:
1. Only use product names explicitly mentioned in the context. Do NOT hallucinate or create product names.
2. Include at least 5 product entries. Do not add names from outside the context.
3. Output the results formatted as shown below.

[
  {{
    "product_name": "Product Name"
  }},
  {{
    "product_name": "Product Name"
  }},
  {{
    "product_name": "Product Name"
  }},
  {{
    "product_name": "Product Name"
  }},
  {{
    "product_name": "Product Name"
  }}
]

IMPORTANT:
- Use only product names from the provided context. You must find the 5 most relevant products from the context products names.
- Do NOT add explanations, reasoning, or any additional text outside the JSON list.

Question: {input}
""")

prompt_response_search = ChatPromptTemplate.from_template("""
You are a helpful, and friendly coach. Answer to the customer's question by presenting one by one the Selected products. You can only use the Selected products provided: 

Selected Products:
{selected_products}                                                   

You can also use the context to provide a better answer:                                                   
<context>
{context}
</context>
                                                          
You can also use this description of the user:                                          
{description}
                                                 
Before the question, this was the conversation between the user and the coach:
{conversation}

Here is the question from the customer:                                                   
Question: {input}


Write a response to the question as a great coach would do. Avoid mentioning the description of the user but use it to adapt the answer.:
""")

document_chain_qualify = create_stuff_documents_chain(model, prompt_qualify)
retrieval_chain_qualify = create_retrieval_chain(vector.as_retriever(), document_chain_qualify)

document_chain_search = create_stuff_documents_chain(model, prompt_search)
retrieval_chain_search = create_retrieval_chain(vector.as_retriever(), document_chain_search)

document_chain_response_search = create_stuff_documents_chain(model, prompt_response_search)
retrieval_chain_response_search = create_retrieval_chain(vector.as_retriever(), document_chain_response_search)

document_chain_advice = create_stuff_documents_chain(model, prompt_advice)
retrieval_chain_advice = create_retrieval_chain(vector_knowledge.as_retriever(), document_chain_advice)

convo = [{"text": "Hello, I want to start training marathon, have you advices?", "isUser": True},{"text": """Hello! I'd be happy to help you prepare for a marathon!

Given your interest in level and sprint, I would recommend incorporating interval training into your routine. This type of training involves alternating between high-intensity and low-intensity periods of exercise, which can help improve your speed and endurance.

For example, you could try running at a fast pace for 1 minute, followed by jogging or walking at a slower pace for 2 minutes. Repeat this cycle for a total of 20-30 minutes, gradually increasing the duration and intensity of your high-intensity intervals over time.

Additionally, since you're planning to run a marathon, it's important to build up your endurance with longer runs. Aim to gradually increase your weekly long run distance by no more than 10% each week. This will help your body adapt to the demands of running for an extended period of time.

Lastly, make sure to listen to your body and take rest days as needed. Incorporating cross-training activities like cycling or swimming can also help prevent injury and add some variety to your routine.

I hope these tips are helpful as you prepare for your marathon! Let me know if you have any other questions.""", "isUser": False}, {"text": "Can you buid me a training program ?", "isUser": True}]

def get_response(user, conversation, cart, purchase):
    user_vect = create_user_vector(user)
    conv, qu = getConversationAndQuestion(conversation)
    user_description = describe_user(user_vector)
    qualify = retrieval_chain_qualify.invoke({"input": qu})
    if qualify["answer"] == "PRODUCT":
        search = retrieval_chain_search.invoke({"input": qu})
        proposed_products_data = json.loads(search['answer'])
        proposed_products = [product["product_name"] for product in proposed_products_data]
        ranked_products = rank_products(user_vect, proposed_products, users, filtered_df)
        response = retrieval_chain_response_search.invoke({"input": qu, "selected_products": ranked_products, "description": user_description, "conversation": conv})
    elif qualify["answer"] == "ADVICE":
        response = retrieval_chain_advice.invoke({"input": qu, "description": user_description, "conversation": conv})
    return response["answer"]