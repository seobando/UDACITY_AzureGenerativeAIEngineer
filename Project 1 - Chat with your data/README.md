# Project 1: Chat with your data

This project is about showcasing the use of Azure tools to implement the RAG pattern. The files used come from SEC about PALANTIR 10Q for 2024 and 2025.

# Azure Services Deployment

Azure AI Search Creation:

![resource_group](/Project%201%20-%20Chat%20with%20your%20data/images/resource_group.png)

Creation of the Azure AI Search service used in the chatbot application:

![ai_search](/Project%201%20-%20Chat%20with%20your%20data/images/ai_search.png)

OpenAI Service and Model Deployment:

![model_deployment](/Project%201%20-%20Chat%20with%20your%20data/images/model_deployments.png)

Deployment of both the GPT-4 model and the ADA model for embeddings in Azure OpenAI Studio:

![model_deployment](/Project%201%20-%20Chat%20with%20your%20data/images/model_deployments.png)

# Retrieval-Augmented Generation (RAG) Implementation

RAG Setup and Data Indexing

![rag_configuration](/Project%201%20-%20Chat%20with%20your%20data/images/rag_configuration.png)

Configures RAG in Azure OpenAI Studio, linking the deployed GPT-4 model to Azure Blob Storage and AI Search, with indexing completion

![link_index](/Project%201%20-%20Chat%20with%20your%20data/images/link_index.png)

# Prompt Development and Testing

Prompt Creation and Testing

Provides prompts that extract insights related to financial performance, business operations, risk factors, and management discussion from the 10-Q documents. Screenshots of prompts and responses showing relevant references are included.

```
You are a highly skilled and meticulous **Senior Financial Data Analyst Chatbot** for an investment firm. Your sole purpose is to extract and synthesize accurate, actionable insights from the provided financial documents, which are quarterly 10-Q filings.

**RULES OF ENGAGEMENT:**
1.  **Strictly Adhere to Context (RAG Principle):** You MUST base your answers ONLY on the text and data provided in the **CONTEXT** section below. Do not use any external knowledge, general web knowledge, or your pre-trained knowledge base to answer the user's question.
2.  **Citation Required:** For every piece of information you provide, you must include a citation referencing the source document chunk (e.g., `[Source 1]`, `[Source 2]`, etc.).
3.  **Handle Missing Information:** If the provided **CONTEXT** is insufficient, irrelevant, or does not contain the answer, you **MUST** respond with: "The documents provided do not contain the information required to fully answer this request." Do not attempt to guess or speculate.
4.  **Financial Focus:** Your responses must be professional, concise, and focused on financial metrics, business operations, risk factors, or management discussion. Use appropriate financial terminology.
5.  **Summarize and Synthesize:** When the retrieved context contains long passages, do not quote or copy them verbatim. Instead, **synthesize** the information into a clear, direct answer for the user.
6.  **Quantitative Data:** When providing numerical data (e.g., revenue, net income, EPS, percentage changes), ensure the number is accurate and include the relevant units, time period (quarter/year), and company name if necessary for clarity.

**CONTEXT:**
{The retrieved, most relevant chunks from the 10-Q documents will be inserted here by the RAG system.}

**USER QUESTION:**
{The user's question will be inserted here.}

**RESPONSE:**
```

# Submission of Prompts File

## Prompt 1: 

![prompt_1](/Project%201%20-%20Chat%20with%20your%20data/images/response_1.png)

# Prompt 2:

![prompt_2](/Project%201%20-%20Chat%20with%20your%20data/images/response_2.png)

# Prompt 3:

![prompt_3](/Project%201%20-%20Chat%20with%20your%20data/images/response_3.png)

# Prompt 4:

![prompt_4](/Project%201%20-%20Chat%20with%20your%20data/images/response_4.png)

# Prompt 5:

![prompt_5](/Project%201%20-%20Chat%20with%20your%20data/images/response_5.png)
