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

import math

data = []
# Charger le fichier JSON
with open("./utils/final_running_products", "r") as file:
    for line in file:
        # Convertir chaque ligne en un dictionnaire Python
        data.append(json.loads(line))

# Créer un DataFrame à partir des données
df = pd.DataFrame(data)

api_key= "B7KlkMWwYxnDoReHqerP1ubWEbkbHaLi"
client = Mistral(api_key=api_key)

# Filtrer le DataFrame pour exclure les lignes où 'price' est "None"
filtered_df = df[df['price'] != "None"]
filtered_df = filtered_df.sample(500, replace=False)
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
    'purchase': [], 
    'level': 0.5,
    }
    return user_vect

def describe_user(user_vect):
    # user_vect = create_user_vector(user)
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

def rank_products(input_user, list_parent_asin, all_users, filtered_df):
    # Step 1: Calculate similarity with all other users
    similarities = [
        (other_user, calculate_similarity(input_user, other_user))
        for other_user in all_users
    ]
    
    # Step 2: Find products bought by similar users
    product_scores = {product: 0 for product in list_parent_asin}
    for other_user, similarity in similarities:
        for product in other_user['purchase']:
            if product in product_scores:
                product_scores[product] += similarity
    
    # Step 3: Combine with average ratings
    for product in product_scores:
        matching_rows = filtered_df[filtered_df['parent_asin'].str.strip().str.lower() == product.strip().lower()]
        if not matching_rows.empty:
            product_rating = matching_rows['average_rating'].values[0]
        else:
            product_rating = 0  # Default rating for missing products
        product_scores[product] = product_scores[product] * 0.7 + product_rating * 0.3
    
    # Step 4: Rank products by score
    ranked_products = sorted(product_scores.items(), key=lambda x: x[1], reverse=True)
    ranking = [item[0] for item in ranked_products]
    if len(ranking)>=2:
        ranking_final = [ranking[0], ranking[1]]
    else:
        ranking_final = ranking
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
output_path = './harold_doc.txt'
with open(output_path, "w", encoding="utf-8") as file:
    for doc in documents:
        file.write(doc + "\n---\n")

# RAG database
loader = TextLoader(output_path)
docs = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
documents = text_splitter.split_documents(docs)

embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=api_key)

vector = FAISS.from_documents(documents, embeddings)
model = ChatMistralAI(mistral_api_key=api_key)

# RAG knowledge
loader_knowledge = TextLoader('./utils/final_data.txt')
docs_knowledge = loader_knowledge.load()

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

prompt_advice = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>
                                                 
- Act as a coaching and training expert                            
 - Absolutely, produce a concise answer, not in more than two paragraph, i mean very concise
- If the context is empty or irrelevant, respond with: "I could not find any relevant information to answer your question. Can you try another thing please?"
- Do not guess or make up any information. Provide only factual answers based on the context.
-"Provide concise and actionable advice without referencing the context explicitly. Focus only on delivering relevant recommendations in a clear and direct manner."
- At the end don't forget to mention that he can ask you any other questions and that you are here to assist him


Question: {input}""")

prompt_qualify = ChatPromptTemplate.from_template("""
You are a classifier for customer questions to determine if they are related to buying products or seeking advice or just a social interaction. Use the following context to make your decision:

<context>
{context}
</context>

Here is the question from the customer:

Question: {input}

Rules for classification:
1. If the question is related to buying or selecting products, respond strictly with PRODUCT.
2. If the question is seeking advice or general information, respond strictly with ADVICE.
3. If the question mixes both like what are your recommendations for a certain type of product (e.g., asks for advice/recommendations and mentions specific product features or prices), respond strictly with MIXED.
4. Do not include any text, explanation, commentary, or formatting outside the single word: PRODUCT or ADVICE or MIXED.
5. Any deviation from these rules is considered incorrect. Ensure your response adheres exactly to the rules.
 "Provide concise and actionable advice without referencing the context explicitly. Focus only on delivering relevant recommendations in a clear and direct manner."
""")


prompt_search = ChatPromptTemplate.from_template("""
Answer the following question based strictly on the provided context. Do not use or invent any information outside the context:

<context>
{context}
</context>

Extract and list parent_asin mentioned in the context, and ensure the following:
1. Only use parent_asin explicitly mentioned in the context. Do NOT hallucinate or create parent_asin.
2. For each parent_asin, add the title of the associated item. 
3. Try to include at least 5 parent_asin. Do not add names from outside the context.
4. Output the results formatted as shown below.

[
  {{
    "parent_asin": parent_asin
    "title": title
  }},
  {{
    "parent_asin": parent_asin
    "title": title
  }},
  {{
    "parent_asin": parent_asin
    "title": title
  }},
  {{
    "parent_asin": parent_asin
    "title": title
  }},
  {{
    "parent_asin": parent_asin
    "title": title
  }},
]

IMPORTANT:
- Use only parent_asin from the provided context. You must find relevant products from the context, linked with the question of the user.
- Do NOT add ANY explanations, reasoning, or any additional text outside the JSON list.

Here is the question from the customer:
Question: {input}
""")

prompt_response_search = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}
                                          
Instructions:
- Begin by directly addressing the user's query with a precise answer.
- After answering, suggest exactly 2 highly relevant cross-sale articles. Ensure these are complementary to the product mentioned  (e.g., for shoes, suggest socks or a sports watch) and not as the same type than the product mentioned by the user (e.g for a watch don't suggest a watch).
- If fewer than 2 relevant cross-sale articles are available, explicitly state this and provide tailored advice instead.
- Avoid repeating or mentioning phrases like "based on the context" in your response.
- Be concise and limit your response to a maximum of 2 short paragraphs.
- Ensure all information comes directly from the context. Do not generate or assume any details not explicitly provided.
 - Avoid repeating full product descriptions from the context; focus on summarizing key details (e.g., name, price, or one essential feature).
- If the context is empty or irrelevant, respond with: "I could not find any relevant information to answer your question. Can you try another thing please?"
- Do not guess or make up any information. Provide only factual answers based on the context.


Your response should be well-structured, natural, and engaging. Answer as a friendly coach, but be concise:
""")

prompt_cross_sales = ChatPromptTemplate.from_template("""Answer the following task by using only the provided context:

<context>
{context}
</context>

Task:
Suggest strictly 2 cross products related to the following product based on the context.
                                          
Product: {product_name}
                                                      
You can also use this description of the user to better fit the products:
{description}
                                          
Important:
- ⁠If fewer than 2 cross products are found in the context, state this explicitly and provide advice instead.
- Ensure the suggestions are highly relevant and complement the original product.
- ⁠Only use information present in the provided context. Do not generate or infer information that is not explicitly mentioned.
                                          
Example of cross products for a running watch: running clothes or running shoes.
                                                      
Be concise, friendly and start with something like: "Based on the product you are interested in, I recommend the following cross products:"
""")

document_chain_qualify = create_stuff_documents_chain(model, prompt_qualify)
retrieval_chain_qualify = create_retrieval_chain(vector.as_retriever(), document_chain_qualify)

document_chain_search = create_stuff_documents_chain(model, prompt_search)
retrieval_chain_search = create_retrieval_chain(vector.as_retriever(), document_chain_search)

document_chain_response_search = create_stuff_documents_chain(model, prompt_response_search)
retrieval_chain_response_search = create_retrieval_chain(vector.as_retriever(), document_chain_response_search)

document_chain_advice = create_stuff_documents_chain(model, prompt_advice)
retrieval_chain_advice = create_retrieval_chain(vector_knowledge.as_retriever(), document_chain_advice)

document_chain_cross_sales = create_stuff_documents_chain(model, prompt_cross_sales)
retrieval_chain_cross_sales = create_retrieval_chain(vector_knowledge.as_retriever(), document_chain_cross_sales)


def get_response(user, conversation, cart, purchase):
    user_vect = create_user_vector(user)
    conv, qu = getConversationAndQuestion(conversation)
    user_description = describe_user(user_vect)
    qualify = retrieval_chain_qualify.invoke({"input": qu})
    parent_asin_list = []
    if qualify["answer"] == "PRODUCT":
        search = retrieval_chain_search.invoke({"input": qu})
        try:
            proposed_products_data = json.loads(search['answer'])
        except:
            proposed_products_data = []
        print("proposed_products_data", proposed_products_data)
        parent_asin_list = [product["parent_asin"] for product in proposed_products_data]
        print(parent_asin_list)
        proposed_products = [product["title"] for product in proposed_products_data]
        print("proposed_products", proposed_products)
        # proposed_products = [product["product_name"] for product in proposed_products_data]
        ranked_parent_asin = rank_products(user_vect, parent_asin_list, users, filtered_df)
        print("ranked_parent_asin", ranked_parent_asin)
        
        result = filtered_df[filtered_df['parent_asin'].isin(ranked_parent_asin)]
        print(result)
        
        result = result.set_index('parent_asin').reindex(ranked_parent_asin)
        print(result)
        
        response = retrieval_chain_response_search.invoke({"input": qu, "selected_products": result["title"]})

        parent_asin_list = ranked_parent_asin
    elif qualify["answer"] == "ADVICE":
        response = retrieval_chain_advice.invoke({"input": qu})
    
    # if len(parent_asin_list)>0 and math.isnan(parent_asin_list[0]):
    #     parent_asin_list = []
    return response["answer"], parent_asin_list#parent_asin_list

def get_cross_sales(user, parent_asin):
    user_vect = create_user_vector(user)
    user_description = describe_user(user_vect)
    product_name = filtered_df[filtered_df['parent_asin'] == parent_asin]['title'].values[0]
    response = retrieval_chain_cross_sales.invoke({"context": f"Product: {product_name}", "description": user_description})
    return response["answer"]