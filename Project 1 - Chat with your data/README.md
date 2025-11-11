# Azure Services Deployment

Azure AI Search Creation

Creation of the Azure AI Search service used in the chatbot application

OpenAI Service and Model Deployment

Deployment of both the GPT-4 model and the ADA model for embeddings in Azure OpenAI Studio

# Retrieval-Augmented Generation (RAG) Implementation

RAG Setup and Data Indexing

Configures RAG in Azure OpenAI Studio, linking the deployed GPT-4 model to Azure Blob Storage and AI Search, with indexing completion

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

Submission of Prompts File

Submits a file containing at least 5 developed prompts that were tested.

## Prompt 1: 

```
Compare Palantir's GAAP Net Income and Revenue for the quarter ended June 30, 2025, against the same quarter in 2024. State the percentage change (increase or decrease) for both metrics.
```

# Prompt 2:

```
Analyze the growth in U.S. Commercial Revenue from the quarter ended September 30, 2024, to the quarter ended September 30, 2025. According to the Management's Discussion section, what is the primary new initiative or product (e.g., AIP) driving this change in the latter filing?
```

# Prompt 3:

```
Examine the 'Cash and Cash Equivalents' balance as of the end of the second quarter for both 2024 and 2025. If there was a material change, what specific explanation or use of cash (e.g., share buybacks, acquisitions) does management provide in the latest 10-Q?
```

# Prompt 4:

```
What was the total dollar amount of Stock-Based Compensation (SBC) expense for the first nine months of 2024 compared to the first nine months of 2025? In which specific financial statement or note is the breakdown of SBC for Research & Development versus Sales & Marketing found?
```

# Prompt 5:

```
Based on the 'Risk Factors' section of the 2025 10-Q compared to the 2024 10-Q, is there any new or materially updated risk factor related to geopolitical tensions or foreign regulation? If so, summarize the key change in the company's language regarding that risk.
```
