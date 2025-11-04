# Integração Deepseek - Intenção Ingredientes

## Visão Geral
O chatbot RockStar Burger agora possui integração com a API Deepseek para consultar ingredientes e receitas dos lanches do cardápio.

## Como Funciona

### Detecção Automática
Quando você menciona palavras-chave relacionadas a ingredientes na sua mensagem, o chatbot automaticamente identifica a intenção:
- "ingredientes"
- "o que tem no prato"
- "receita do lanche"
- "composição"
- "o que leva"

### Fluxos de Uso

#### 1. Mencionando o prato diretamente
Exemplo: "Quais são os ingredientes do X-Bacon?"
- O chatbot detecta automaticamente o prato mencionado (X-Bacon)
- Consulta a API Deepseek
- Exibe a lista de ingredientes

#### 2. Pergunta genérica sobre ingredientes
Exemplo: "Me mostre os ingredientes"
- O chatbot exibe uma lista suspensa com todos os pratos disponíveis
- Você seleciona o prato desejado
- Clica no botão "🔍 Buscar Ingredientes"
- Os ingredientes são consultados e exibidos

## Pratos Disponíveis
- Hambúrguer
- X-Burger
- X-Salada
- X-Bacon
- X-Egg
- X-Calabresa
- X-Frango
- X-Tudo
- Vegetariano

## Configuração da API Key

### Localização
A chave da API está armazenada em `.streamlit/secrets.toml` (já configurado e protegido pelo `.gitignore`).

### Formato do arquivo
```toml
[deepseek]
api_key = "sua-chave-aqui"
```

### Como obter a chave
1. Acesse https://openrouter.ai
2. Crie uma conta ou faça login
3. Navegue até "API Keys" no dashboard
4. Gere uma nova chave
5. Copie a chave e cole no arquivo `secrets.toml`

## Endpoint e Modelo
- **Endpoint:** `https://openrouter.ai/api/v1/chat/completions`
- **Modelo:** `deepseek/deepseek-r1:free`
- **Provider:** OpenRouter (roteador para Deepseek)

## Segurança
- ✅ A chave está em `.streamlit/secrets.toml` (ignorado pelo Git)
- ✅ Nunca exponha a chave em código ou commits
- ✅ Rotacione a chave periodicamente

## Tratamento de Erros
O sistema possui tratamento robusto de erros:
- Requisições com timeout de 20 segundos
- Mensagens amigáveis em caso de falha na API
- Fallback para mensagens padrão se a API estiver indisponível

## Exemplo de Uso Completo

```
Você: Quais ingredientes tem no X-Tudo?

Bot: [Consultando receita de X-Tudo...]

Bot: Ingredientes para X-Tudo:
- Pão de hambúrguer: 1 unidade
- Carne bovina: 150g
- Queijo: 2 fatias
- Presunto: 2 fatias
- Ovo: 1 unidade
- Bacon: 3 tiras
- Alface: 2 folhas
- Tomate: 3 rodelas
- Milho: 2 colheres de sopa
- Ervilha: 2 colheres de sopa
- Maionese: a gosto
```

## Testes
Para testar a integração:

1. Inicie o Streamlit:
```powershell
streamlit run app.py
```

2. Digite uma das seguintes mensagens:
   - "Quais são os ingredientes do Hambúrguer?"
   - "Me mostra a receita do X-Bacon"
   - "O que tem no Vegetariano?"
   - "Ingredientes" (e depois selecione o prato)

## Próximos Passos (Opcional)
- [ ] Adicionar cache para respostas da API (evitar consultas repetidas)
- [ ] Implementar rate limiting local
- [ ] Adicionar suporte a múltiplos idiomas
- [ ] Armazenar histórico de consultas
