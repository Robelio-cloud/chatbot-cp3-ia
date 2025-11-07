# 🔒 Guia de Segurança - API Keys

## ⚠️ NUNCA COMMITE API KEYS NO GIT!

Este projeto usa a API do OpenRouter/Deepseek. As chaves são **secretas e pessoais**.

---

## 📋 Como Configurar Corretamente

### 1️⃣ Obter uma Nova API Key

1. Acesse: https://openrouter.ai/keys
2. Faça login (ou crie uma conta)
3. **VERIFIQUE SEU EMAIL** (obrigatório!)
4. Clique em **"Create Key"**
5. Copie a chave completa (formato: `sk-or-v1-...`)

### 2️⃣ Configurar Localmente (Para Desenvolvimento)

Edite o arquivo `.streamlit/secrets.toml`:

```toml
[deepseek]
api_key = "sk-or-v1-SUA_CHAVE_REAL_AQUI"
```

✅ **Este arquivo está no `.gitignore`** - Não será commitado!

### 3️⃣ Configurar no Streamlit Cloud (Para Produção)

1. Acesse: https://share.streamlit.io
2. Selecione seu app: **chatbot-cp3-ia**
3. Clique em **⚙️ Settings**
4. Vá em **Secrets**
5. Cole:
```toml
[deepseek]
api_key = "sk-or-v1-SUA_CHAVE_REAL_AQUI"
```
6. Clique em **Save**

### 4️⃣ Configurar em Notebooks/Scripts de Teste

**❌ NUNCA faça isso:**
```python
API_KEY = "sk-or-v1-b945dcfa..."  # ❌ EXPOSTO NO GIT!
```

**✅ FAÇA isso:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")  # ✅ Variável de ambiente

# Ou leia do secrets.toml
import streamlit as st
API_KEY = st.secrets["deepseek"]["api_key"]  # ✅ Usando Streamlit secrets
```

---

## 🚨 O Que Fazer Se Expor a Chave

### Se você commitou uma chave acidentalmente:

1. **⚡ Ação Imediata:**
   - Acesse https://openrouter.ai/keys
   - **DELETE** a chave exposta imediatamente
   - Gere uma **nova chave**

2. **🧹 Limpar o Git:**
   ```bash
   # Remover chave do arquivo
   git add .
   git commit -m "security: remove exposed API key"
   git push
   ```

3. **🔐 Configurar Corretamente:**
   - Use `.gitignore` (já configurado!)
   - Use variáveis de ambiente
   - Use Streamlit Secrets (produção)

---

## 📂 Arquivos que NUNCA devem ter chaves:

- ❌ `test_api.py`
- ❌ `diagnostico_api.py`
- ❌ `teste_deepseek_simples.ipynb`
- ❌ Qualquer arquivo commitado no Git

## 📂 Arquivos seguros para chaves:

- ✅ `.streamlit/secrets.toml` (no `.gitignore`)
- ✅ `.env` (no `.gitignore`)
- ✅ Variáveis de ambiente do sistema

---

## 🛡️ Boas Práticas de Segurança

1. **Sempre use placeholders** nos arquivos de exemplo:
   ```python
   API_KEY = "SUA_API_KEY_AQUI"
   ```

2. **Rotacione suas chaves periodicamente** (a cada 30-90 dias)

3. **Monitore o uso** no dashboard do OpenRouter

4. **Delete chaves não utilizadas** imediatamente

5. **Nunca compartilhe chaves** por email, chat, etc.

---

## 📧 Contato OpenRouter

- **Suporte**: support@openrouter.ai
- **Segurança**: security@openrouter.ai
- **Dashboard**: https://openrouter.ai/keys

---

## ✅ Checklist de Segurança

Antes de fazer push para o GitHub:

- [ ] Verificou que não há `sk-or-v1-` em arquivos commitados
- [ ] `.streamlit/secrets.toml` está no `.gitignore`
- [ ] Arquivos de teste usam placeholders (`SUA_API_KEY_AQUI`)
- [ ] README tem instruções claras de configuração
- [ ] Produção usa Streamlit Cloud Secrets

---

## 🎯 Lembre-se:

> **"Chaves de API são como senhas - nunca compartilhe ou publique!"**

Se tiver dúvidas, consulte:
- https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management
- https://openrouter.ai/docs#api-keys
