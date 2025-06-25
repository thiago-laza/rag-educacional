import os
import csv
from dotenv import load_dotenv
import gradio as gr
from google import genai
from google.genai import types

from langchain_community.document_loaders import (
    TextLoader,
    UnstructuredMarkdownLoader,
    UnstructuredWordDocumentLoader,
)
from langchain_community.vectorstores import Qdrant
from langchain_community.embeddings import HuggingFaceEmbeddings

# Carrega variáveis de ambiente (API Key)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente GEMINI_API_KEY não está definida.")

# Inicializa cliente Gemini
client = genai.Client(api_key=api_key)

# Caminho do arquivo de conhecimento (pode ser .txt, .md ou .docx)
base_path = "/home/laza/chat_RAG_hf/api/chat_05_MAT/documentos/contexto_pedagogico"

# Detecta extensão e escolhe o loader adequado
if os.path.exists(base_path + ".txt"):
    print("Usando arquivo: ")
    loader = TextLoader(base_path + ".txt", encoding="utf-8")
elif os.path.exists(base_path + ".md"):
    print("Usando arquivo: /home/laza/chat_RAG_hf/api/chat_05_MAT/documentos/contexto_pedagogico.md")
    loader = UnstructuredMarkdownLoader(base_path + ".md")
elif os.path.exists(base_path + ".docx"):
    print("Usando arquivo: criterios_analise_mat.docx")
    loader = UnstructuredWordDocumentLoader(base_path + ".docx")
else:
    raise FileNotFoundError("Nenhum arquivo de base encontrado com extensões .txt, .md ou .docx")

# Carrega documentos
docs = loader.load()

# Cria embeddings e base vetorial (Qdrant em memória)
embeddings = HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5",
    model_kwargs={"device": "cpu"}
)

qdrant = Qdrant.from_documents(
    documents=docs,
    embedding=embeddings,
    location=":memory:",
    collection_name="criterios_mat"
)

# Função que monta o prompt com base no contexto
def create_prompt(query: str):
    results = qdrant.similarity_search(query, k=5)
    context = "\n\n".join([doc.page_content for doc in results])
    return f"""
Você é um avaliador pedagógico da área de Matemática. Responda com base apenas no contexto abaixo.

Contexto:
{context}

Pergunta:
{query}

Responda em português brasileiro, de forma clara, objetiva e fundamentada.
    """.strip()

# Função do chatbot com Gemini
def chatbot_gemini(pergunta):
    prompt = create_prompt(pergunta)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt],
        config=types.GenerateContentConfig(
            max_output_tokens=400,
            temperature=0.1
        )
    )
    return response.text

# Classe personalizada para salvar interações com classificação
class CSVCustomLogger(gr.FlaggingCallback):
    def __init__(self, csv_path):
        self.csv_path = csv_path
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)

    def setup(self, components, flagging_dir):
        # Cria o cabeçalho se o arquivo não existir
        if not os.path.exists(self.csv_path):
            with open(self.csv_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Pergunta", "Resposta", "Classificacao"])

    def flag(self, flag_data, flag_option=None, username=None):
        # flag_data[0] = pergunta, flag_data[1] = resposta
        with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                flag_data[0],
                flag_data[1],
                flag_option or "não indicou"
            ])
        return "OK"

# Instancia o logger personalizado
custom_logger = CSVCustomLogger("logs/interacoes_chat.csv")

# Interface Gradio
demo = gr.Interface(
    fn=chatbot_gemini,
    inputs=gr.Textbox(label="Digite sua pergunta", lines=3),
    outputs=gr.Textbox(label="Resposta do Chatbot"),
    title="Chatbot Pedagógico - Matemática (RAG + Gemini API)",
    description="Este chatbot responde com base em critérios pedagógicos definidos em um arquivo (.txt, .md ou .docx).",
    flagging_mode="manual",
    flagging_options=["Boa", "Ruim", "Melhorar"],
    flagging_callback=custom_logger
)

if __name__ == "__main__":
    demo.launch(inbrowser=True)
