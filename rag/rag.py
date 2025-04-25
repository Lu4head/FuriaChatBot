import os

from decouple import config

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings


os.environ['HUGGINGFACE_API_KEY'] = config('HUGGINGFACE_API_KEY')


if __name__ == '__main__':
    # Carrega dados do arquivo PDF
    pdf1_file_path = '/app/rag/data/FURIA_Esports_Contexto.pdf'
    pdf1_loader = PyPDFLoader(pdf1_file_path) 
    pdf1 = pdf1_loader.load()
    
    pdf2_file_path = '/app/rag/data/Furia_Esports.pdf'
    pdf2_loader = PyPDFLoader(pdf2_file_path) 
    pdf2 = pdf2_loader.load()
    
    # Carregar dados de arquivo TXT
    txt_file_path = '/app/rag/data/FURIA_Esports.txt'
    txt_loader = TextLoader(txt_file_path)
    txt = txt_loader.load()

    text_splitter = RecursiveCharacterTextSplitter( # Define como será realizada a divisão dos dados
        chunk_size=1000,
        chunk_overlap=200,
    ) 
    
    chunks = text_splitter.split_documents( # Cria os chuncks do arquivos enviado como parâmetro com base na divisão definida acima
        documents= [
            *pdf1,
            *pdf2,
            *txt,
        ]
    )

    persist_directory = '/app/chroma_data'

    
    embedding = HuggingFaceEmbeddings() # Carrega modelos de embedding do HuggingFace
    
    # Inicializa o Banco de dados Chroma (banco de dados de vetores)
    vector_store = Chroma(
        embedding_function=embedding, # Modelo de embedding utilizado
        persist_directory=persist_directory, # Diretório onde será salvo o banco de dados
    )
    
    vector_store.add_documents( # Adiciona os chunks no banco de dados
        documents=chunks,
    )
