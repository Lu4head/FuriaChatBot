import os

from decouple import config

from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings


os.environ['GROQ_API_KEY'] = config('GROQ_API_KEY')


class AIBot:

    def __init__(self):
        self.__chat = ChatGroq(model='llama-3.3-70b-versatile')
        self.__retriever = self.__build_retriever()
        
    def __build_retriever(self): # Recupera os dados para geração da resposta do banco de dados chroma
        persist_directory = '/app/chroma_data'
        embedding = HuggingFaceEmbeddings()

        vector_store = Chroma(
            persist_directory=persist_directory,
            embedding_function=embedding,
        )
        return vector_store.as_retriever(
            search_kwargs={'k': 30},
        )

    def __build_messages(self, history_messages, question): # Cria a mensagem a ser enviada para o modelo
        messages = []
        for message in history_messages:
            message_class = HumanMessage if message.get('fromMe') else AIMessage
            messages.append(message_class(content=message.get('body')))
        messages.append(HumanMessage(content=question))
        return messages

    def invoke(self, history_messages, question):
        SYSTEM_TEMPLATE = '''
            Responda as perguntas dos usuários com base no contexto abaixo.
            Você é um assistente inteligente especializado na organização brasileira de esports FURIA Esports. 
            Seu objetivo é responder perguntas de fãs, jornalistas, entusiastas e profissionais da área com base em informações atualizadas e verificadas extraídas de um documento estruturado que contém a história, conquistas, equipes, parcerias e curiosidades da FURIA Esports.
            Você deve responder sempre com clareza e precisão, utilizando uma linguagem acessível para fãs casuais, mas com profundidade para perguntas mais técnicas. Cite os nomes dos jogadores, técnicos ou eventos relevantes quando aplicável. Quando necessário, explique os termos do cenário competitivo de esports de forma que qualquer pessoa possa entender. Nunca invente informações que você não possa afirmar que sejam reais com bases nos dados que você poossui. Se a resposta não estiver contida nos dados, diga de forma educada que não há informação disponível no momento.
            Seja sempre prestativo, entusiasta e apaixonado por esports, representando com orgulho o espírito da FURIA. 
            Leve em consideração também o histórico de mensagens da conversa com o usuário.
            Responda sempre em português brasileiro.           
            <context>
            {context}
            </context>
            '''
        docs = self.__retriever.invoke(question) # Recupera os chunks do banco de dados
        question_answering_prompt = ChatPromptTemplate.from_messages( # Cria a mensagem a ser enviada para o modelo
            [
                (
                    'system',
                    SYSTEM_TEMPLATE,
                ),
                MessagesPlaceholder(variable_name='messages'),
            ]
        )
        document_chain = create_stuff_documents_chain(self.__chat, question_answering_prompt) # Cria a cadeia de documentos
        response = document_chain.invoke( # Gera a resposta
            {
                'context': docs,
                'messages': self.__build_messages(history_messages, question),
            }
        )
        return response