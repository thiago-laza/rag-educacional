import os
import csv
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai
from typing import List, Tuple

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
    DirectoryLoader,
)
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- 1. Configurações e Variáveis de Ambiente ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente 'GEMINI_API_KEY' não está definida.")

genai.configure(api_key=GEMINI_API_KEY)

# Caminho para o DIRETÓRIO de contexto
CONTEXT_DIR_PATH = "../documentos"
LOGS_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOGS_DIR, "interacoes_chat_mat.csv")

# Configurações do modelo Gemini
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest"
GENERATION_CONFIG = genai.types.GenerationConfig(
    max_output_tokens=400,
    temperature=0.1
)

# --- 2. Funções de Carregamento de Documentos ---
def load_all_context_documents(directory_path: str):
    """
    Carrega todos os documentos de um diretório, tratando diferentes extensões.
    """
    loaders = {
        ".txt": TextLoader,
        ".md": UnstructuredMarkdownLoader,
        ".docx": UnstructuredWordDocumentLoader,
    }
    all_documents = []
    
    for ext, loader_cls in loaders.items():
        try:
            loader = DirectoryLoader(
                directory_path,
                glob=f"**/*{ext}",
                loader_cls=loader_cls,
                loader_kwargs={"encoding": "utf-8"} if ext == ".txt" else {}
            )
            loaded_docs = loader.load()
            print(f"Carregados {len(loaded_docs)} documentos com extensão {ext}.")
            all_documents.extend(loaded_docs)
        except Exception as e:
            print(f"Aviso: Não foi possível carregar arquivos {ext}. Erro: {e}")

    if not all_documents:
        raise FileNotFoundError(f"Nenhum arquivo de contexto encontrado em: {directory_path}")
    
    return all_documents

# --- 3. Configuração do RAG ---
# Agora, o script carrega todos os documentos do diretório
context_documents = load_all_context_documents(CONTEXT_DIR_PATH)

embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}
)

qdrant_vector_store = Qdrant.from_documents(
    documents=context_documents,
    embedding=embeddings,
    location=":memory:",
    collection_name="criterios_mat"
)

def create_prompt_from_rag(query: str, vector_store: Qdrant, k_results: int = 5) -> str:
    """
    Gera um prompt contextualizado buscando informações relevantes no banco de dados vetorial.
    """
    results = vector_store.similarity_search(query, k=k_results)
    context = "\n\n".join([doc.page_content for doc in results])
    
    return f"""
Você é um avaliador pedagógico da área de Matemática. Responda com base apenas no contexto fornecido abaixo.

Contexto:
{context}

Pergunta:
{query}

Responda em português brasileiro, de forma clara, objetiva e fundamentada.
    """.strip()

# --- 4. Função Principal do Chatbot ---
def chatbot_gemini(pergunta: str) -> str:
    """
    Processa a pergunta do usuário, gera um prompt com RAG e obtém a resposta do modelo Gemini.
    """
    prompt = create_prompt_from_rag(pergunta, qdrant_vector_store)
    
    model = genai.GenerativeModel(
        model_name=GEMINI_MODEL_NAME,
        generation_config=GENERATION_CONFIG
    )
    
    response = model.generate_content(contents=[prompt])
    return response.text

# --- 5. Classe de Log Personalizada ---
class CSVCustomLogger(gr.FlaggingCallback):
    """
    Classe para registrar interações do chatbot em um arquivo CSV.
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    def setup(self, components, flagging_dir):
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Pergunta", "Resposta", "Classificacao"])

    def flag(self, flag_data: list, flag_option: str = None, username: str = None):
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                flag_data[0],
                flag_data[1],
                flag_option or "não indicou"
            ])
        return "OK"

# --- 6. Configuração e Lançamento da Interface Gradio ---
if __name__ == "__main__":
    custom_logger = CSVCustomLogger(LOG_FILE_PATH)

    demo = gr.Interface(
        fn=chatbot_gemini,
        inputs=gr.Textbox(label="Digite sua pergunta", lines=3),
        outputs=gr.Textbox(label="Resposta do Chatbot"),
        title="Chatbot Pedagógico - Matemática (RAG + Gemini API)",
        description=(
            "Este chatbot oferece feedback pedagógico em Matemática, "
            "baseado em critérios definidos em um documento de contexto (.txt, .md ou .docx)."
        ),
        flagging_mode="manual",
        flagging_options=["Boa", "Ruim", "Melhorar"],
        flagging_callback=custom_logger
    )

    demo.launch(inbrowser=True)