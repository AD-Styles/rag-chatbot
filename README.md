# 📚 Implementing Context-Aware LLM Chatbot with LangChain, Vector Search, and Gradio Deployment

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-blue.svg)

---

## 📌 프로젝트 요약 (Project Overview)
본 프로젝트는 특정 도메인 문서(학술 논문)를 기반으로 답변하는 **RAG(Retrieval-Augmented Generation) 챗봇 파이프라인의 구축 및 배포 프로세스**를 입증하는 엔지니어링 포트폴리오입니다. LangChain을 활용한 문서의 로딩, 분할, 벡터 임베딩 처리부터, 사용자의 대화 맥락을 기억하는 메모리(Memory) 시스템 연동까지 아키텍처 전반을 설계했습니다. 최종적으로 Gradio UI를 결합하여 Hugging Face Spaces에 배포함으로써 기술 검증을 넘어 실제 사용자 대상의 웹 서비스 운영 경험을 기록했습니다.

---

## 🎯 핵심 목표 (Motivation)
| 구분 | 세부 내용 |
| :--- | :--- |
| **RAG 파이프라인 구축** | 범용 LLM의 한계(지식 부족, 환각 현상)를 극복하기 위해 Chroma 벡터 DB와 연결하여 외부 지식을 동적으로 검색 및 주입하는 구조 설계. |
| **대화 맥락 유지 (Memory)** | 독립적인 단일 질의응답을 넘어, `RunnableWithMessageHistory`를 통해 세션별 대화 기록을 관리하여 문맥을 이해하는 다턴(Multi-turn) 대화 구현. |
| **엔드투엔드(E2E) 배포** | 백엔드 로직에 Gradio 기반의 직관적인 사용자 인터페이스를 입히고, Hugging Face 플랫폼에 호스팅하여 서비스 가용성 확보. |

---

## 📂 프로젝트 구조 (Project Structure)
```text
📂 rag-chatbot
├── 📄 Maximizing Muscle Hypertrophy.pdf # RAG 지식 검색 기반 원본 문서 (Vector DB 색인용)
└── 📄 README.md
├── 📄 app.py                            # Gradio UI 및 RAG 파이프라인 통합 실행 메인 서버
├── 📄 requirements.txt                  # Hugging Face 배포를 위한 의존성 패키지 명세서                         
```

---

## 🛠️ 주요 알고리즘 및 기술적 구현 (Technical Implementation)

### 1. Document Processing & Vectorization
초거대 언어 모델이 처리할 수 없는 방대한 문서를 효율적으로 검색할 수 있도록 데이터를 전처리하고 색인화했습니다.

| 구현 단계 | 활용 모듈 및 파라미터 | 기술적 포인트 |
| :--- | :--- | :--- |
| Data Loading | PyPDFLoader | PDF 문서를 페이지 단위로 추출하여 Document 객체로 변환 |
| Text Splitting | RecursiveCharacterTextSplitter | chunk_size=1000, chunk_overlap=200 설정을 통해 문맥 유실 최소화 |
| Embedding & Storage | GoogleGenerativeAIEmbeddings, Chroma | gemini-embedding-001 모델로 텍스트를 벡터화하고 Chroma DB에 색인 저장 |

---

### 2. Context-Aware Retrieval & Generation
사용자의 질문에 대해 가장 연관성 높은 문서를 찾아 답변을 생성하는 핵심 체인을 구성했습니다.

| 프로세스 순서 | 활용 모듈 | 수행 내용 |
| :--- | :--- | :--- |
| 1. Retrieval | retriever | 벡터 유사도 기반으로 질문과 관련된 상위 문서 조각(Chunk) 추출 |
| 2. Prompting | ChatPromptTemplate | System Prompt, Context, Chat History, User Input을 결합한 동적 프롬프트 설계 |
| 3. Generation | create_retrieval_chain | 검색된 문서와 질문을 Gemini 2.0 Flash 모델에 전달하여 최종 답변 생성 |

---

### 3. Conversational Memory Injection
LCEL(LangChain Expression Language)을 활용하여 체인에 대화 상태 관리 기능을 주입했습니다.

| 메모리 관리 기법 | 활용 객체 | 비고 |
| :--- | :--- | :--- |
| Session Tracking | get_session_history, session_id | 사용자별로 InMemoryChatMessageHistory를 독립적으로 할당하여 대화 격리 |
| History Integration | MessagesPlaceholder | 프롬프트 내 대화 기록이 삽입될 위치를 지정하여 문맥 유지 |

---

## 🚀 트러블슈팅 및 성능 최적화 (Troubleshooting & Optimization)

| 분석 항목 | 세부 해결 과정 및 전략 |
| :--- | :--- |
| 환각(Hallucination) 억제 | System Prompt에 "문서에 없는 내용은 모른다고 답하세요"라는 제약 조건을 명시하여 모델의 추론 범위를 문서 내로 한정 |
| 청크 분할 문맥 유지 | chunk_overlap을 적용하여 인접한 조각 간의 정보 연속성 보존 |
| UI 이벤트 안정화 | Gradio의 submit과 click 이벤트를 단일 콜백 함수로 통합하여 다양한 사용자 입력 패턴에서도 동일한 응답 로직 보장 |

---

## 📊 학습 개념의 직관적 해석 (Analogies)

| 핵심 개념 | 비유 (Analogy) | 기술적 의미 설명 |
| :--- | :--- | :--- |
| RAG (검색 증강 생성) | 오픈북 시험 | AI가 사전 지식에만 의존하지 않고, 문서를 참고하여 정답을 도출하는 기법 |
| Vector Embedding | 도서관 십진분류표 | 단어의 의미를 좌표로 변환하여 의미 기반 검색 수행 |
| Text Splitter (Overlap) | 포스트잇 겹쳐 붙이기 | 일부를 겹치게 잘라 문맥을 보존하는 방식 |

---

## 🤖 최종 QA Chatbot Huggingface
1. https://huggingface.co/spaces/AD-Styles/RAG_Chatbot
2. https://huggingface.co/spaces/AD-Styles/RAG_Chatbot_Upgrade

---

## 💡 회고록 (Retrospective)
이번 실습을 통해서 단순히 API를 호출하는 단계를 넘어 로더, 분할기, 벡터 DB, 메모리 모듈을 LCEL 파이프라인으로 유기적으로 연결하며 전체적인 데이터 흐름을 제어하는 설계 역량을 길렀습니다. 또한 단발성 질의응답 시스템에 Memory 모듈을 도입하고 Gradio UI를 통해 시각화함으로써, '기술'을 실제 사용자가 편리하게 사용할 수 있는 '서비스'의 형태로 구현하는 과정을 경험했습니다. RAG 시스템의 성능은 모델의 파라미터만큼이나 '양질의 청킹 전략'과 '정교한 프롬프트 가드레일'에 달려 있음을 체감했습니다. 이는 향후 실무 솔루션 개발에 있어 중요한 지표가 될 것이라고 생각합니다.
