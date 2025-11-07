import requests
import json

# IMPORTANTE: Nunca commite a API key real no Git!
# Substitua pela sua chave real antes de executar
api_key = "SUA_API_KEY_AQUI"  # Obtenha em https://openrouter.ai/keys
url = 'https://openrouter.ai/api/v1/chat/completions'

headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

payload = {
    'model': 'deepseek/deepseek-r1:free',
    'messages': [
        {'role': 'user', 'content': 'Teste simples'}
    ]
}

print("🔍 Testando API key do Deepseek...")
print(f"API Key: {api_key[:20]}...{api_key[-10:]}")
print(f"URL: {url}")
print()

try:
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    print(f"Status Code: {resp.status_code}")
    print()
    
    if resp.status_code == 200:
        print("✅ API KEY VÁLIDA!")
        data = resp.json()
        print(f"Resposta: {json.dumps(data, indent=2)[:500]}")
    elif resp.status_code == 401:
        print("❌ API KEY INVÁLIDA - Erro 401 Unauthorized")
        print(f"Resposta: {resp.text}")
    elif resp.status_code == 429:
        print("⚠️ RATE LIMIT - Muitas requisições")
        print(f"Resposta: {resp.text}")
    else:
        print(f"❌ ERRO {resp.status_code}")
        print(f"Resposta: {resp.text[:500]}")
        
except requests.exceptions.Timeout:
    print("⏱️ TIMEOUT - API não respondeu em 30 segundos")
except Exception as e:
    print(f"❌ ERRO: {e}")
