import requests
import json

# IMPORTANTE: Nunca commite a API key real no Git!
# Substitua pela sua chave real antes de executar
api_key = "SUA_API_KEY_AQUI"  # Obtenha em https://openrouter.ai/keys

print("=" * 70)
print("🔍 DIAGNÓSTICO COMPLETO DA API OPENROUTER")
print("=" * 70)
print()

# Teste 1: Verificar formato da chave
print("📋 TESTE 1: Formato da Chave")
print("-" * 70)
print(f"Comprimento: {len(api_key)} caracteres")
print(f"Inicia com: {api_key[:15]}")
print(f"Termina com: {api_key[-15:]}")
print(f"Espaços em branco: {' ' in api_key}")
tem_quebra = '\n' in api_key or '\r' in api_key
print(f"Quebras de linha: {tem_quebra}")
print()

# Teste 2: Verificar conectividade com OpenRouter
print("📋 TESTE 2: Conectividade Básica")
print("-" * 70)
try:
    resp = requests.get('https://openrouter.ai', timeout=10)
    print(f"✅ OpenRouter acessível: Status {resp.status_code}")
except Exception as e:
    print(f"❌ Erro ao acessar OpenRouter: {e}")
print()

# Teste 3: Testar endpoint de models (não requer autenticação)
print("📋 TESTE 3: Endpoint de Modelos (sem autenticação)")
print("-" * 70)
try:
    resp = requests.get('https://openrouter.ai/api/v1/models', timeout=10)
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        models = resp.json()
        # Procurar modelo deepseek
        deepseek_models = [m for m in models.get('data', []) if 'deepseek' in m.get('id', '').lower()]
        print(f"✅ Modelos Deepseek disponíveis: {len(deepseek_models)}")
        for model in deepseek_models[:3]:
            print(f"  - {model.get('id')}")
    else:
        print(f"❌ Erro: {resp.text[:200]}")
except Exception as e:
    print(f"❌ Erro: {e}")
print()

# Teste 4: Testar autenticação com a chave
print("📋 TESTE 4: Autenticação com API Key")
print("-" * 70)
url = 'https://openrouter.ai/api/v1/chat/completions'
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json',
}

# Teste com modelo gratuito Deepseek
payload_deepseek = {
    'model': 'deepseek/deepseek-r1:free',
    'messages': [{'role': 'user', 'content': 'Oi'}]
}

print("Testando modelo: deepseek/deepseek-r1:free")
try:
    resp = requests.post(url, headers=headers, json=payload_deepseek, timeout=10)
    print(f"Status Code: {resp.status_code}")
    
    if resp.status_code == 200:
        print("✅ SUCESSO! API key válida!")
        data = resp.json()
        print(f"Resposta: {json.dumps(data, indent=2)[:300]}")
    elif resp.status_code == 401:
        print("❌ ERRO 401: Unauthorized")
        print(f"Resposta: {resp.text}")
        print("\n🔍 Possíveis causas:")
        print("  - API key inválida ou expirada")
        print("  - Conta não verificada")
        print("  - Chave revogada")
    elif resp.status_code == 402:
        print("❌ ERRO 402: Payment Required")
        print(f"Resposta: {resp.text}")
        print("\n🔍 Possível causa:")
        print("  - Conta sem créditos")
        print("  - Modelo requer pagamento")
    elif resp.status_code == 429:
        print("⚠️ ERRO 429: Rate Limit")
        print(f"Resposta: {resp.text}")
    else:
        print(f"❌ ERRO {resp.status_code}")
        print(f"Resposta completa: {resp.text}")
except Exception as e:
    print(f"❌ Exceção: {e}")
print()

# Teste 5: Testar com modelo alternativo gratuito
print("📋 TESTE 5: Modelo Alternativo Gratuito")
print("-" * 70)
modelos_gratuitos = [
    'meta-llama/llama-3.2-1b-instruct:free',
    'google/gemma-2-9b-it:free',
    'qwen/qwen-2-7b-instruct:free'
]

for modelo in modelos_gratuitos:
    print(f"\nTestando: {modelo}")
    payload = {
        'model': modelo,
        'messages': [{'role': 'user', 'content': 'test'}]
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"  Status: {resp.status_code}")
        if resp.status_code == 200:
            print(f"  ✅ Funciona com {modelo}!")
            break
        else:
            print(f"  ❌ {resp.text[:100]}")
    except Exception as e:
        print(f"  ❌ Erro: {e}")

print()
print("=" * 70)
print("🏁 FIM DO DIAGNÓSTICO")
print("=" * 70)
