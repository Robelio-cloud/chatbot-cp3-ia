# 🤘 RockStar Burger - Chatbot Inteligente

![image](/images/chatbot-02.png)

## 🎸 Sobre o Projeto

**RockStar Burger** é um chatbot inteligente para uma **lanchonete temática de Rock e Metal** que utiliza técnicas avançadas de Processamento de Linguagem Natural (NLP) para atender clientes de forma interativa e divertida.

### 🎯 Tipo de Estabelecimento
**Lanchonete Temática Rock/Metal** - Um ambiente que combina a paixão pelo rock com hambúrgueres gourmet, onde cada produto tem nome de música clássica do rock/metal.

## 🚀 Funcionalidades

- ✅ **Detecção de Múltiplas Intenções** em uma única frase
- ✅ **11 Categorias de Intenções** (cumprimentos, cardápio, preços, pedidos, ingredientes/receitas, etc.)
- ✅ **500+ Exemplos de Frases** incluindo erros de digitação comuns
- ✅ **Respostas Temáticas** no estilo rock/metal
- ✅ **Interface Web Interativa** com Streamlit
- ✅ **Análise Técnica Detalhada** dos resultados
- ✅ **Sistema Híbrido** (Classificador ML + Busca por Similaridade)
- 🆕 **Integração com API Deepseek** via OpenRouter para consulta de ingredientes
- 🆕 **Agent Configurado** para retornar ingredientes em formato JSON estruturado
- 🆕 **Identificação de Alergênicos** automaticamente pela IA
- 🆕 **Cache Inteligente** de receitas consultadas
- 🆕 **Retry Automático** com backoff exponencial para resiliência da API

## 🛠️ Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit** - Interface web
- **NLTK** - Processamento de linguagem natural
- **Scikit-learn** - Machine Learning
- **Pandas/NumPy** - Manipulação de dados
- **TF-IDF** - Vetorização de texto
- **Logistic Regression** - Classificação
- **Cosine Similarity** - Busca por similaridade
- **Requests** - Requisições HTTP para APIs
- **API Deepseek R1** (via OpenRouter) - Inteligência Artificial generativa
- **JSON** - Formato estruturado de dados

## 📦 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### 1. Clone o Repositório
```bash
git clone <url-do-repositorio>
cd chatbot-cp2-ia
```

### 2. Instale as Dependências
```bash
pip install streamlit nltk scikit-learn pandas numpy requests
```

### 3. Configure a API Key do Deepseek

Crie o arquivo `.streamlit/secrets.toml` com sua chave da API OpenRouter:

```toml
[deepseek]
api_key = "sk-or-v1-SUA_CHAVE_AQUI"
```

> **Importante:** Este arquivo NÃO deve ser commitado no Git (já está no `.gitignore`)

Para obter uma API key gratuita:
1. Acesse [openrouter.ai](https://openrouter.ai)
2. Crie uma conta
3. Gere uma API key
4. Cole no arquivo `secrets.toml`

### 4. Downloads do NLTK (Automático)
O sistema baixa automaticamente os recursos necessários do NLTK:
- `punkt` - Tokenização
- `stopwords` - Palavras irrelevantes (português)
- `wordnet` - Lematização

## 🏃‍♂️ Como Executar

### Método 1: Comando Direto
```bash
streamlit run app.py
```

### Método 2: Via Módulo Python
```bash
python -m streamlit run app.py
```

### 3. Acesse no Navegador
Após executar, abra seu navegador em:
- **Local**: http://localhost:8501
- **Rede**: http://[seu-ip]:8501

## 📁 Estrutura dos Arquivos

```
chatbot-cp3-ia/
├── app.py                           # 🎯 Aplicação principal Streamlit (56.7 KB)
├── app_backup_20251107_080449.py    # 💾 Backup seguro da versão estável
├── intents_database.json            # 🧠 Base de dados das intenções (504 exemplos)
├── menu.json                        # 🍔 Cardápio com preços (9 lanches + 7 bebidas)
├── requirements.txt                 # 📦 Dependências do projeto
├── .gitignore                       # 🔒 Arquivos ignorados pelo Git
├── .gitattributes                   # ⚙️ Configurações do repositório
├── .streamlit/
│   └── secrets.toml                 # 🔑 API keys (NÃO commitar!)
├── images/
│   ├── chatbot-01.png              # 📸 Screenshot da aplicação web
│   └── chatbot-02.png              # 📸 Screenshot do funcionamento
├── README.md                        # 📚 Documentação principal completa
├── SECURITY.md                      # 🛡️ Guidelines de segurança e API keys
└── BACKUP_INFO.md                   # 💾 Documentação dos backups do projeto
```

### 📊 Estatísticas dos Arquivos

| Arquivo | Tamanho | Descrição |
|---------|---------|-----------|
| `app.py` | 56.7 KB | Aplicação completa com 11 intenções |
| `intents_database.json` | 30.0 KB | 504 exemplos de treino (v2.0) |
| `menu.json` | 1.5 KB | Cardápio completo estruturado |
| `README.md` | 14.0 KB | Documentação detalhada |
| `SECURITY.md` | 3.6 KB | Guia de segurança |
| `BACKUP_INFO.md` | 2.4 KB | Informações de backup |

## 🎯 Cardápio RockStar Burger

### 🍔 LANCHES

| Lanche | Preço |
|--------|-------|
| **Hambúrguer** | R$ 20,00 |
| **X-Burger** | R$ 23,00 |
| **X-Salada** | R$ 25,50 |
| **X-Bacon** | R$ 26,00 |
| **X-Egg** | R$ 24,00 |
| **X-Calabresa** | R$ 23,00 |
| **X-Frango** | R$ 23,00 |
| **X-Tudo** | R$ 31,00 |
| **Vegetariano** 🌱 | R$ 25,00 |

### 🥤 BEBIDAS

| Bebida | Preço |
|--------|-------|
| **Refrigerante (lata)** | R$ 6,00 |
| **Água** | R$ 4,00 |
| **Suco de Laranja Natural** 🍊 | R$ 7,50 |
| **Cerveja (lata)** 🍺 | R$ 8,00 |
| **Milkshake de Chocolate** 🍫 | R$ 12,00 |
| **Milkshake de Morango** �草 | R$ 12,00 |
| **Chá Gelado** ❄️ | R$ 5,50 |

> 💡 **Dica:** Pergunte ao chatbot sobre ingredientes e alergênicos de qualquer item do cardápio!

## 🤖 Como Usar o Chatbot

### Exemplos de Interação:

**Simples:**
- "Oi, quero ver o cardápio"
- "Quanto custa o X-TUDO?"
- "Vocês entregam?"

**Múltiplas Intenções:**
- "Oi, quero ver o cardápio e saber os preços" *(detecta 3 intenções)*
- "Valeu pelo atendimento, tchau!" *(detecta 2 intenções)*

**Consulta de Ingredientes (Nova Funcionalidade!):**
- "Quais os ingredientes do X-Bacon?"
- "Me fala a receita do Hambúrguer"
- "O que tem no Milkshake?"
- "Tem alergênicos no X-Tudo?"

> 🆕 **Integração com IA:** Ao perguntar sobre ingredientes, o chatbot consulta a **API Deepseek R1** (via OpenRouter) que retorna os ingredientes em formato JSON estruturado, incluindo quantidades e identificação de alergênicos.

### Configurações Avançadas:
- **Modo Híbrido**: Usa classificador + busca por similaridade
- **Apenas Classificador**: Usa apenas machine learning
- **Apenas Retrieval**: Usa apenas busca por similaridade
- **Ajuste de Confiança**: Sliders para fine-tuning

## 🎛️ Menu Lateral (Sidebar)

O chatbot possui um menu lateral com várias configurações e informações:

### 📊 Estatísticas da Base de Dados
Exibe informações sobre a base de conhecimento:
- **11 intenções implementadas:**
  1. 👋 **greeting** - Cumprimentos e saudações
  2. 👋 **goodbye** - Despedidas
  3. 🙏 **thanks** - Agradecimentos
  4. 📋 **menu** - Consulta ao cardápio
  5. 💰 **prices** - Consulta de preços
  6. 🛒 **purchase** - Realização de pedidos
  7. 🚚 **delivery_time** - Tempo de entrega
  8. 🕐 **hours** - Horário de funcionamento
  9. 😠 **complaint** - Reclamações
  10. 🍔 **ingredientes** - Consulta de ingredientes/receitas (com IA)
  11. ❓ **fallback** - Mensagens não compreendidas
- Total de exemplos de frases (500+)
- Total de respostas disponíveis

### ⚙️ Configurações do Sistema
Permite ajustar o comportamento do chatbot:

**Modo de Operação:**
- 🔄 **Híbrido (Recomendado)**: Combina classificador ML e busca por similaridade
- 🎯 **Apenas Classificador**: Usa somente o modelo de ML treinado
- 🔍 **Apenas Retrieval**: Usa somente busca por similaridade textual

**Limiares de Confiança:**
- **Classificador (0.0 - 1.0)**: Ajusta sensibilidade do modelo ML
- **Retrieval (0.0 - 1.0)**: Ajusta similaridade mínima para aceitar resultados

### 🤖 Integração API Deepseek
Informações sobre a integração com IA generativa:
- ✅ API Deepseek R1 via OpenRouter
- ✅ Retry automático (5 tentativas)
- ✅ Cache local de respostas
- ✅ Timeout: 30s por requisição

### 🧹 Limpar Cache de Ingredientes
Botão para limpar o cache local de receitas consultadas.

**O que faz:**
- Remove todas as receitas armazenadas em memória
- Próximas consultas farão novas requisições à API
- Útil para testar mudanças ou atualizar informações

**Quando usar:**
- Após mudanças na API ou configurações
- Para forçar consultas frescas da IA
- Para liberar memória (em sessões longas)

## 🧠 Agent Configurado para JSON

### Como funciona a Integração com Deepseek

Quando o usuário pergunta sobre ingredientes, o sistema:

1. **Detecta a Intenção** "ingredientes" usando ML/NLP
2. **Extrai o Prato** mencionado na pergunta
3. **Consulta a API Deepseek** com um prompt estruturado
4. **Recebe JSON** com ingredientes, quantidades e alergênicos

### Estrutura do Prompt Agent

O chatbot envia um **prompt otimizado** para a IA:

```
# Contextualização
Você é um chef de cozinha da região metropolitana de São Paulo Brasil 
e trabalha numa hamburgueria renomada.

# Tarefa
Passe os ingredientes da receita do [PRATO] que você faz, 
incluindo informações sobre os possíveis alergênicos.

# Formato da resposta
Responda no seguinte formato JSON:
{
  "ingredientes": [
    {
      "nome": "nome do ingrediente",
      "quantidade": "quantidade do ingrediente",
      "unidade": "unidade de medida",
      "alergenico": true/false
    }
  ]
}
```

### Exemplo de Resposta da API

```json
{
  "ingredientes": [
    {
      "nome": "Pão de Hambúrguer",
      "quantidade": "1",
      "unidade": "unidade",
      "alergenico": true
    },
    {
      "nome": "Hambúrguer Bovino",
      "quantidade": "150",
      "unidade": "gramas",
      "alergenico": false
    },
    {
      "nome": "Queijo Cheddar",
      "quantidade": "2",
      "unidade": "fatias",
      "alergenico": true
    }
  ]
}
```

### Tratamento de Erros e Resiliência

**Retry com Backoff Exponencial:**
- 5 tentativas automáticas
- Espera entre tentativas: 10s, 20s, 40s, 80s, 160s
- Total de ~4 minutos antes de desistir

**Fallback Inteligente:**
- Receitas pré-cadastradas para itens principais
- Mensagens claras em caso de erro
- Cache local para evitar requisições repetidas

**Tratamento de Rate Limits:**
- Detecta HTTP 429 (rate limit)
- Aguarda automaticamente antes de retentar
- Exibe feedback visual ao usuário

## 📊 Análise Técnica

O sistema fornece análise detalhada:
- **Intenções Detectadas** com percentual de confiança
- **Método Utilizado** (Classificador/Retrieval/Keyword/API)
- **Segmento Analisado** da frase
- **Texto Normalizado** vs Original
- **Visualização JSON** para respostas de ingredientes (expandível/colapsável)

## 🏢 Horários de Funcionamento
- **Terça a Domingo**: 18h00 - 00h00
- **Delivery**: Até 23h30
- **Segunda-feira**: Fechado (manutenção)

## 🎨 Visual Theme

Interface com tema **gótico/rock**:
- Fundo preto estrelado
- Fonte medieval (MedievalSharp)
- Cores: vermelho sangue, roxo, branco
- Emojis temáticos (🤘, 🎸, 💀, 🔥)

## 🔧 Troubleshooting

### Erro: "streamlit não reconhecido"
**Solução**: Use `python -m streamlit run app.py`

### Erro: API Deepseek não responde
**Possíveis causas:**
- API key inválida ou expirada
- Rate limit atingido (muitas requisições)
- Problemas de conectividade

**Soluções:**
1. Verifique se o arquivo `.streamlit/secrets.toml` existe e tem a chave correta
2. Aguarde alguns minutos (rate limit da API gratuita)
3. Teste com o notebook `teste_deepseek_simples.ipynb`
4. Use o botão "Limpar Cache de Ingredientes" na sidebar

### Erro: NLTK Download
**Solução**: Execute manualmente:
```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### Erro: Dependências
**Solução**: Reinstale:
```bash
pip install --upgrade streamlit nltk scikit-learn pandas numpy requests
```

### Cache não limpa
**Solução**: 
1. Use o botão "🧹 Limpar Cache de Ingredientes" na sidebar
2. Ou reinicie o Streamlit (Ctrl+C e execute novamente)

## 📈 Estatísticas da Base de Dados

- **11 Intenções** diferentes (greeting, goodbye, thanks, menu, prices, purchase, delivery_time, hours, complaint, ingredientes, fallback)
- **500+ Exemplos** de frases com variações
- **Suporte a erros** de digitação comuns
- **Múltiplas variações** linguísticas
- **Integração com IA** para ingredientes e receitas
- **Cache inteligente** para otimização de consultas

## 🌐 Deploy em URL Pública

### 🎯 Opção 1: Streamlit Community Cloud (RECOMENDADO - GRATUITO)

1. **Suba para o GitHub:**
```bash
git init
git add .
git commit -m "Initial commit - RockStar Burger Chatbot"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/chatbot-cp2-ia.git
git push -u origin main
```

2. **Acesse [share.streamlit.io](https://share.streamlit.io)**
3. **Conecte com GitHub** e selecione:
   - Repository: `chatbot-cp2-ia`
   - Branch: `main`
   - Main file path: `app.py`
4. **Deploy automático!** 🎉

**URL resultante:** `https://SEU_USUARIO-chatbot-cp2-ia-app-HASH.streamlit.app`

## 🔗 Aplicação publicada na Web.

A aplicação já está publicada no Streamlit Community Cloud e pode ser acessada publicamente neste link:

- https://chatbot-cp3-ia-pfgsp5rgufdusxows5akmq.streamlit.app/

![image](/images/chatbot-01.png)

### 🚂 Opção 2: Railway (FÁCIL - GRATUITO)

1. Acesse [railway.app](https://railway.app)
2. Conecte com GitHub
3. Selecione seu repositório
4. Deploy automático!

### ☁️ Opção 3: Google Cloud Run / Heroku

Consulte documentação específica para essas plataformas.

## 🤝 Contribuição

Para contribuir:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Adicione novos exemplos em `intents_database.json`
4. Teste no chatbot
5. Envie um pull request

## 📜 Licença

Este projeto é educacional e foi desenvolvido como parte do curso de Inteligência Artificial da FIAP.

---

**🤘 Keep on rockin' and enjoy your burger! 🍔**