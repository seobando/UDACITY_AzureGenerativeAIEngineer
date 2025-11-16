#  AI Copilot Development

## 🚀 Project Overview:

This project challenges the developer to act as an AI specialist and build a functional, industry-tailored **AI Copilot**.

The primary goal is to design, implement, and deploy a chat-based application capable of providing **accurate, real-time responses** by retrieving relevant information from an indexed dataset. This copilot is intended to significantly **enhance the user/customer experience** for a chosen company.

### 🎯 Specific Track

This project focuses on the **Outlander Gear Co. (Product/Retail)** track:

* **Goal:** Build a **Product Data Copilot**.
* **Function:** Provide instant access to product details, pricing, and comparisons to enhance the customer shopping experience for a pioneer in high-quality outdoor equipment.

## ✨ Project Rubric

1. Project and Data Configuration and Preparation

- AI model is deployed within the project: Screenshots or logs show the successful deployment of a base model.

- Upload and management of data in AI Studio: The copilot responds using data grounded from a data source, and evaluations are created against the data source.

- AI Search index using the uploaded data: The copilot application uses an AI Search Service evidenced by functionality or screenshots

2. Copilot App Development

- Implementation of Prompt Flow for the custom AI Copilot: Screenshots of the Prompt Flow of the copilot.

- The Copilot is tested with relevant questions: Screenshots show accurate responses to evaluation questions.

3. Evaluation of the Copilot

- The automated evaluation of the copilot is performed with a structured dataset: JSONL or CSV evaluation dataset provided and used in AI Studio for evaluation. Metrics and results from the automated evaluation are included in the submission.

- Manual prompt evaluation is conducted: Evidence/screenshots of manually added questions and responses with feedback provided.

## 🔧 Set Up

### Project Structure

The project is organized as follows:

```
Project 2 - Custom Copilot/
├── outlander-copilot/          # Main Prompt Flow application
│   ├── flow.dag.yaml          # Flow definition (nodes, inputs, outputs)
│   ├── chat.jinja2            # Chat prompt template
│   ├── tools/                  # Custom Python tools
│   │   ├── chat.py            # Chat tool (Azure OpenAI integration)
│   │   └── retrieve.py        # Retrieval tool (Azure AI Search)
│   ├── azure_openai.yaml      # Azure OpenAI connection config
│   ├── openai.yaml            # OpenAI connection config
│   └── azure_ai_search.yaml   # Azure AI Search connection config
├── data/                       # Data files for indexing
├── evaluation/                 # Evaluation datasets and results
│   ├── llm_evaluation_qa.json # Evaluation questions
│   └── llm_evaluation_qa.md   # Evaluation documentation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### Prerequisites

Before setting up the project, ensure you have:

- **Python 3.9+** installed
- **Azure OpenAI Service** deployed with a model (e.g., `gpt-4o`)
- **Azure AI Search** service with an index created
- **Azure credentials** (API keys and endpoints)

### Installation

1. **Install Python dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Verify Prompt Flow installation:**

   ```bash
   pf --version
   ```

### Configuration

#### 1. Azure OpenAI Connection

Create a connection to Azure OpenAI using one of the following methods:

**Option A: Using YAML file with command-line overrides (Recommended)**

```bash
cd outlander-copilot
pf connection create --file azure_openai.yaml \
  --set api_key=<your_api_key> \
  --set api_base=<your_api_base> \
  --name open_ai_connection
```

**Option B: Using environment variables**

The `chat.py` tool automatically loads credentials from a `.env` file. Create a `.env` file in the `outlander-copilot` directory:

```env
AZURE_OPENAI_API_KEY=your-api-key
AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o
```

#### 2. Azure AI Search Configuration

Create a `.env` file in the `outlander-copilot` directory (or add to existing one) with:

```env
AZURE_SEARCH_ENDPOINT=https://your-service-name.search.windows.net
AZURE_SEARCH_API_KEY=your-api-key
```

Alternatively, you can use:
- `AZURE_SEARCH_SERVICE_NAME` (instead of `AZURE_SEARCH_ENDPOINT`)

The retrieve tool automatically loads these credentials using `python-dotenv`.

#### 3. Verify Connections

Check that your connections are properly configured:

```bash
pf connection show --name open_ai_connection
```

### Running the Prompt Flow

#### Interactive Chat Session

To start an interactive chat session with the copilot:

```bash
cd outlander-copilot
pf flow test --flow . --interactive
```

**What to expect:**
- A welcome message will appear in the terminal
- Type your question and press **Enter** to send
- The bot will respond using the RAG flow (retrieval + chat)
- Chat history is maintained across multiple turns
- Press **Ctrl+C** to quit

**Example session:**

```
=========================================
Welcome to chat flow, <your-flow-name>.
Press Enter to send your message.
You can quit with ctrl+C.
=========================================
User: What is the price of the TrailMaster X4 Tent?
Bot: [Response from your flow with retrieved context]
```

#### Verbose Mode

To see detailed output from each node in the flow:

```bash
pf flow test --flow . --interactive --verbose
```

This will display:
- **User input** (in green)
- **Bot output** (in gold)
- **Node outputs** (in cyan) - shows intermediate results from retrieve and chat nodes
- **Flow script output** (in blue)

#### Single Test Run

To test the flow with a single question (non-interactive):

```bash
pf flow test --flow . \
  --inputs question="What is the price of the TrailMaster X4 Tent?"
```

### Flow Architecture

The copilot uses a **Retrieval-Augmented Generation (RAG)** pattern:

1. **Retrieve Node**: Queries Azure AI Search to find relevant product information
2. **Chat Node**: Uses Azure OpenAI to generate a response based on:
   - Retrieved context from AI Search
   - User's question
   - Chat history (for conversational context)

The flow is defined in `flow.dag.yaml` and uses:
- **Chat Input**: User questions (`question` input)
- **Chat History**: Maintains conversation context (`chat_history` input)
- **Chat Output**: Generated responses (`answer` output)

For more details on the flow implementation, see `outlander-copilot/README.md`.


4. Deployment

- The copilot is deployed successfully and verified: Screenshots of the deployment confirmation with endpoint information included.

# Resources

[How to integrate Prompt Flow in VSC](https://www.youtube.com/watch?v=M6gXchnxHik&t=472s)
[Full Prompt Flow series](https://www.youtube.com/watch?v=K50ZhIIKkV4&list=PLyqwquIuSMZqZHRGm1m-MHsH00jQzGT-D&index=1)