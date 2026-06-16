#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import torch
import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer, TextIteratorStreamer # import TextIteratorStreamer instead of TextStreamer
from threading import Thread # We need Thread for stream output in streamlit
import chromadb
from chromadb.utils import embedding_functions
from docx import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


# In[3]:


# ---------------------------------------------------------
# 1. PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(page_title="Game Analysis Chatbot")
st.title("Game Analysis Chatbot")

uploaded_file = st.file_uploader(
    "Upload Knowledge Document",
    type=["docx"]
)

# ---------------------------------------------------------
# 2. CACHE THE MODEL LOADING
# ---------------------------------------------------------
# @st.cache_resource ensures the model is only loaded ONCE into memory.
# Without this, Streamlit will re-download/re-load the model every time the user types!
@st.cache_resource
def load_model():
    # Set visible GPU (change depending on devices, or comment out for CPU)
    os.environ["CUDA_VISIBLE_DEVICES"] = "6" 
    
    model_name = "Qwen/Qwen2.5-0.5B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    
    return model, tokenizer, device


# In[4]:


model, tokenizer, device = load_model()


# In[ ]:


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


# In[ ]:


def load_docx(file):

    doc = Document(file)

    text = "\n".join(
        [p.text for p in doc.paragraphs]
    )

    return text


# In[5]:


# Load ChromaDB
chroma_client = chromadb.PersistentClient(
    path="/Users/testing/Desktop/Study/IS6620/game_analytics_db"
)

local_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="BAAI/bge-small-en-v1.5"
)

collection = chroma_client.get_collection(
    name="game_analytics",
    embedding_function=local_ef
)
if uploaded_file and st.button("Add To Knowledge Base"):

    with st.spinner("Processing document..."):

        text = load_docx(uploaded_file)

        chunks = splitter.split_text(text)

        collection.upsert(
            documents=chunks,
            ids=[
                f"{uploaded_file.name}_{i}"
                for i in range(len(chunks))
            ]
        )

    st.success(
        f"{uploaded_file.name} added to knowledge base."
    )


# In[13]:


#现在只是针对 retention case 的 hard-coded query expansion，现实中用户会不停问不同的问题，我们也不可能时时刻刻帮用户expand问题，所以我们还是需要接入rewriter，改写成适合检索的关键词，由于0.5B 的 rewriter 会乱输出解释。所以我们要给它更强约束，并且做清洗
#另外，为简化操作，将代码用封装函数处理，后续只需要简单提问即可
def ask_rag(question):
    rewrite_prompt = f"""
You are a search query rewriting assistant for a game analytics knowledge base.

Rewrite the user question into ONLY search keywords.

Rules:
- Output one line only.
- Do not answer the question.
- Do not explain your rewrite.
- Keep all important metrics and numbers.
- Add related analytics terms.
- Use noun phrases only.
- No full sentences.

Examples:
User Question: My D1 retention dropped from 40% to 25%. What should I investigate?
Search Query: D1 retention drop 40% 25% root cause analysis onboarding funnel tutorial completion cohort analysis churn feature adoption A/B testing

User Question: My paying users decreased this week. What metrics should I check?
Search Query: paying users decrease monetization funnel payer conversion ARPPU ARPU revenue drop LTV cohort analysis purchase behavior

User Question: My tutorial completion rate dropped by 15%. What could be the root cause?
Search Query: tutorial completion rate drop 15% onboarding funnel progression funnel difficulty spike user drop-off cohort analysis

User Question:
{question}

Search Query:
"""

    tokenized_rewrite = tokenizer(
        rewrite_prompt,
        return_tensors="pt"
    ).to(device)

    rewrite_output = model.generate(
        **tokenized_rewrite,
        max_new_tokens=80,
        do_sample=False
    )

    input_length = tokenized_rewrite["input_ids"].shape[1]
    new_tokens = rewrite_output[0][input_length:]

    rewritten_query = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    ).strip()

    rewritten_query = rewritten_query.split("\n")[0].replace('"', '').strip()

    print("REWRITTEN QUERY:", rewritten_query)

    # Domain filter after query rewriting
    domain_keywords = [
        "retention", "churn", "cohort", "funnel", "a/b", "ab test",
        "ltv", "arpu", "arppu", "revenue", "monetization", "payer",
        "paying users", "session", "tutorial", "onboarding", "conversion",
        "metrics", "root cause", "d1", "d7", "d30", "experiment",
        "hypothesis", "sample size", "statistical significance",
        "player", "user", "game", "engagement", "feature adoption",
        "留存", "流失", "漏斗", "同期群", "付费", "收入",
        "商业化", "指标", "转化", "新手引导", "教程", "时长",
        "活跃", "实验", "假设", "样本", "显著性", "玩家", "用户"
    ]

    if not any(k in rewritten_query.lower() for k in domain_keywords):
        return (
            "This chatbot only supports game analytics questions. "
            "Please ask about retention, churn, funnel, A/B testing, "
            "LTV, monetization, or root cause analysis."
        )

    RAG_results = collection.query(
        query_texts=[rewritten_query],
        n_results=3,
        include=["documents", "distances"]
    )

    retrieved_docs = "\n\n".join(RAG_results["documents"][0])
    top_distance = RAG_results["distances"][0][0]

    print("TOP DISTANCE:", top_distance)

    if top_distance > 0.45:
        return (
            "This question seems outside my game analytics knowledge base. "
            "Please ask about retention, churn, funnel, A/B testing, "
            "LTV, monetization, or root cause analysis."
        )

    prompt = f"""
You are a professional game analytics assistant.

Answer the user's original question using the knowledge below.

Rules:
- Give practical investigation steps.
- Answer in 3-5 bullet points.
- Do not mention "retrieved knowledge", "context", or "RAG".
- Do not say "the provided knowledge".
- Do not say "please let me know".
- Prefer practical, game analytics language.
- Each bullet point must be under 30 words.

Knowledge:
{retrieved_docs}

User Question:
{question}

Final Answer:
"""

    tokenized_prompt = tokenizer(
        prompt,
        return_tensors="pt"
    ).to(device)

    output = model.generate(
        **tokenized_prompt,
        max_new_tokens=400,
        do_sample=False,
        eos_token_id=tokenizer.eos_token_id
    )

    input_length = tokenized_prompt["input_ids"].shape[1]
    new_tokens = output[0][input_length:]

    answer = tokenizer.decode(
        new_tokens,
        skip_special_tokens=True
    )

    bad_phrases = [
        "**Note:**",
        "Note:",
        "Please let me know",
        "The final answer",
        "This answer is based on",
        "provided knowledge",
        "retrieved knowledge",
        "RAG",
    ]

    for phrase in bad_phrases:
        if phrase in answer:
            answer = answer.split(phrase)[0]

    return answer.strip()


# In[14]:


# 3. INITIALIZE SESSION STATE (MEMORY)
# ---------------------------------------------------------
# This is our Short-Term Buffer. It survives Streamlit re-runs.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a game analytics assistant. You help users analyze retention, churn, cohort, funnel, A/B testing, LTV, and root cause problems."}
    ]


# In[15]:


# ---------------------------------------------------------
# 4. DRAW THE EXISTING CHAT HISTORY
# ---------------------------------------------------------
# We skip displaying the "system" prompt to the user
for msg in st.session_state.messages:
    if msg["role"] != "system":
        # Display the message using markdown format
        with st.chat_message(msg["role"]):
            st.write(msg["content"])


# In[16]:


# ---------------------------------------------------------
# 5. CHAT INPUT & GENERATION
# ---------------------------------------------------------
user_input = st.chat_input("Type your message here...")

if user_input:
    
    # A. Save user input to memory & display it
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)

    # B. Generate answer with RAG
    with st.spinner("Analyzing your question..."):
        answer = ask_rag(user_input)

    # C. Display answer
    with st.chat_message("assistant"):
        st.write(answer)

    # D. Save answer to memory
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )


# In[ ]:




