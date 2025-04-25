from flask import Flask, request, jsonify

from bot.ai_bot import AIBot
from services.waha import Waha


app = Flask(__name__)


@app.route('/chatbot/webhook/', methods=['POST'])
def webhook():
    data = request.json # JSON dos dados recebidos da API do WAHA

    print(f'EVENTO RECEBIDO: {data}')

    chat_id = data['payload']['from'] # Identifica quem enviou a mensagem
    received_message = data['payload']['body'] # Mensagem recebida
    is_group = '@g.us' in chat_id # Se no chat_id tiver @g.us, a mensagem é de um grupo
    is_status = 'status@broadcast'in chat_id # Se no chat_id tiver status@broadcast, a mensagem é de um status

    if is_group or is_status: # Se a mensagem é de um grupo ou status, ignora
        return jsonify({'status': 'success', 'message': 'Mensagem de grupo/status ignorada.'}), 200
    
    waha = Waha()
    ai_bot = AIBot()
    
    waha.start_typing(chat_id=chat_id) # Exibir status de digitando na conversa do WhahatsApp equanto o bot estiver processando a resposta
    history_messages = waha.get_history_messages( # Obtém o histórico de mensagens da conversa
        chat_id=chat_id,
        limit=10,
    )
    response_message = ai_bot.invoke( # Envia a mensagem para o modelo de IA e recebe a resposta
        history_messages=history_messages,
        question=received_message,
    )
    waha.send_message( # Envia a resposta para o WhahatsApp
        chat_id=chat_id,
        message=response_message,
    )
    waha.stop_typing(chat_id=chat_id) # Finaliza o status de digitando após a resposta ser enviada

    return jsonify({'status': 'success'}), 200 # Retorna o status de sucesso para o WAHA


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
