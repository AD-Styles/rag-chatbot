import os
import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# -------------------------------------------------------------------
# 1. RAG 챗봇 세팅
# -------------------------------------------------------------------

# API 키 설정 (Hugging Face Spaces Secrets 연동용)
if "GOOGLE_API_KEY" not in os.environ:
    raise ValueError("GOOGLE_API_KEY 환경 변수가 설정되지 않았습니다.")

# LLM
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0)

# 문서 로딩 & 분할
loader = PyPDFLoader("Maximizing Muscle Hypertrophy.pdf")
pages = loader.load_and_split()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(pages)

# 벡터 저장소
embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)
retriever = vectorstore.as_retriever()

# RAG Chain with Memory
store = {}
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

qa_prompt = ChatPromptTemplate.from_messages([
    ("system", """논문 리뷰 전문가입니다. 제공된 문서를 바탕으로 한국어로 답변하세요.
문서에 없는 내용은 모른다고 답하세요.

{context}"""),
    MessagesPlaceholder("chat_history"),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
)

# -------------------------------------------------------------------
# 2. 챗봇 UI 구조 및 실행 로직
# -------------------------------------------------------------------

with gr.Blocks() as demo:
    gr.Markdown("## 📄 논문 리뷰 챗봇 (Maximizing Muscle Hypertrophy)")

    chatbot = gr.Chatbot(label="대화창", height=400)

    with gr.Row():
        inp = gr.Textbox(
            placeholder="논문에 대해 질문해보세요...",
            scale=4,
            container=False
        )
        btn = gr.Button("전송", variant="primary", scale=1)

    btn_clear = gr.Button("대화 초기화")

    def respond(message, history):
        config = {"configurable": {"session_id": "hf_deploy_session"}}
        
        response = conversational_rag_chain.invoke(
            {"input": message},
            config=config,
        )
        bot_reply = response["answer"]
        history.append([message, bot_reply])
        
        return "", history

    # 버튼 및 텍스트박스 이벤트 연결
    btn.click(fn=respond, inputs=[inp, chatbot], outputs=[inp, chatbot])
    inp.submit(fn=respond, inputs=[inp, chatbot], outputs=[inp, chatbot])
    btn_clear.click(fn=lambda: ([], ""), outputs=[chatbot, inp])

if __name__ == "__main__":
    demo.launch()
