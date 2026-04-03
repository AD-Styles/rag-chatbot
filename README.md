# 📚 Interactive Paper Review: End-to-End Conversational RAG Architecture
> **Implementing Context-Aware LLM Chatbot with LangChain, Vector Search, and Gradio Deployment**

![Python](https://img.shields.io/badge/Python-3.10-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.3.25-green.svg)
![Gradio](https://img.shields.io/badge/Gradio-UI-orange.svg)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-blue.svg)


## 📌 프로젝트 요약 (Project Overview)
본 프로젝트는 특정 도메인 문서(학술 논문)를 기반으로 답변하는 **RAG(Retrieval-Augmented Generation) 챗봇 파이프라인의 전체 구축 및 배포 프로세스**를 입증하는 엔지니어링 포트폴리오입니다. LangChain을 활용한 문서의 로딩, 분할, 벡터 임베딩 처리부터, 사용자의 대화 맥락을 기억하는 메모리(Memory) 시스템 연동까지 아키텍처 전반을 직접 설계했습니다. 최종적으로 Gradio UI를 결합하여 Hugging Face Spaces에 배포함으로써 기술 검증을 넘어 실제 사용자 대상의 웹 서비스 운영 경험을 기록했습니다.


## 🎯 핵심 목표 (Motivation)
| 구분 | 세부 내용 |
| :--- | :--- |
| **RAG 파이프라인 구축** | 범용 LLM의 한계(지식 부족, 환각 현상)를 극복하기 위해 Chroma 벡터 DB와 연결하여 외부 지식을 동적으로 검색 및 주입하는 구조 설계. |
| **대화 맥락 유지 (Memory)** | 독립적인 단일 질의응답을 넘어, `RunnableWithMessageHistory`를 통해 세션별 대화 기록을 관리하여 문맥을 이해하는 다턴(Multi-turn) 대화 구현. |
| **엔드투엔드(E2E) 배포** | 백엔드 로직에 Gradio 기반의 직관적인 사용자 인터페이스를 입히고, Hugging Face 플랫폼에 호스팅하여 서비스 가용성 확보. |


## 📂 프로젝트 구조 (Project Structure)
```text
📂 rag-chatbot
├── 📄 app.py                            # Gradio UI 및 RAG 파이프라인 통합 실행 메인 서버
├── 📄 requirements.txt                  # Hugging Face 배포를 위한 의존성 패키지 명세서
├── 📄 Maximizing Muscle Hypertrophy.pdf # RAG 지식 검색 기반 원본 문서 (Vector DB 색인용)
└── 📄 README.md                         
