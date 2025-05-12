# Multi-Agent Swarm System for Italian Public Administration Data Analysis

This repository hosts a fully functional, production-grade multi-agent system built upon OpenAI's Swarm framework, designed specifically for the semantic understanding, exploration, and visualization of structured CSV datasets provided by the Italian Public Administration. It represents a powerful implementation of hybrid intelligence where advanced LLM reasoning is combined with task-specific modularity, creating a system that is capable of interpreting ambiguous, multi-step, and semantically rich natural language queries without requiring any manual preprocessing or hardcoded filters. The system is intended as a reference architecture for applied Retrieval-Augmented Generation (RAG) strategies, designed with professional data exploration and governance in mind.

## Purpose of the Project
The core idea behind this project is to empower Italian analysts, policymakers, journalists, and technically-savvy citizens with a tool that allows them to interact naturally with data published by the Italian government, including but not limited to salary distributions, income segmentation, digital access methods, and commuting patterns of civil servants that have access to the NoiPa Portal. All analyses are done in real-time through a Swarm of expert agents, each with a precise functional responsibility, acting in coordination to extract meaningful insights. The user simply asks a question in plain Italian (or English), such as "Show me the distribution of digital accesses by region for women under 40" or "What is the average salary of male workers in Milan in health administration", and the system automatically understands which dataset to query, how to filter it, what to compute, and whether a chart is required.

## System Architecture
The system is built around a Swarm of modular agents, each responsible for a distinct phase of the interpretation-execution pipeline. It leverages Swarm OpenAI , OpenAI GPT-4.1, LlamaIndex for deep semantic schema parsing, and Streamlit for visualization. The architecture is designed to minimize hardcoded logic, instead relying on nowadays extreme powerful natural language understanding from LLMs that are guided by structured prompt templates and shared metadata.

### Agent Composition:

- **Conversational Agent**: Parses the user's natural language request, identifies the intent, and produces a fully structured semantic prompt that includes the type of operation (e.g., sum, mean, distribution), the dataset involved, the exact columns needed, and any necessary filters. It also identifies multi-dataset scenarios and proposes valid merges only if columns are semantically compatible.

- **Prompt Engine**: Translates the structured prompt into a well-formed, precise natural instruction that is used by the downstream Data Agent. It also decides whether a chart is required based on lexical clues and prompts the Visualization Agent accordingly.

- **Data Agent**: Generates executable Python code using only `pandas`. The code is always robust, minimal, safe, and includes automatic data cleaning, coercion of column types, merging logic if needed, and filtering based on uppercased, trimmed textual inputs. It never generates visualizations directly.

- **Visualization Agent**: Receives the output of the Data Agent along with the user prompt and the code that generated the data. It creates elegant, professional-quality plots using matplotlib or seaborn, always saving the figure to a PNG image. It handles missing or invalid data gracefully.

- **Explanation Agent**: Provides a final natural language explanation of the result, fully aware of whether a visualization was generated. It adapts its tone and structure depending on whether the result is a number, a list, a distribution, or a complex dataframe.

## Semantic Data Foundation
The system supports four highly structured and representative datasets from the Italian Public Administration. Each dataset has been semantically indexed using LlamaIndex. This indexing step ensures that column descriptions, value types, filters, and merge compatibility rules are fully mapped and retrievable at runtime. The datasets include:

1. **Salaries**: Aggregated data on salary payments, including the method of payment, administrative office, sex and age of recipients, and municipality of the working site.

2. **Income Segments**: Data on civil servants distributed by income brackets, region of residence, and tax rates. Age and gender breakdowns are also included.

3. **Digital Access**: Records of how public employees access online government services (SPID, CIE, etc.), filtered by region of residence, administration, and demographic info.

4. **Commuting**: Data about work-site proximity, administrative unit, and estimated minimum and maximum distance in kilometers for employees who do not live in the same municipality as their workplace.

All of these datasets are designed to be compatible with aggregation operations, regional breakdowns, and administrative filters. The agents dynamically determine which of the datasets (or combinations) are relevant based on user queries, allowing for powerful reasoning and zero manual SQL or Python coding.

## Key Features
- Semantic understanding of complex user input
- Fully modular agentic pipeline with Swarm
- Integration of LlamaIndex for smart schema mapping
- Chart generation delegated to a dedicated agent with type detection
- Streamlit-based interactive chat UI
- Robust Python code generation with defensive programming practices
- Clear, localized, and intelligent explanations of any result
- Designed for multi-step, follow-up, and elliptical queries
- Support for chart downloads and explanations in natural language

## How to Use

1. **Clone the repository**
```bash
git clone https://github.com/esimonelli/TRIPLE3
cd multiagent-swarm-pa
```

2. **Set up your environment**
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. **Run the interface**
```bash
streamlit run streamlit_app.py
```

4. **Ask your questions** using natural language, and explore the visual and textual results in real-time.

## Final Remarks
This project is intended as a real-world demonstration of how multi-agent coordination, when guided by semantically aware LLM prompting and lightweight orchestration, can deliver powerful, interpretable, and scalable data interaction systems. While it is tightly tuned for the Italian PA use case, the architecture can be ported to any domain with well-structured tabular data. Future extensions may include fine-tuned embeddings for domain-specific knowledge, support for multilingual queries, and external APIs to serve web or mobile clients.

Every agent in this system acts autonomously but within a clearly defined communicative contract, producing a collaborative workflow that respects the principle of minimal redundancy and maximum semantic leverage. This is not only a demonstration of Swarm's practical applicability but also a case study in the next evolution of user-data interaction.

We hope this repository helps researchers, developers, and data practitioners to better understand and explore what is possible when foundation models are used as reasoning agents across an entire analytical stack.
