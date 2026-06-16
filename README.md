# Game Analytics Assistant

# 游戏数据分析助手

## Project Overview

## 项目概述

This project is a Retrieval-Augmented Generation (RAG) chatbot designed to help game analysts, product managers, and game designers quickly obtain actionable insights related to player retention, churn, funnel analysis, A/B testing, monetization, and other game analytics topics.

本项目是一个基于检索增强生成（Retrieval-Augmented Generation, RAG）的智能聊天机器人，旨在帮助游戏数据分析师、产品经理和游戏设计师快速获取与玩家留存、流失分析、漏斗分析、A/B 测试、商业化以及其他游戏数据分析相关的可执行洞察。

Instead of relying solely on a language model's general knowledge, the chatbot retrieves relevant information from a curated Game Analytics Knowledge Base and generates responses grounded in domain-specific content.

与仅依赖大语言模型的通用知识不同，该聊天机器人会从专门构建的游戏数据分析知识库中检索相关内容，并基于领域知识生成回答，从而提高回答的准确性和专业性。

The system aims to simulate how a game analytics consultant would assist stakeholders in diagnosing business problems and recommending data-driven actions.

该系统旨在模拟游戏数据分析顾问的工作方式，帮助利益相关者诊断业务问题并提出数据驱动的决策建议。

---

## Key Features

## 核心功能

### 1. Domain-Specific Knowledge Base

### 1. 领域知识库构建

Built a custom Game Analytics Knowledge Base covering topics such as:

构建了专属的游戏数据分析知识库，涵盖以下主题：

* Retention Analysis（留存分析）
* Churn Analysis（流失分析）
* Funnel Analysis（漏斗分析）
* Cohort Analysis（用户群组分析）
* A/B Testing（A/B 测试）
* LTV (Lifetime Value)（用户生命周期价值）
* Monetization Metrics（商业化指标）
* Root Cause Analysis（根因分析）

The knowledge base is converted into vector embeddings and stored in ChromaDB for semantic retrieval.

知识库内容被转换为向量嵌入（Embeddings），并存储于 ChromaDB 中，以支持语义检索。

---

### 2. Query Rewriting

### 2. 查询重写（Query Rewriting）

Users often ask questions in natural language, which may not be optimal for retrieval.

用户通常使用自然语言提问，而这些问题未必适合直接进行向量检索。

To improve retrieval quality, a query rewriting module converts user questions into search-oriented analytics keywords before retrieval.

为了提升检索效果，系统在检索前会通过查询重写模块，将用户问题转换为更适合搜索的数据分析关键词。

**Example / 示例：**

**User Question / 用户问题：**

"My D1 retention dropped from 40% to 25%. What should I investigate?"

“我的 D1 留存率从 40% 下降到 25%，我应该检查哪些方面？”

**Rewritten Query / 重写后的查询：**

"D1 retention drop 40% 25% onboarding funnel churn cohort analysis tutorial completion"

“D1 留存下降 40% 25% 新手引导 漏斗分析 流失 用户群组分析 教程完成率”

This significantly improves retrieval accuracy.

该机制能够显著提升知识检索的准确率。

---

### 3. Retrieval-Augmented Generation (RAG)

### 3. 检索增强生成（RAG）

The system follows a RAG pipeline:

系统采用如下 RAG 工作流程：

User Question
用户问题

→ Query Rewriter
→ 查询重写

→ ChromaDB Retrieval
→ ChromaDB 检索

→ Relevance Filtering
→ 相关性过滤

→ Local LLM Generation
→ 本地大语言模型生成

→ Final Answer
→ 最终回答

This architecture allows the chatbot to generate responses grounded in domain knowledge rather than relying solely on model memorization.

该架构使模型能够基于知识库内容生成回答，而非仅依赖模型自身记忆，从而降低幻觉问题并提升专业性。

---

### 4. Relevance Filtering

### 4. 相关性过滤

To reduce hallucinations and prevent off-topic responses:

为了减少模型幻觉并避免偏离主题的回答，系统采用了多层过滤机制：

* Query relevance checks are applied before retrieval.
  检索前进行问题相关性判断。
* Similarity-based filtering is performed after retrieval.
  检索后进行相似度过滤。
* Non-game-analytics questions are rejected.
  非游戏数据分析相关问题将被拒绝回答。

**Example / 示例：**

**Question / 问题：**

"Do you know Sherlock Holmes?"

“你知道福尔摩斯吗？”

**Response / 回答：**

"This chatbot only supports game analytics questions."

“本聊天机器人仅支持游戏数据分析相关问题。”

---

### 5. Interactive Web Interface

### 5. 交互式网页界面

Built using Streamlit.

项目使用 Streamlit 构建轻量级 Web 应用界面。

Users can:

用户可以：

* Ask analytics questions
  提出游戏数据分析问题
* Receive retrieval-enhanced responses
  获取基于知识检索增强的回答
* Maintain short-term conversation history
  保留短期对话上下文
* Interact through a lightweight web interface
  通过简洁易用的网页界面进行交互

### 6. Dynamic Knowledge Base Expansion
### 6. 动态知识库扩展

Users can upload their own game analytics documents (.docx) directly through the web interface.

The system automatically:

- Extracts document content
- Splits text into semantic chunks using RecursiveCharacterTextSplitter
- Generates vector embeddings
- Stores them in ChromaDB

This enables users to continuously expand the knowledge base without modifying source code.

用户可以通过网页界面上传自己的游戏分析文档（.docx）。

系统将自动：

- 提取文档内容
- 使用 RecursiveCharacterTextSplitter 进行文本切分
- 生成向量嵌入
- 写入 ChromaDB

从而实现无需修改代码即可扩展知识库。

---

### System Architecture

User Question
↓
Query Rewriter
↓
Domain Filter
↓
ChromaDB Retrieval
↓
Relevance Filtering
↓
Qwen Local LLM
↓
Final Answer

Knowledge Expansion Pipeline

User Uploads DOCX
↓
Document Parsing
↓
RecursiveCharacterTextSplitter
↓
Embedding Generation
↓
ChromaDB Storage

## Technology Stack

## 技术栈

* Python
* Streamlit
* ChromaDB
* Sentence Transformers（BAAI/bge-small-en-v1.5）
* Hugging Face Transformers
* Qwen2.5-0.5B-Instruct

---

## Limitations

## 项目局限性

### Lightweight Local Model

### 轻量级本地模型

The current implementation uses:

当前版本使用：

**Qwen2.5-0.5B-Instruct**

The project intentionally uses Qwen2.5-0.5B-Instruct to enable fully local deployment on consumer-grade hardware.
本项目选用通义千问Qwen2.5-0.5B-Instruct模型，初衷是实现消费级硬件上的完整本地部署。

While this improves accessibility and reduces infrastructure costs, it introduces several limitations:
此举虽提升了方案易用性、降低基础设施成本，但也带来存在以下限制：

* Response quality is sometimes inconsistent.
  回答质量偶尔不够稳定。
* Instruction-following capability is limited.
  指令遵循能力有限。
* Responses may occasionally be verbose or incomplete.
  回答可能出现冗长或不完整的情况。
* Complex reasoning performance is constrained.
  复杂推理能力受到模型规模限制。

These limitations stem primarily from model capacity rather than the RAG architecture itself. Future versions can easily replace the local model with stronger open-source models or commercial APIs without changing the RAG architecture.

这些问题主要来源于模型参数规模，而非 RAG 架构本身。后续版本无需改动检索增强生成（RAG）整体架构，即可便捷替换本地模型，改用性能更强的开源模型或商用大模型接口。

---

### Knowledge Base Coverage

### 知识库覆盖范围

The chatbot can only answer questions covered by the current knowledge base.

当前系统只能回答知识库所覆盖范围内的问题。

Expanding the knowledge base would significantly improve answer quality and domain coverage.

未来扩展知识库内容将进一步提升回答质量和领域覆盖能力。

---

## Future Improvements

## 未来优化方向

### Stronger Language Models

### 更强大的语言模型

Potential upgrades include:

未来可升级至：

* Qwen2.5-1.5B
* Qwen2.5-3B
* GPT-4o API
* Claude API

These models would improve:

这些模型有望提升：

* Response quality
  回答质量
* Instruction following
  指令遵循能力
* Analytical reasoning
  分析推理能力
* Answer consistency
  回答一致性

---

### DSPy Optimization

### DSPy 优化

Future versions may integrate DSPy to optimize:

未来版本计划引入 DSPy，对以下模块进行自动优化：

* Query rewriting
  查询重写
* Prompt engineering
  提示词工程
* Response generation
  回答生成

through automated prompt optimization.

通过自动化提示词优化进一步提升整体性能。

---

### Agent-Based Architecture

### Agent 多智能体架构

Potential future architecture:

未来可采用如下多智能体架构：

User Question
用户问题

→ Domain Classifier
→ 领域分类器

→ Query Rewriter
→ 查询重写器

→ Retriever
→ 检索器

→ Analysis Agent
→ 分析智能体

→ Writing Agent
→ 写作智能体

→ Final Answer
→ 最终回答

This would allow more structured business recommendations and improved response quality.

该架构能够提供更结构化的业务分析建议，并进一步提升回答质量。

---

## Example Questions

## 示例问题

* What is retention?
  什么是留存率？
* My D1 retention dropped from 40% to 25%. What should I investigate?
  我的 D1 留存率从 40% 降到 25%，应该检查哪些指标？
* How should I design an A/B test?
  如何设计一个 A/B 测试？
* My paying users decreased this week. What metrics should I check?
  本周付费用户下降了，我应该关注哪些指标？
