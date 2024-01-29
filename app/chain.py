from yandex_chain import YandexEmbeddings, YandexLLM
from langchain.vectorstores import Chroma
from langchain.document_loaders import WebBaseLoader
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough

loader = WebBaseLoader(
    web_paths=("https://cloud.yandex.ru/ru/docs/datasphere/concepts/",
               "https://cloud.yandex.ru/ru/docs/datasphere/concepts/resource-model")
)
docs = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(docs)
vectorstore = Chroma.from_documents(documents=splits, embedding=YandexEmbeddings(
                                      folder_id="<id_каталога>", 
                                      api_key="<API-ключ>")
                                    )
retriever = vectorstore.as_retriever()

# Create YandexLLM model
model = YandexLLM(folder_id="<id_каталога>", 
                  api_key="<API-ключ>")


template = """Используй текст ниже, чтобы отвечать на вопросы в конце. Если ты не знаешь ответ,\
      то не придумывай и ответь, что не знаешь. Используй максимум три предложения для ответа.
      {context}
      Вопрос: {question}
      Ответ:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

qa_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | QA_CHAIN_PROMPT
    | model
)