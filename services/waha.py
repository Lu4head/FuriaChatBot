import requests


class Waha:

    def __init__(self, port : int = 3000, session : str ="default"):
        self.__api_url = f'http://waha:{port}'
        self.__session = session
        
    def send_message(self, chat_id, message):
        ''' 
        ### Enviar mensagem WhastApp. 
        
        args:
            * chat_id: str | Destinatário da mensagem
            * message: str | Mensagem a ser enviada
        '''
        
        url = f'{self.__api_url}/api/sendText' # Endpoint da API do WAHA para envio de mensagens de texto
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': self.__session,
            'chatId': chat_id,
            'text': message,
        }
        requests.post( # Envia uma requisição POST para o endpoint da API do WAHA com os dados para envio da mensagem
            url=url,
            json=payload,
            headers=headers,
        )
    
    def get_history_messages(self, chat_id, limit):
        '''
        ### Obter o histórico de mensagens de um chat.
        
        args:
            * chat_id: str | Identificador do chat
            * limit: int | Número máximo de mensagens a serem retornadas
            
        return:
            * list | Lista de mensagens
        '''
        
        url = f'{self.__api_url}/api/default/chats/{chat_id}/messages?limit={limit}&downloadMedia=false' # Endpoint da API do WAHA para obter o histórico de mensagens
        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.get(
            url=url,
            headers=headers,
        )
        return response.json()
        
    def start_typing(self, chat_id):
        url = f'{self.__api_url}/api/startTyping' # Endpoint da API do WAHA para iniciar o status de digitando
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': self.__session,
            'chatId': chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )

    def stop_typing(self, chat_id):
        url = f'{self.__api_url}/api/stopTyping' # Endpoint da API do WAHA para parar o status de digitando
        headers = {
            'Content-Type': 'application/json',
        }
        payload = {
            'session': self.__session,
            'chatId': chat_id,
        }
        requests.post(
            url=url,
            json=payload,
            headers=headers,
        )
    