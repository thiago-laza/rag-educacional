import os
import csv
from dotenv import load_dotenv
import gradio as gr
import google.generativeai as genai

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

# --- 1. Configurações e Variáveis de Ambiente ---

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente 'GEMINI_API_KEY' não está definida. Crie um arquivo .env na raiz do projeto.")

# Configura a API do Gemini globalmente
genai.configure(api_key=GEMINI_API_KEY)

# Caminho base para o documento de contexto
# Ajuste conforme a localização real do seu arquivo no projeto
CONTEXT_DOC_BASE_PATH = "/home/laza/chat_RAG_hf/api/chat_05_MAT/documentos/contexto_pedagogico"
LOGS_DIR = "logs"
LOG_FILE_PATH = os.path.join(LOGS_DIR, "interacoes_chat_mat.csv") # Nome do log específico para matemática

# Configurações do modelo Gemini
GEMINI_MODEL_NAME = "gemini-1.5-flash-latest"
GENERATION_CONFIG = genai.types.GenerationConfig(
    max_output_tokens=400,
    temperature=0.1
)

# --- 2. Funções de Carregamento de Documentos (Poderia ser um módulo 'rag_loader.py') ---

def load_context_document(base_path: str):
    """
    Detecta a extensão do arquivo de contexto e carrega o documento usando o loader apropriado.
    """
    if os.path.exists(base_path + ".txt"):
        print(f"Usando arquivo: {base_path}.txt")
        loader = TextLoader(base_path + ".txt", encoding="utf-8")
    elif os.path.exists(base_path + ".md"):
        print(f"Usando arquivo: {base_path}.md")
        loader = UnstructuredMarkdownLoader(base_path + ".md")
    elif os.path.exists(base_path + ".docx"):
        print(f"Usando arquivo: {base_path}.docx")
        loader = UnstructuredWordDocumentLoader(base_path + ".docx")
    else:
        raise FileNotFoundError(
            f"Nenhum arquivo de base encontrado para o caminho: {base_path} com extensões .txt, .md ou .docx"
        )
    return loader.load()

# --- 3. Configuração do RAG (Poderia ser um módulo 'rag_core.py') ---

# Carrega documentos
context_documents = load_context_document(CONTEXT_DOC_BASE_PATH)

# Cria embeddings
# O device='cpu' é bom para compatibilidade, mas pode ser 'cuda' se tiver GPU NVIDIA
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}
)

# Cria base vetorial (Qdrant em memória)
qdrant_vector_store = Qdrant.from_documents(
    documents=context_documents,
    embedding=embeddings,
    location=":memory:", # Banco de dados em memória para simplicidade
    collection_name="criterios_mat" # Nome da coleção
)

def create_prompt_from_rag(query: str, vector_store: Qdrant, k_results: int = 5) -> str:
    """
    Gera um prompt contextualizado buscando informações relevantes no banco de dados vetorial.
    """
    results = vector_store.similarity_search(query, k=k_results)
    context = "\n\n".join([doc.page_content for doc in results])
    
    # Template de prompt ajustado para Matemática
    return f"""
Você é um avaliador pedagógico da área de Matemática. Responda com base apenas no contexto fornecido abaixo.

Contexto:
{context}

Pergunta:
{query}

Responda em português brasileiro, de forma clara, objetiva e fundamentada.
    """.strip()

# --- 4. Função Principal do Chatbot (Poderia ser parte de 'rag_core.py' ou 'gemini_service.py') ---

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

# --- 5. Classe de Log Personalizada (Poderia ser um módulo 'utils/csv_logger.py') ---

class CSVCustomLogger(gr.FlaggingCallback):
    """
    Classe para registrar interações do chatbot em um arquivo CSV,
    incluindo pergunta, resposta e classificação.
    """
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        # Garante que o diretório de logs exista
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    def setup(self, components, flagging_dir):
        # Cria o cabeçalho do CSV se o arquivo não existir
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Pergunta", "Resposta", "Classificacao"])

    def flag(self, flag_data: list, flag_option: str = None, username: str = None):
        """
        Registra a interação (pergunta, resposta) e a classificação no CSV.
        """
        # flag_data[0] = pergunta, flag_data[1] = resposta
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                flag_data[0],
                flag_data[1],
                flag_option or "não indicou" # Usa "não indicou" se a classificação for nula
            ])
        return "OK"

# --- 6. Configuração e Lançamento da Interface Gradio ---

if __name__ == "__main__":
    # Instancia o logger personalizado
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