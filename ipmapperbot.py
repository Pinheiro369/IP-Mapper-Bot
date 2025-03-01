import logging
import requests
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuração do logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Função para verificar se o IP é válido
def is_valid_ip(ip):
    pattern = re.compile(r'^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$')
    return bool(pattern.match(ip))

# Função para obter informações do IP
def get_ip_info(ip):
    url = f"http://ipinfo.io/{ip}/json"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta uma exceção para status code 4xx/5xx
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao obter informações do IP: {e}")
        return None

# Função para criar uma estrutura de "nodes" (nós) para exibir a resposta
def format_ip_info(info):
    # Adicionando as informações em um formato estruturado
    nodes = {
        "IP": info.get('ip', 'N/A'),
        "Hostname": info.get('hostname', 'N/A'),
        "Cidade": info.get('city', 'N/A'),
        "Região": info.get('region', 'N/A'),
        "País": info.get('country', 'N/A'),
        "Localização": info.get('loc', 'N/A'),
        "Provedor": info.get('org', 'N/A'),
        "Fuso Horário": info.get('timezone', 'N/A'),
        "Código Postal": info.get('postal', 'N/A'),
        "Latitude/Longitude": info.get('loc', 'N/A'),
        "Organização": info.get('org', 'N/A'),
    }
    return nodes

# Comando /ipinfo
async def ipinfo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ Por favor, forneça um IP. Exemplo: /ipinfo 8.8.8.8")
        return

    ip = context.args[0]

    # Verifica se o IP fornecido é válido
    if not is_valid_ip(ip):
        await update.message.reply_text("❌ O IP fornecido não é válido. Exemplo de IP válido: 8.8.8.8")
        return
    
    info = get_ip_info(ip)

    if info:
        # Formata a resposta em Markdown
        nodes = format_ip_info(info)
        message = (
            f"🌐 **Informações Detalhadas do IP**\n\n"
            f"🔢 **IP**: `{nodes['IP']}`\n"
            f"🏷️ **Hostname**: `{nodes['Hostname']}`\n"
            f"🏙️ **Cidade**: `{nodes['Cidade']}`\n"
            f"📍 **Região**: `{nodes['Região']}`\n"
            f"🇵🇹 **País**: `{nodes['País']}`\n"
            f"📌 **Localização**: `{nodes['Localização']}`\n"
            f"🏢 **Provedor**: `{nodes['Provedor']}`\n\n"
            f"🕒 **Fuso Horário**: `{nodes['Fuso Horário']}`\n"
            f"📍 **Código Postal**: `{nodes['Código Postal']}`\n"
            f"🌍 **URL de Detalhes**: [ipinfo.io/{info.get('ip')}]({'http://ipinfo.io/' + info.get('ip') + '/json'})\n"
            f"📊 **Detalhes Adicionais**:\n"
            f"  - **Latitude/Longitude**: `{nodes['Latitude/Longitude']}`\n"
            f"  - **Organização**: `{nodes['Organização']}`"
        )
    else:
        message = "❌ Não foi possível obter informações para o IP fornecido. Tente novamente mais tarde."

    # Envia a mensagem formatada com Markdown
    await update.message.reply_text(message, parse_mode="Markdown")

# Função para exibir informações do bot
async def bot_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_message = (
        "🤖 **Informações do Bot**\n\n"
        "Este bot fornece informações sobre um IP fornecido. Exemplos de uso:\n"
        "/ipinfo 8.8.8.8 - Obtém informações detalhadas de um IP\n\n"
        "Desenvolvido por: Pinheiro369\n"
        "Fonte de Dados: [ipinfo.io](https://ipinfo.io)\n"
        "Requisitos: Acesso à internet para obter informações IP."
    )
    await update.message.reply_text(info_message, parse_mode="Markdown")

# Função principal
def main():
    # Cria a aplicação e passa o token do bot diretamente
    application = Application.builder().token(" SEU TOKEN DO BOT").build()
    
    # Adiciona os comandos
    application.add_handler(CommandHandler("ipinfo", ipinfo))
    application.add_handler(CommandHandler("botinfo", bot_info))

    # Inicia o bot
    application.run_polling()

if __name__ == '__main__':
    main()