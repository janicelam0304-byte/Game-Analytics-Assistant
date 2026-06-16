# Product Requirement Document (PRD)

# 产品需求文档（PRD）

# Game Analytics Assistant

# 游戏数据分析助手

Game-Analytics-RAG/
│
├── game_analysis_rag_chatbot.py
├── README.md
├── PRD.md
├── requirements.txt
├── Game_Analytics_Knowledge_Base.docx
└── game_analytics_db/
---

# 1. Product Background

# 1. 产品背景

Game analysts and product managers frequently rely on analytical frameworks such as retention analysis, funnel analysis, cohort analysis, A/B testing, and LTV evaluation.

游戏数据分析师和产品经理在日常工作中经常依赖留存分析（Retention Analysis）、漏斗分析（Funnel Analysis）、队列分析（Cohort Analysis）、A/B 测试以及用户生命周期价值（LTV）评估等分析框架。

However, knowledge is often scattered across documentation, internal training materials, and past project reports.

然而，这些知识通常分散在产品文档、内部培训资料以及历史项目报告中。

Junior analysts spend significant time searching for relevant frameworks and may lack experience in diagnosing business problems systematically.

初级分析师往往需要花费大量时间查找相关分析框架，同时缺乏系统化诊断业务问题的经验。

This project aims to build an AI-powered Game Analytics Assistant that provides instant, structured, and actionable recommendations based on a curated analytics knowledge base.

本项目旨在构建一个基于 AI 的游戏数据分析助手，通过精选的分析知识库，为用户提供即时、结构化且可执行的分析建议。

---

# 2. Product Goals

# 2. 产品目标

The product aims to:

本产品旨在实现以下目标：

* Reduce time spent searching analytics documentation
  减少查找分析文档所需时间

* Improve consistency of analytical recommendations
  提高分析建议的一致性和标准化程度

* Assist junior analysts in diagnosing business problems
  帮助初级分析师快速定位和诊断业务问题

* Provide framework-driven investigation guidance
  提供基于分析框架的调查与排查指导

* Enable rapid access to game analytics knowledge
  实现游戏数据分析知识的快速获取

---

# 3. Target Users

# 3. 目标用户

### Primary Users / 核心用户

* Game Data Analysts（游戏数据分析师）
* Product Managers（产品经理）
* Game Designers（游戏策划）

### Secondary Users / 次要用户

* Indie Developers（独立游戏开发者）
* Live Operations Teams（游戏运营团队）
* Students Learning Game Analytics（学习游戏数据分析的学生）

---

# 4. User Pain Points

# 4. 用户痛点

### Pain Point 1 / 痛点 1

Knowledge is scattered across multiple documents and sources.

分析知识分散在多个文档和信息来源中，检索效率较低。

### Pain Point 2 / 痛点 2

Junior analysts may not know which framework to use when diagnosing retention or monetization issues.

初级分析师在分析留存或变现问题时，往往不知道应采用哪种分析框架。

### Pain Point 3 / 痛点 3

Repeated questions consume significant analyst time.

大量重复性问题会占用分析师的时间和精力。

### Pain Point 4 / 痛点 4

Business stakeholders require fast recommendations without waiting for expert consultation.

业务相关方希望快速获得分析建议，而无需等待专家支持。

---

# 5. Proposed Solution

# 5. 解决方案

Build a RAG-based Game Analytics Assistant.

构建一个基于 RAG（Retrieval-Augmented Generation，检索增强生成）的游戏数据分析助手。

### Core Capabilities / 核心能力

* Retention Analysis（留存分析）
* Churn Analysis（流失分析）
* Funnel Analysis（漏斗分析）
* Cohort Analysis（队列分析）
* A/B Testing Guidance（A/B 测试指导）
* Monetization Analysis（变现分析）
* Root Cause Investigation（根因分析）

The assistant retrieves relevant knowledge from a domain-specific knowledge base and generates actionable recommendations.

系统将从游戏数据分析领域知识库中检索相关内容，并生成具有可执行性的分析建议。

---

# 6. System Architecture

# 6. 系统架构

### Query Processing Flow / 问答处理流程

User Question（用户问题）
↓
Query Rewriter（问题重写模块）
↓
Domain Filter（领域过滤模块）
↓
Vector Retrieval - ChromaDB（向量检索）
↓
Relevance Filtering（相关性过滤）
↓
Local LLM（本地大语言模型）
↓
Answer Generation（答案生成）

### Knowledge Expansion Pipeline / 知识库扩展流程

User Uploads DOCX（用户上传 DOCX 文件）
↓
Document Parsing（文档解析）
↓
RecursiveCharacterTextSplitter（文本切分）
↓
Embedding Generation（向量嵌入生成）
↓
ChromaDB Storage（存储至 ChromaDB）

---

# 7. Key Features

# 7. 核心功能

### Feature 1 / 功能 1

Domain-specific analytics knowledge base

游戏数据分析领域专属知识库

### Feature 2 / 功能 2

Query rewriting to improve retrieval quality

通过问题重写提升检索质量

### Feature 3 / 功能 3

Semantic retrieval using ChromaDB

基于 ChromaDB 的语义检索能力

### Feature 4 / 功能 4

Domain filtering for out-of-scope questions

针对非游戏分析领域问题进行过滤

### Feature 5 / 功能 5

Interactive Streamlit chat interface

基于 Streamlit 的交互式聊天界面

### Feature 6 / 功能 6

Dynamic knowledge base expansion through document upload

支持通过文档上传动态扩展知识库

### Feature 7 / 功能 7

Upload Progress Feedback with Spinner

上传文档并构建知识库时，通过 Streamlit Spinner 提供实时加载提示，向用户展示系统正在执行文档解析、文本切分、向量生成和数据库写入等操作，减少因等待过程不可见而产生的不确定感，提升整体用户体验。

通过加载状态反馈机制，用户能够明确了解系统正在处理任务，从而降低等待焦虑并提高功能可用性。

---

# 8. Success Metrics

# 8. 成功指标

### Retrieval Metrics / 检索指标

* Retrieval relevance（检索相关性）
* Retrieval precision（检索准确率）

### User Metrics / 用户指标

* User satisfaction（用户满意度）
* Response usefulness（回答实用性）

### System Metrics / 系统指标

* Response latency（响应延迟）
* Successful query completion rate（问题成功解决率）

---

# 9. Current Limitations

# 9. 当前限制

The current implementation uses Qwen2.5-0.5B-Instruct due to local hardware constraints.

由于本地硬件资源限制，当前版本采用 Qwen2.5-0.5B-Instruct 模型。

Known limitations include:

当前已知限制包括：

* Reduced reasoning capability
  推理能力有限

* Less consistent instruction following
  指令遵循能力不够稳定

* Occasional incomplete responses
  偶尔出现回答不完整的情况

* Limited complex analytical reasoning
  对复杂分析场景的推理能力较弱

These limitations are primarily model-related rather than architecture-related.

上述问题主要来源于模型规模限制，而非系统架构设计问题。

---

# 10. Future Roadmap

# 10. 未来规划

### V1

* Basic RAG Assistant（基础 RAG 助手）
* Query Rewriter（问题重写模块）
* Domain Filter（领域过滤模块）
* ChromaDB Retrieval（ChromaDB 检索能力）

### V1.1

* User document upload（用户文档上传）
* Dynamic knowledge base expansion（动态知识库扩展）
* Upload processing spinner and progress feedback（上传处理 Spinner 与加载状态反馈）
* LangChain RecursiveCharacterTextSplitter with chunk overlap（基于 LangChain 的文本切分与 Chunk Overlap 上下文保留机制）

### V2

* PDF support（PDF 文件支持）
* OCR document processing（OCR 文档识别）

### V3

* DSPy optimization（DSPy 优化）
* Multi-query retrieval（多查询检索）

### V4

* Agent-based architecture（Agent 架构升级）
* Analysis Agent（分析 Agent）
* Writing Agent（写作 Agent）

### V5

* SQL generation（SQL 自动生成）
* Dashboard interpretation（数据看板解读）
* Automated business insights（自动化业务洞察）
