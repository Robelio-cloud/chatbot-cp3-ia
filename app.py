import streamlit as st
import re
import string
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.metrics.pairwise import cosine_similarity
import json
from datetime import datetime
from pathlib import Path
import unicodedata
import requests
st.markdown("""
    <style>
        /* Importa uma fonte gótica do Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=MedievalSharp&display=swap');

        /* Fundo preto com estrelas brancas */
        .stApp {
            background-color: #000000;
            background-image:
                radial-gradient(white, rgba(255,255,255,.2) 2px, transparent 40px),
                radial-gradient(white, rgba(255,255,255,.15) 1px, transparent 30px),
                radial-gradient(white, rgba(255,255,255,.1) 2px, transparent 40px),
                radial-gradient(rgba(255,255,255,.4), rgba(255,255,255,.1) 2px, transparent 30px);
            background-size: 550px 550px, 350px 350px, 250px 250px, 150px 150px;
            background-position: 0 0, 40px 60px, 130px 270px, 70px 100px;
            color: #FFFFFF;
        }

        /* Título Principal */
        .rockstar-title {
            font-family: 'MedievalSharp', cursive;
            font-size: 4.5em;
            color: #E50000; /* Vermelho Sangue */
            font-weight: bold;
            text-align: center;
            text-shadow: 2px 2px 4px #000000;
            margin-bottom: 0.2em;
        }
        
        /* Personalizar botão primary para cor roxa escura */
        .stButton > button[kind="primary"] {
            background-color: #4B0082 !important; /* Roxo Indigo */
            border: 2px solid #E50000 !important;
            color: white !important;
            font-weight: bold;
        }
        
        .stButton > button[kind="primary"]:hover {
            background-color: #8B008B !important; /* Magenta Escuro */
            border-color: #FF4500 !important;
        }
        
        /* Container das respostas do chatbot */
        .chatbot-response {
            background-color: #1a1a1a;
            color: #ffffff;
            padding: 15px;
            border-radius: 10px;
            border-left: 5px solid #E50000;
            margin: 10px 0;
            word-wrap: break-word;
        }
        
        /* Muda a cor dos cabeçalhos (h1, h2, h3) */
        h1, h2, h3 {
            color: #E50000 !important;
        }
        
        /* Muda a cor do texto do slider */
        .stSlider [data-baseweb="slider"] {
             color: #FFFFFF !important;
        }

    </style>
    <div class="rockstar-title">RockStar Burger</div>
""", unsafe_allow_html=True)
# --- Fim do bloco visual ---

# Carrega intents do arquivo `intents_database.json` para permitir atualizações dinâmicas do menu
try:
    intents_path = Path(__file__).resolve().parent / "intents_database.json"
    with open(intents_path, 'r', encoding='utf-8') as f:
        intents_blob = json.load(f)
        intents = intents_blob.get('intents', {})
except Exception as e:
    # Se falhar ao carregar, definimos um fallback mínimo para manter a aplicação funcionando
    st.error(f"Aviso: não foi possível carregar 'intents_database.json' — usando intents padrão. Erro: {e}")
    intents = {
        "greeting": {"examples": ["oi"], "responses": ["E aí! Bem-vindo ao RockStar Burger!"]},
        "menu": {"examples": ["menu"], "responses": ["Hambúrguer - R$ 20,00\nX-Burger - R$ 23,00"]},
        "purchase": {"examples": ["quero pedir"], "responses": ["O que você quer pedir?"]},
        "prices": {"examples": ["preço"], "responses": ["Hambúrguer: R$ 20,00"]},
        "fallback": {"examples": [], "responses": ["Desculpe, não entendi. Pode repetir?"]}
    }


def parse_menu_from_intents(intents_blob):
    """Tenta extrair lanches e bebidas das respostas do intent 'menu'.

    Retorna dict: {'lanches': [(nome, preco_str), ...], 'bebidas': [...]}.
    """
    menu = {'lanches': [], 'bebidas': []}
    seen = {'lanches': set(), 'bebidas': set()}
    try:
        responses = intents_blob.get('menu', {}).get('responses', [])
        if not responses:
            responses = intents_blob.get('prices', {}).get('responses', [])

        for resp in responses:
            # Divide texto em duas seções: antes de 'BEBIDAS' e depois (caso apareça no meio da string)
            parts = re.split(r'\bBEBIDAS?[:\s]*', resp, flags=re.IGNORECASE)
            lanche_part = parts[0]
            bebida_part = parts[1] if len(parts) > 1 else ''

            def extract_items(section_text):
                items = []
                # quebra por linhas e também por vírgulas (para formatos compactos)
                candidates = []
                for line in section_text.splitlines():
                    line = line.strip()
                    if not line:
                        continue
                    # Se a linha contém vários itens separados por vírgula, separa
                    if ',' in line and 'R$' in line:
                        parts_line = [p.strip() for p in re.split(r',|;|\n', line) if p.strip()]
                        candidates.extend(parts_line)
                    else:
                        candidates.append(line)

                for part in candidates:
                    # Remove marcadores comuns
                    part = re.sub(r'^[•\-*\s]+', '', part)

                    # Tenta vários padrões previsíveis
                    m = re.match(r'(.+?)\s*[-–—:]\s*R\$\s*([\d.,]+)', part)
                    if m:
                        name = m.group(1).strip()
                        price = m.group(2).strip()
                        items.append((name, price))
                        continue

                    m2 = re.match(r'(.+?)\s*\(\s*R\$\s*([\d.,]+)\s*\)', part)
                    if m2:
                        name = m2.group(1).strip()
                        price = m2.group(2).strip()
                        items.append((name, price))
                        continue

                    # Caso haja 'R$' em qualquer lugar, tenta extrair que vem antes e depois
                    if 'R$' in part:
                        try:
                            left, right = part.split('R$', 1)
                            name = left.replace('—', '').replace('-', '').strip(' :•')
                            price = re.search(r'([\d.,]+)', right)
                            if price:
                                items.append((name, price.group(1).strip()))
                                continue
                        except Exception:
                            pass

                return items

            # Extrai lanches e bebidas separadamente
            lanches_found = extract_items(lanche_part)
            bebidas_found = extract_items(bebida_part)

            # Se não encontrou bebidas na segunda parte, tenta procurar na primeira parte por padrões inline
            if not bebidas_found:
                # procura por 'BEBIDAS:' inline na lanche_part (após uma vírgula)
                inline = re.search(r'BEBIDAS?[:\s]*(.*)$', resp, flags=re.IGNORECASE)
                if inline:
                    bebidas_found = extract_items(inline.group(1))

            # adiciona sem duplicatas
            for name, price in lanches_found:
                key = name.lower()
                if key not in seen['lanches']:
                    menu['lanches'].append((name, price))
                    seen['lanches'].add(key)

            for name, price in bebidas_found:
                key = name.lower()
                if key not in seen['bebidas']:
                    menu['bebidas'].append((name, price))
                    seen['bebidas'].add(key)

        return menu
    except Exception:
        return menu


# Prepara menu extraído para uso na interface
# Tenta carregar um menu estruturado em `menu.json` (preferência). Se não houver, usa o parser das intents.
try:
    menu_json_path = Path(__file__).resolve().parent / "menu.json"
    if menu_json_path.exists():
        with open(menu_json_path, 'r', encoding='utf-8') as mf:
            MENU_DATA = json.load(mf)
    else:
        MENU_DATA = parse_menu_from_intents(intents)
except Exception:
    MENU_DATA = parse_menu_from_intents(intents)


def build_prices_response(query=None):
    """Gera uma string de preços com base em MENU_DATA.
    Se a query mencionar bebidas, retorna somente bebidas; se mencionar lanches, retorna somente lanches;
    caso contrário, retorna ambos.
    """
    try:
        q = (query or '').lower()
        lanches = MENU_DATA.get('lanches', [])
        bebidas = MENU_DATA.get('bebidas', [])

        # palavras-chave simples para identificar se o usuário está perguntando sobre bebidas
        bebida_keywords = ['refrigerante', 'água', 'agua', 'suco', 'cerveja', 'milkshake', 'chá', 'cha', 'bebida', 'bebidas']
        lanche_keywords = ['hambúrguer', 'hamburguer', 'hamburgueres', 'lanche', 'lanches', 'x-burger', 'x-bacon', 'x-salada', 'x-tudo', 'vegetariano']

        wants_bebida = any(k in q for k in bebida_keywords)
        wants_lanche = any(k in q for k in lanche_keywords)

        def iter_items(coll):
            # Normaliza cada item para (name, price)
            for itm in coll:
                if isinstance(itm, dict):
                    yield itm.get('name', '').strip(), itm.get('price', '').strip()
                elif isinstance(itm, (list, tuple)) and len(itm) >= 2:
                    yield str(itm[0]).strip(), str(itm[1]).strip()
                elif isinstance(itm, str):
                    # tenta extrair "Nome - R$ 12,00" ou "Nome (R$ 12,00)"
                    s = itm.strip()
                    m = re.match(r'(.+?)\s*[-–—:]\s*R\$\s*([\d.,]+)', s)
                    if m:
                        yield m.group(1).strip(), m.group(2).strip()
                    else:
                        m2 = re.match(r'(.+?)\s*\(\s*R\$\s*([\d.,]+)\s*\)', s)
                        if m2:
                            yield m2.group(1).strip(), m2.group(2).strip()
                        else:
                            # fallback: nome inteiro, preço vazio
                            yield s, ''

        # normalize query tokens (without stopwords) to try to detect specific items
        q_norm = normalize_text(query or '')
        tokens = [t for t in q_norm.split() if t]
        
        # Remove generic words that don't identify specific menu items
        # Inclui palavras de consulta de preço para que queries genéricas como "quanto custa o lanche" retornem o menu completo
        generic_words = [
            'lanche', 'lanches', 'hamburguer', 'hamburgueres', 'bebida', 'bebidas', 
            'item', 'itens', 'produto', 'produtos',
            'quanto', 'custa', 'vale', 'preço', 'preco', 'valor', 'valo', 
            'qual', 'quais', 'e', 'eh', 'é', 'o', 'a', 'os', 'as', 'do', 'da', 'dos', 'das'
        ]
        tokens = [t for t in tokens if t not in generic_words]

        def normalize_plain(s: str) -> str:
            return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode().lower()

        # build searchable map of menu item normalized names -> (name, price)
        menu_index = []
        for name, price in list(iter_items(lanches)) + list(iter_items(bebidas)):
            menu_index.append((normalize_plain(name), name, price))

        # find explicit matches from tokens
        explicit_matches = []
        if tokens:
            for tok in tokens:
                for n_norm, name, price in menu_index:
                    if tok in n_norm:
                        explicit_matches.append((name, price))

        # If tokens is empty (generic query), return full menu
        # If user mentioned specific items but none match the menu, respond that we don't serve it
        if not tokens:
            # Generic query like "quanto custa o lanche" -> return full menu
            pass  # Will fall through to return full menu below
        elif tokens and not explicit_matches:
            # Build simplified menu summary: all lanches + Refrigerante (lata) if present
            lanches_names = [name for name, _ in list(iter_items(lanches))]
            bebida_names = [name for name, _ in list(iter_items(bebidas))]
            # Prefer a beverage named 'refrigerante' if present
            selected_beb = None
            for b in bebida_names:
                if 'refrigerante' in b.lower():
                    selected_beb = b
                    break
            if not selected_beb and bebida_names:
                selected_beb = bebida_names[0]

            if selected_beb:
                lanches_names.append(selected_beb)

            summary = ', '.join(lanches_names)
            return f"Desculpe, não servimos isso. Nosso cardápio tem: {summary}."

        lines = []
        
        # If we have explicit matches, show only those
        if explicit_matches:
            lines.append('Preços encontrados:')
            for name, price in explicit_matches:
                if price:
                    lines.append(f"{name}: R$ {price}")
                else:
                    lines.append(f"{name}")
        else:
            # Show full menu (lanches and/or bebidas based on query)
            if wants_lanche or (not wants_bebida and not wants_lanche):
                items = list(iter_items(lanches))
                if items:
                    lines.append('Preços dos lanches:')
                    for name, price in items:
                        if price:
                            lines.append(f"{name}: R$ {price}")
                        else:
                            lines.append(f"{name}")
                    lines.append('')

            if wants_bebida or (not wants_bebida and not wants_lanche):
                items = list(iter_items(bebidas))
                if items:
                    lines.append('Preços das bebidas:')
                    for name, price in items:
                        if price:
                            lines.append(f"{name}: R$ {price}")
                        else:
                            lines.append(f"{name}")

        if not lines:
            # fallback para quando MENU_DATA estiver vazio
            return np.random.choice(intents.get('prices', {}).get('responses', ["Desculpe, não tenho os preços agora."]))

        # Use <br> so HTML rendering preserves line breaks inside the chatbot-response div
        return '<br>'.join(lines)
    except Exception:
        return np.random.choice(intents.get('prices', {}).get('responses', ["Desculpe, não tenho os preços agora."]))


# --- Integração Deepseek para intenção "ingredientes" ---
PRATOS = [
    "Hambúrguer", "X-Burger", "X-Salada", "X-Bacon", "X-Egg",
    "X-Calabresa", "X-Frango", "X-Tudo", "Vegetariano"
]

# Receitas pré-cadastradas (fallback quando API não está disponível)
RECEITAS_PRECADASTRADAS = {
    "hambúrguer": """**Ingredientes do Hambúrguer:**
• 1 pão de hambúrguer (contém glúten)
• 1 hambúrguer bovino (150g)
• Queijo cheddar (1 fatia) - **ALERGÊNICO: Leite**
• Alface
• Tomate (2 rodelas)
• Cebola (2 rodelas)
• Molho especial da casa (contém ovos) - **ALERGÊNICO: Ovos**""",
    
    "x-burger": """**Ingredientes do X-Burger:**
• 1 pão de hambúrguer (contém glúten) - **ALERGÊNICO: Trigo**
• 1 hambúrguer bovino (150g)
• 2 fatias de queijo cheddar - **ALERGÊNICO: Leite**
• Alface
• Tomate (3 rodelas)
• Cebola roxa (2 rodelas)
• Picles
• Molho especial da casa - **ALERGÊNICO: Ovos**""",
    
    "x-bacon": """**Ingredientes do X-Bacon:**
• 1 pão de hambúrguer (contém glúten) - **ALERGÊNICO: Trigo**
• 1 hambúrguer bovino (150g)
• 3 fatias de bacon crocante
• 2 fatias de queijo cheddar - **ALERGÊNICO: Leite**
• Alface
• Tomate (2 rodelas)
• Cebola caramelizada
• Molho barbecue""",
    
    "x-salada": """**Ingredientes do X-Salada:**
• 1 pão de hambúrguer (contém glúten) - **ALERGÊNICO: Trigo**
• 1 hambúrguer bovino (150g)
• Queijo mussarela (2 fatias) - **ALERGÊNICO: Leite**
• Alface (porção generosa)
• Tomate (4 rodelas)
• Cebola (2 rodelas)
• Cenoura ralada
• Milho
• Maionese - **ALERGÊNICO: Ovos**""",
    
    "x-tudo": """**Ingredientes do X-Tudo:**
• 1 pão de hambúrguer especial (contém glúten) - **ALERGÊNICO: Trigo**
• 2 hambúrgueres bovinos (150g cada)
• 4 fatias de queijo cheddar - **ALERGÊNICO: Leite**
• 4 fatias de bacon
• 1 ovo frito - **ALERGÊNICO: Ovos**
• Presunto (2 fatias)
• Calabresa fatiada
• Alface, tomate, cebola
• Milho, ervilha, batata palha
• Molhos especiais (maionese, ketchup, mostarda) - **ALERGÊNICO: Ovos (maionese)**""",
    
    "vegetariano": """**Ingredientes do Vegetariano:**
• 1 pão integral (contém glúten) - **ALERGÊNICO: Trigo**
• 1 hambúrguer vegetariano (grão de bico e quinoa)
• 2 fatias de queijo vegano (sem lactose)
• Alface roxa
• Tomate (3 rodelas)
• Cebola roxa grelhada
• Cogumelos salteados
• Rúcula
• Molho de iogurte vegetal (ou veganaise)
• Azeite e ervas

*Opção vegana disponível sem queijo*""",
    
    "refrigerante": """**Ingredientes/Composição do Refrigerante:**
• Água gaseificada
• Açúcar ou adoçante (dependendo da versão)
• Concentrado de frutas ou saborizantes artificiais
• Acidulante (ácido cítrico)
• Conservantes
• Corante caramelo

*Disponível em versões: Coca-Cola, Guaraná, Fanta, Sprite*
*Opções: Normal ou Zero*""",
    
    "suco natural": """**Ingredientes do Suco Natural:**
• Frutas frescas da estação (laranja, limão, morango, maracujá)
• Água filtrada
• Açúcar ou mel (opcional)
• Gelo

*100% natural, sem conservantes ou corantes artificiais*
*Consulte sabores disponíveis no dia*""",
    
    "milkshake": """**Ingredientes do Milkshake:**
• Sorvete de creme (500ml) - **ALERGÊNICO: Leite**
• Leite integral (200ml) - **ALERGÊNICO: Leite**
• Calda de chocolate, morango ou baunilha
• Chantilly - **ALERGÊNICO: Leite**
• Cobertura especial

*Sabores disponíveis: Chocolate, Morango, Baunilha, Ovomaltine*
**⚠️ CONTÉM LACTOSE**"""
}

INTENT_INGREDIENTES_KEYWORDS = [
    "ingredientes", "ingrediente", "receita", "composição", "o que tem no", "o que leva",
    "como é feito", "como fazer", "modo de preparo", "lista de ingredientes",
    "o que vai no", "o q vai no", "oq vai no", "que vai no", "qual ingrediente"
]

def detect_ingredientes_intent(text: str) -> bool:
    """Detecta se a query solicita informações sobre ingredientes/receita.
    Evita falsos positivos checando se é realmente sobre ingredientes,
    não apenas mencionando um prato.
    """
    txt = (text or '').lower()
    
    # Palavras que indicam perguntas sobre PREÇO ou PEDIDO (NÃO ingredientes)
    palavras_nao_ingredientes = [
        "quanto custa", "quanto é", "quanto vai ficar", "quanto fica", "qual o preço",
        "qual o valor", "preço", "valor", "custa", "vai ficar",
        "quero pedir", "queria pedir", "gostaria de pedir",
        "me traz", "me dá", "pode trazer", "vou querer",
        "quero um ", "quero o ", "quero uma "
    ]
    
    # Se tem pergunta sobre preço/pedido, definitivamente NÃO é sobre ingredientes
    if any(palavra in txt for palavra in palavras_nao_ingredientes):
        # A menos que mencione EXPLICITAMENTE ingredientes/receita junto
        if not any(kw in txt for kw in ["ingredientes", "receita", "composição", "como é feito", "como fazer"]):
            return False
    
    # Verifica se tem alguma palavra-chave de ingredientes
    return any(kw in txt for kw in INTENT_INGREDIENTES_KEYWORDS)

def consulta_deepseek(nome_prato: str, api_key: str, timeout: int = 30, max_retries: int = 5) -> str:
    """Consulta a API Deepseek (via OpenRouter) para obter ingredientes/receita do prato.
    Implementa retry automático com backoff exponencial para rate limits.
    Usa cache local para evitar requisições repetidas.
    Usa receitas pré-cadastradas como fallback quando API não está disponível.
    """
    import time
    import re
    
    # Normaliza o nome do prato para buscar no cache e receitas
    # Remove acentos, hífens, espaços extras
    def normalize_prato_name(name: str) -> str:
        n = name.lower().strip()
        # Remove acentos
        n = unicodedata.normalize('NFKD', n).encode('ASCII', 'ignore').decode()
        # Remove hífens e espaços múltiplos
        n = re.sub(r'[-\s]+', ' ', n).strip()
        return n
    
    cache_key = normalize_prato_name(nome_prato)
    
    # Verifica cache primeiro (apenas para consultas já feitas anteriormente)
    if cache_key in st.session_state.get('ingredientes_cache', {}):
        cached_result = st.session_state['ingredientes_cache'][cache_key]
        return f"{cached_result}\n\n*️⃣ *(Resposta do cache - consulta anterior)*"
    
    # Normaliza as chaves das receitas pré-cadastradas para usar como FALLBACK se API falhar
    receitas_normalized = {normalize_prato_name(k): v for k, v in RECEITAS_PRECADASTRADAS.items()}
    
    # ESTRATÉGIA: SEMPRE tenta API Deepseek PRIMEIRO
    # Receitas pré-cadastradas são usadas APENAS como fallback emergencial se API falhar completamente
    
    # Mostra indicador de que está consultando a API
    with st.spinner(f'🔍 Consultando API Deepseek para obter ingredientes de **{nome_prato}**...'):
        url = 'https://openrouter.ai/api/v1/chat/completions'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        }
        prompt = f"""# Contextualização

Você é um chef de cozinha da região metropolitana de São Paulo Brasil e trabalha numa hamburgueria renomada. Seu restaurante tem ótimas recomendações.

# Tarefa

Passe os ingredientes da receita do {nome_prato} que você faz, incluindo informações sobre os possíveis alergênicos.
Traga informações única e exclusivamente dos ingredientes, sem modo de preparo e outras informações.

# Formato da resposta

Responda no seguinte formato JSON:

{{
  "ingredientes": [
    {{
      "nome": "nome do ingrediente",
      "quantidade": "quantidade do ingrediente",
      "unidade": "unidade de medida",
      "alergenico": true/false
    }}
  ]
}}

# Exemplo de resposta

{{
    "ingredientes": [
        {{
            "nome": "Farinha de Trigo",
            "quantidade": "500",
            "unidade": "gramas",
            "alergenico": true
        }},
        {{
            "nome": "Ovos",
            "quantidade": "3",
            "unidade": "unidades",
            "alergenico": true
        }},
        {{
            "nome": "Açúcar",
            "quantidade": "1",
            "unidade": "xícara",
            "alergenico": false
        }}
    ]
}}"""
    payload = {
        'model': 'deepseek/deepseek-r1:free',
        'messages': [
            {'role': 'user', 'content': prompt}
        ]
    }

    resp = None
    
    for attempt in range(max_retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            # Verifica o status code ANTES de fazer raise
            if resp.status_code == 429:
                # Rate limit - tenta novamente com backoff exponencial mais agressivo
                if attempt < max_retries - 1:
                    # Backoff: 10s, 30s, 60s, 120s (aumentado para evitar rate limits)
                    wait_time = 10 * (2 ** attempt)
                    st.warning(f"⏳ Rate limit detectado. Aguardando {wait_time}s antes de tentar novamente... (tentativa {attempt + 1}/{max_retries})")
                    time.sleep(wait_time)
                    continue  # Tenta novamente
                else:
                    # Após TODAS as tentativas (5x com backoff longo), usa fallback APENAS em último caso
                    if cache_key in receitas_normalized:
                        receita = receitas_normalized[cache_key]
                        # Salva no cache também
                        if 'ingredientes_cache' not in st.session_state:
                            st.session_state['ingredientes_cache'] = {}
                        st.session_state['ingredientes_cache'][cache_key] = receita
                        return f"{receita}\n\n⚠️ *(API Deepseek indisponível após 5 tentativas - usando fallback local)*"
                    else:
                        # Se não tem receita pré-cadastrada, retorna mensagem de erro clara
                        return '❌ **API Deepseek indisponível**\n\nApós 5 tentativas com backoff exponencial (total ~4 minutos), a API continua retornando rate limit 429.\n\n**Possíveis causas:**\n• Limite diário da API gratuita atingido\n• Muitas requisições recentes\n• Serviço temporariamente sobrecarregado\n\n**Soluções:**\n• Aguarde alguns minutos e tente novamente\n• Use uma API key paga (sem rate limits)\n• Verifique o status em: https://openrouter.ai/status'
            elif resp.status_code == 401:
                return '🔑 **API key inválida!**\n\nPor favor, verifique se sua chave está correta no arquivo `.streamlit/secrets.toml`'
            
            # Se não for erro conhecido, faz raise para capturar outros erros HTTP
            resp.raise_for_status()
            # Se chegou aqui, deu certo!
            break
            
        except requests.exceptions.HTTPError as e:
            # Outros erros HTTP que não são 429 ou 401
            return f'❌ **Erro HTTP {resp.status_code if resp else "desconhecido"}:**\n\n{str(e)}'
        except requests.exceptions.RequestException as e:
            return f'🔌 **Erro na conexão:**\n\n{str(e)}'
    
    if not resp:
        return 'Erro: nenhuma resposta recebida da API'

    try:
        j = resp.json()
    except Exception:
        return f'Erro ao decodificar resposta JSON: {resp.text[:200]}'

    # Extrai conteúdo da resposta
    try:
        content = j.get('choices', [{}])[0].get('message', {}).get('content')
    except Exception:
        content = None

    if not content:
        return json.dumps(j, ensure_ascii=False, indent=2)

    # Armazena no cache para requisições futuras
    if 'ingredientes_cache' not in st.session_state:
        st.session_state['ingredientes_cache'] = {}
    st.session_state['ingredientes_cache'][cache_key] = content

    return content

def extract_prato_from_query(query: str) -> str:
    """Tenta extrair o nome do prato mencionado na query.
    Aceita variações como 'x tudo', 'xtudo', 'x-tudo', 'X-TUDO', etc.
    """
    import re
    q_lower = query.lower()
    
    for prato in PRATOS:
        prato_lower = prato.lower()
        
        # 1. Busca exata (com acentos)
        if prato_lower in q_lower:
            return prato
        
        # 2. Busca ignorando hífens e espaços
        # Remove hífens, espaços e underscores
        q_normalized = re.sub(r'[-\s_]', '', q_lower)
        prato_normalized = re.sub(r'[-\s_]', '', prato_lower)
        
        if prato_normalized in q_normalized:
            return prato
        
        # 3. Para lanches que começam com "x-", busca apenas a parte depois do "x"
        if prato_lower.startswith('x-'):
            # Pega a parte depois do "x-" (ex: "bacon", "tudo", "salada")
            parte_principal = prato_lower.split('x-', 1)[1]
            
            # Busca por padrões como "x tudo", "xtudo", "x-tudo"
            # Cria um padrão que aceita variações: x[\s-_]?tudo
            pattern = r'\bx[\s\-_]?' + re.escape(parte_principal) + r'\b'
            if re.search(pattern, q_lower):
                return prato
            
            # Também busca apenas a palavra-chave (ex: só "tudo" → X-Tudo)
            # Mas só se for uma palavra isolada ou no final/início
            if re.search(r'\b' + re.escape(parte_principal) + r'\b', q_lower):
                return prato
        
        # 4. Caso especial: hambúrguer (pode vir sem acento)
        if prato_lower == 'hambúrguer':
            if re.search(r'\bhamburgu?e?r\b', q_lower):
                return prato
    
    return None


# Transformar em dataframe (utterance, intent)
rows = []
for intent, v in intents.items():
    for ex in v["examples"]:
        rows.append({"text": ex, "intent": intent})

df = pd.DataFrame(rows)

# Downloads (apenas na primeira execução) com verificações e fallbacks.
# Tentamos baixar os recursos necessários; se falhar (por exemplo, sem internet),
# o app usa alternativas robustas para não travar em produção.
resource_checks = [
    ('punkt', 'tokenizers/punkt'),
    ('stopwords', 'corpora/stopwords'),
    ('wordnet', 'corpora/wordnet'),
    ('omw-1.4', 'corpora/omw-1.4')
]

have_punkt = False
have_stopwords = False
have_wordnet = False

for name, path in resource_checks:
    try:
        nltk.data.find(path)
        if name == 'punkt':
            have_punkt = True
        if name == 'stopwords':
            have_stopwords = True
        if name in ('wordnet', 'omw-1.4'):
            have_wordnet = True
    except LookupError:
        try:
            # quiet=True evita muita saída no deploy
            nltk.download(name, quiet=True)
            # Re-check
            nltk.data.find(path)
            if name == 'punkt':
                have_punkt = True
            if name == 'stopwords':
                have_stopwords = True
            if name in ('wordnet', 'omw-1.4'):
                have_wordnet = True
        except Exception:
            # Se não for possível baixar, seguimos com fallback
            pass

# Stopwords (fallback vazio / pequeno conjunto se não houver recursos)
if have_stopwords:
    try:
        stop_words = set(stopwords.words('portuguese'))
    except Exception:
        stop_words = set()
else:
    # Um pequeno conjunto de stopwords em português como fallback
    stop_words = set([
        'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'é', 'com', 'não', 'uma',
        'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele'
    ])

# Lemmatizer (só será usado se wordnet estiver disponível)
lemmatizer = None
if have_wordnet:
    try:
        lemmatizer = WordNetLemmatizer()
    except Exception:
        lemmatizer = None


def normalize_text(text):
    text = text.lower()
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text)
    # Tenta usar o tokenizador do NLTK (punkt). Se não estiver disponível,
    # faz um tokenizador simples baseado em regex para evitar crash no deploy.
    try:
        # se punkt não foi encontrado, nltk.word_tokenize lançará LookupError
        tokens = nltk.word_tokenize(text)
    except LookupError:
        tokens = re.findall(r"\b[\w']+\b", text, flags=re.UNICODE)
    tokens = [t for t in tokens if t.isalpha()]
    tokens = [t for t in tokens if t not in stop_words]
    # Aplica lematização apenas se o lemmatizer estiver disponível
    if lemmatizer is not None:
        try:
            tokens = [lemmatizer.lemmatize(t) for t in tokens]
        except Exception:
            # Se algo der errado na lematização, mantemos os tokens originais
            pass
    return ' '.join(tokens)

df['text_norm'] = df['text'].apply(normalize_text)

# Criar vetorizadores
tfidf_vect = TfidfVectorizer()
X_tfidf = tfidf_vect.fit_transform(df['text_norm'])

# Treinar classificador
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(X_tfidf, df['intent'])


def retrieve_response(query, vect=tfidf_vect, utter_vecs=X_tfidf, df=df, threshold=0.6):
    q = normalize_text(query)
    qv = vect.transform([q])
    sims = cosine_similarity(qv, utter_vecs).flatten()
    idx_sorted = np.argsort(-sims)
    if sims[idx_sorted[0]] >= threshold:
        chosen_idx = idx_sorted[0]
        intent = df.iloc[chosen_idx]['intent']
        # Special handling para intent 'prices' — formata os preços com base no MENU_DATA
        if intent == 'prices':
            try:
                resp = build_prices_response(query)
                print(f"DEBUG - build_prices_response retornou: {resp[:200]}...")  # Debug
            except Exception as e:
                print(f"DEBUG - Erro em build_prices_response: {e}")  # Debug
                resp = np.random.choice(intents[intent]['responses'])
        else:
            resp = np.random.choice(intents[intent]['responses'])
        return resp, intent, sims[idx_sorted[0]]
    else:
        return np.random.choice(intents['fallback']['responses']), 'fallback', sims[idx_sorted[0]]

def detect_multiple_intents(query, threshold_clf=0.3, threshold_retrieve=0.3):
    """Detecta múltiplas intenções em uma única frase"""
    import re
    
    # Primeiro, tenta detectar intenções na frase completa
    detected_intents = []
    
    # Verifica greeting no início da frase
    greeting_words = ['oi', 'olá', 'hello', 'hey', 'e aí', 'fala', 'salve', 'bom dia', 'boa tarde', 'boa noite']
    query_lower = query.lower()
    for greeting in greeting_words:
        if query_lower.startswith(greeting) or f' {greeting} ' in query_lower:
            detected_intents.append({
                'intent': 'greeting',
                'confidence': 0.95,
                'method': 'keyword_detection',
                'segment': greeting
            })
            break
    
    # Verifica goodbye no final da frase
    goodbye_words = ['tchau', 'falou', 'bye', 'adeus', 'até mais', 'até logo', 'valeu tchau', 'xau']
    for goodbye in goodbye_words:
        if query_lower.endswith(goodbye) or f' {goodbye}' in query_lower:
            if not any(d['intent'] == 'goodbye' for d in detected_intents):
                detected_intents.append({
                    'intent': 'goodbye',
                    'confidence': 0.95,
                    'method': 'keyword_detection',
                    'segment': goodbye
                })
            break
    
    # Verifica thanks em qualquer lugar
    thanks_words = ['obrigado', 'obrigada', 'valeu', 'brigado', 'grato', 'agradeco', 'thanks']
    for thanks in thanks_words:
        if thanks in query_lower:
            if not any(d['intent'] == 'thanks' for d in detected_intents):
                detected_intents.append({
                    'intent': 'thanks',
                    'confidence': 0.90,
                    'method': 'keyword_detection',
                    'segment': thanks
                })
            break
    
    # Divide a frase em segmentos para detectar outras intenções
    segments = re.split(r'[,.;!?]|\be\b|\stambém\b|\sainda\b|\se\b|\squero\b|\sgostaria\b', query.lower())
    segments = [seg.strip() for seg in segments if seg.strip()]
    
    # Se não há segmentos múltiplos, usa a frase completa
    if len(segments) <= 1:
        segments = [query]
    
    for segment in segments:
        if len(segment.split()) < 2:  # Ignora segmentos muito pequenos
            continue
            
        # Testa classificador
        q_norm = normalize_text(segment)
        if not q_norm:  # Se não há texto normalizado, pula
            continue
            
        qv = tfidf_vect.transform([q_norm])
        probs = clf.predict_proba(qv)[0]
        
        # Pega as top 3 intenções mais prováveis
        top_indices = np.argsort(-probs)[:3]
        
        for idx in top_indices:
            intent = clf.classes_[idx]
            prob = probs[idx]
            
            # Verifica se já foi detectada por keyword
            already_detected = any(d['intent'] == intent for d in detected_intents)
            
            if prob >= threshold_clf and not already_detected:
                detected_intents.append({
                    'intent': intent,
                    'confidence': prob,
                    'method': 'classifier',
                    'segment': segment
                })
                break
        
        # Se não encontrou pelo classificador, tenta retrieval
        if not any(d['segment'] == segment for d in detected_intents if d['method'] in ['classifier', 'retrieval']):
            _, intent_ret, sim = retrieve_response(segment, threshold=threshold_retrieve)
            if intent_ret != 'fallback':
                already_detected = any(d['intent'] == intent_ret for d in detected_intents)
                if not already_detected:
                    detected_intents.append({
                        'intent': intent_ret,
                        'confidence': sim,
                        'method': 'retrieval',
                        'segment': segment
                    })
    
    # Se não detectou nada, usa fallback
    if not detected_intents:
        detected_intents.append({
            'intent': 'fallback',
            'confidence': 0.0,
            'method': 'fallback',
            'segment': query
        })
    
    # Ordena por confiança (maior primeiro)
    detected_intents.sort(key=lambda x: x['confidence'], reverse=True)
    
    return detected_intents

def generate_multi_intent_response(detected_intents):
    """Gera resposta baseada em múltiplas intenções detectadas"""
    import sys
    print("="*50, file=sys.stderr)
    print(f"🎯 INTENTS DETECTADAS ({len(detected_intents)}): {[d['intent'] for d in detected_intents]}", file=sys.stderr)
    print("="*50, file=sys.stderr)
    sys.stderr.flush()
    
    if len(detected_intents) == 1:
        intent_data = detected_intents[0]
        if intent_data['intent'] == 'prices':
            try:
                resp = build_prices_response(intent_data.get('segment'))
                # Se a resposta for a mensagem de erro "não servimos", tenta resposta padrão
                if "não servimos isso" in resp.lower():
                    resp = build_prices_response(None)  # Tenta com query vazia (menu completo)
            except Exception as e:
                # Fallback: retorna resposta do JSON se build_prices_response falhar
                resp = np.random.choice(intents['prices']['responses'])
        else:
            resp = np.random.choice(intents[intent_data['intent']]['responses'])
        return resp, intent_data
    
    # Para múltiplas intenções, cria uma resposta combinada
    response_parts = []
    primary_intent = detected_intents[0]  # A primeira será considerada principal
    
    for intent_data in detected_intents:
        intent = intent_data['intent']
        # Use as respostas definidas no arquivo de intents quando possível
        if intent in intents and 'responses' in intents[intent]:
            try:
                if intent == 'prices':
                    resp_prices = build_prices_response(intent_data.get('segment'))
                    print(f"DEBUG multi - build_prices_response retornou: {resp_prices[:200]}...")  # Debug
                    response_parts.append(resp_prices)
                else:
                    response_parts.append(np.random.choice(intents[intent]['responses']))
            except Exception as e:
                print(f"DEBUG multi - Erro: {e}")  # Debug
                # fallback simples se algo der errado
                response_parts.append(intents[int].get('responses', [''])[0] if intents.get(intent) else '')
        else:
            # Intenção não mapeada no arquivo: usa mensagens curtas padrão
            if intent == 'greeting':
                response_parts.append("Salve, rockstar! 🤘")
            elif intent == 'thanks':
                response_parts.append("Valeu! 🤘")
            elif intent == 'goodbye':
                response_parts.append("Até a próxima! Keep rockin'!")
    
    combined_response = "\n\n".join(response_parts)
    
    if not combined_response:
        combined_response = np.random.choice(intents['fallback']['responses'])
    
    return combined_response, primary_intent

def combined_respond(query, threshold_clf=0.6, threshold_retrieve=0.4):
    # Detecta múltiplas intenções
    detected_intents = detect_multiple_intents(query, threshold_clf * 0.5, threshold_retrieve)
    
    # Gera resposta baseada nas intenções detectadas
    response, primary_intent = generate_multi_intent_response(detected_intents)
    
    return response, detected_intents, primary_intent

# Interface do Streamlit
st.title('💀 Chatbot RockStar Burger 🤘')

# Botão para exibir o menu extraído de `intents_database.json`
st.markdown("### 🍽️ Cardápio")
if st.button("Ver Menu"):
    st.markdown("---")
    lanches = MENU_DATA.get('lanches', [])
    bebidas = MENU_DATA.get('bebidas', [])

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Lanches")
        if lanches:
            # lanches é uma lista de dicts (name, price) ou tuplas (name, price)
            df_lanches = pd.DataFrame([
                (i+1, itm['name'] if isinstance(itm, dict) else itm[0], itm['price'] if isinstance(itm, dict) else itm[1])
                for i, itm in enumerate(lanches)
            ], columns=['No.', 'Item', 'Preço'])
            df_lanches['Preço'] = df_lanches['Preço'].apply(lambda p: f"R$ {p}")
            st.table(df_lanches)
        else:
            st.info("Nenhum lanche encontrado no menu.")

    with col2:
        st.subheader("Bebidas")
        if bebidas:
            df_bebidas = pd.DataFrame([
                (i+1, itm['name'] if isinstance(itm, dict) else itm[0], itm['price'] if isinstance(itm, dict) else itm[1])
                for i, itm in enumerate(bebidas)
            ], columns=['No.', 'Item', 'Preço'])
            df_bebidas['Preço'] = df_bebidas['Preço'].apply(lambda p: f"R$ {p}")
            st.table(df_bebidas)
        else:
            st.info("Nenhuma bebida encontrada no menu.")

# Sidebar com informações
# NOTA: A API do Streamlit posiciona a sidebar sempre à esquerda.
st.sidebar.markdown("""
### ✝️ Funcionalidades do Palco ✝️
- **Intenções suportadas:**
  - 😇 Cumprimentos e Despedidas
  - 🛒 Pedidos de Burgers
  - 🐍 Cardápio e Preços
  - 🐺 Horários de Funcionamento
  - 🦇 Tempo de Entrega
  - ☮️ Agradecimentos
  - 😈 Reclamações
  - 🔥 Ingredientes (com IA)
  
- **Tecnologias:**
  - TF-IDF Vectorization
  - Logistic Regression Classifier
  - Cosine Similarity Retrieval
""")

# Configurações avançadas
st.sidebar.markdown("### ⚙️ Ajuste o Som")
mode = st.sidebar.selectbox(
    'Modo de Operação:',  
    ['🔄 Híbrido (Recomendado)', '🎯 Apenas Classificador', '🔍 Apenas Retrieval'],
    help="Escolha como o chatbot deve processar as mensagens"
)

# Sliders de confiança na vertical
st.sidebar.markdown("### 🎚️ Níveis de Confiança")
if mode == '🔄 Híbrido (Recomendado)':
    threshold_clf = st.sidebar.slider('Confiança Classificador 🧠', 0.0, 1.0, 0.6, 0.05)
    threshold_ret = st.sidebar.slider('Confiança Similaridade 🔍', 0.0, 1.0, 0.4, 0.05)
elif mode == '🎯 Apenas Classificador':
    threshold_clf = st.sidebar.slider('Confiança Classificador 🧠', 0.0, 1.0, 0.5, 0.05)
    threshold_ret = 0.0
else:  # Retrieval only
    threshold_clf = 1.0
    threshold_ret = st.sidebar.slider('Confiança Similaridade 🔍', 0.0, 1.0, 0.6, 0.05)

# Gerenciamento de cache de ingredientes
st.sidebar.markdown("---")
st.sidebar.markdown("### 🗑️ Cache de Ingredientes")
cache_size = len(st.session_state.get('ingredientes_cache', {}))
st.sidebar.info(f"📦 Pratos em cache: {cache_size}")

# Toggle para usar ou não receitas pré-cadastradas
st.sidebar.markdown("---")
st.sidebar.markdown("### 🤖 Integração API Deepseek")

st.sidebar.info("""
**Status da integração:**
✅ API Deepseek R1 via OpenRouter  
✅ Retry automático com backoff exponencial (5 tentativas)  
✅ Cache local de respostas  
✅ Timeout: 30s por requisição
""")

if st.sidebar.button("🧹 Limpar Cache de Ingredientes", help="Remove todas as receitas armazenadas em cache"):
    if 'ingredientes_cache' in st.session_state:
        num_cached = len(st.session_state['ingredientes_cache'])
        st.session_state['ingredientes_cache'] = {}
        st.sidebar.success(f"✅ {num_cached} receita(s) removida(s) do cache!")
    else:
        st.sidebar.info("Cache já está vazio!")

# Input do usuário
st.markdown("### 💬 Mande seu recado para a banda")

# usamos session_state para permitir que botões 'Pedir' preencham o campo
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

# Cache de ingredientes para evitar rate limits da API
if 'ingredientes_cache' not in st.session_state:
    st.session_state['ingredientes_cache'] = {}

user_input = st.text_area(
    "Digite sua mensagem:",  
    height=100,
    placeholder="Ex: E aí! Quero um Master of Burgers. Quanto tempo demora?",
    key='user_input'
)

# Estado para menu de ingredientes
if 'show_ingredientes_menu' not in st.session_state:
    st.session_state['show_ingredientes_menu'] = False
if 'last_user_input' not in st.session_state:
    st.session_state['last_user_input'] = ''

# Botão de envio
if st.button("🎸 Enviar Mensagem", type="primary"):
    if user_input:
        # Verifica primeiro se é uma intenção de ingredientes
        if detect_ingredientes_intent(user_input):
            st.session_state['show_ingredientes_menu'] = True
            st.session_state['last_user_input'] = user_input
            st.rerun()
        elif False:  # Placeholder para manter estrutura
            # Fluxo especial para ingredientes
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**👤 Você disse:**")
            with col2:
                st.info(user_input)
            
            st.markdown("**🤖 RockStar Burger responde:**")
            st.markdown('<div class="chatbot-response">Beleza! 🎸 Escolha o lanche que você quer saber os ingredientes:</div>', unsafe_allow_html=True)
            
            # Grade de botões com os pratos
            st.markdown("### 🍔 Nossos Lanches:")
            cols = st.columns(3)
            for idx, prato in enumerate(PRATOS):
                with cols[idx % 3]:
                    if st.button(f"� {prato}", key=f"ing_{prato}", use_container_width=True):
                        with st.spinner(f'Consultando receita de {prato}... 🔥'):
                            try:
                                import json
                                api_key = st.secrets["deepseek"]["api_key"]
                                resultado = consulta_deepseek(prato, api_key)
                                st.markdown(f'<div class="chatbot-response"><strong>🍔 Ingredientes para {prato}:</strong></div>', unsafe_allow_html=True)
                                
                                # Tenta parsear como JSON para exibição estruturada
                                try:
                                    # Remove possíveis marcadores de cache/mensagens
                                    resultado_limpo = resultado.split('\n\n*️⃣')[0].split('\n\n📋')[0].strip()
                                    dados_json = json.loads(resultado_limpo)
                                    st.json(dados_json, expanded=True)
                                except:
                                    # Se não for JSON válido, exibe como código
                                    st.code(resultado, language='json', line_numbers=False)
                            except Exception as e:
                                st.error(f"Erro ao consultar ingredientes: {e}")
                                st.markdown('<div class="chatbot-response">Desculpe, não consegui buscar os ingredientes no momento. Tente novamente mais tarde.</div>', unsafe_allow_html=True)
        else:
            # Fluxo normal para outras intenções
            with st.spinner('Afinando os instrumentos... 🎸'):
                if mode == '🔄 Híbrido (Recomendado)':
                    response, detected_intents, primary_intent = combined_respond(user_input, threshold_clf, threshold_ret)
                elif mode == '🎯 Apenas Classificador':
                    response, detected_intents, primary_intent = combined_respond(user_input, threshold_clf, 0.0)
                else:  # Retrieval only
                    resp, intent, confidence = retrieve_response(user_input, threshold=threshold_ret)
                    source = 'retrieval' if intent != 'fallback' else 'fallback'
                    # Converte para o novo formato
                    detected_intents = [{
                        'intent': intent,
                        'confidence': confidence,
                        'method': source,
                        'segment': user_input
                    }]
                    primary_intent = detected_intents[0]
                    response = resp
            
            # Exibição dos resultados (somente para fluxo normal)
            st.markdown("---")
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown("**👤 Você disse:**")
            with col2:
                st.info(user_input)
                
            st.markdown("**🤖 RockStar Burger responde:**")
            # Substituir $ por entidade HTML para evitar interpretação LaTeX
            response_safe = response.replace('$', '&#36;')
            st.markdown(f'<div class="chatbot-response">{response_safe}</div>', unsafe_allow_html=True)
            
            # Análise técnica
            st.markdown("### 📊 Backstage (Análise Técnica)")
            
            # Mostra todas as intenções detectadas
            st.markdown("**🎯 Intenções Detectadas:**")
            
            if len(detected_intents) == 1:
                # Uma única intenção
                intent_data = detected_intents[0]
                intent_display = intent_data['intent'].replace('_', ' ').title()
                confidence_pct = intent_data['confidence'] * 100
                confidence_color = "🟢" if confidence_pct >= 70 else "🟡" if confidence_pct >= 50 else "🔴"
                
                col1, col2 = st.columns(2)
                with col1:
                    st.success(f"**{intent_display}**")
                    st.info(f"**{confidence_color} {confidence_pct:.1f}%**")
                
                with col2:
                    source_emoji = {
                        'classifier': '🧠 Classificador ML',
                        'retrieval': '🔍 Busca por Similaridade',
                        'fallback': '❓ Resposta Padrão'
                    }
                    method_name = source_emoji.get(intent_data['method'], intent_data['method'])
                    st.warning(f"**{method_name}**")
            else:
                # Múltiplas intenções
                st.info(f"**🔍 {len(detected_intents)} intenções detectadas na sua mensagem:**")
                
                for i, intent_data in enumerate(detected_intents, 1):
                    intent_display = intent_data['intent'].replace('_', ' ').title()
                    confidence_pct = intent_data['confidence'] * 100
                    confidence_color = "🟢" if confidence_pct >= 70 else "🟡" if confidence_pct >= 50 else "🔴"
                    
                    method_emoji = {
                        'classifier': '🧠',
                        'retrieval': '🔍',
                        'fallback': '❓'
                    }
                    
                    with st.expander(f"{i}. {intent_display} {confidence_color} {confidence_pct:.1f}%"):
                        st.write(f"**Segmento analisado:** '{intent_data['segment']}'")
                        st.write(f"**Método:** {method_emoji.get(intent_data['method'], '')} {intent_data['method'].title()}")
                        st.write(f"**Confiança:** {confidence_pct:.1f}%")
            
            # Texto normalizado
            st.markdown("### 🔤 Processamento de Texto")
            normalized = normalize_text(user_input)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📝 Texto Original:**")
                st.code(user_input, language="text")
            with col2:
                st.markdown("**🔤 Texto Normalizado:**")
                st.code(normalized, language="text")

# Menu de ingredientes (fora do botão principal para permitir clicks)
if st.session_state.get('show_ingredientes_menu', False):
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**👤 Você disse:**")
    with col2:
        st.info(st.session_state.get('last_user_input', ''))
    
    st.markdown("**🤖 RockStar Burger responde:**")
    st.markdown('<div class="chatbot-response">Beleza! 🎸 Escolha o lanche que você quer saber os ingredientes:</div>', unsafe_allow_html=True)
    
    # Grade de botões com os pratos
    st.markdown("### 🍔 Nossos Lanches:")
    cols = st.columns(3)
    for idx, prato in enumerate(PRATOS):
        with cols[idx % 3]:
            if st.button(f"🔥 {prato}", key=f"ing_{prato}", use_container_width=True):
                with st.spinner(f'Consultando receita de {prato}... 🔥'):
                    try:
                        import json
                        api_key = st.secrets["deepseek"]["api_key"]
                        resultado = consulta_deepseek(prato, api_key)
                        st.markdown(f'<div class="chatbot-response"><strong>🍔 Ingredientes para {prato}:</strong></div>', unsafe_allow_html=True)
                        
                        # Tenta parsear como JSON para exibição estruturada
                        try:
                            # Remove possíveis marcadores de cache/mensagens
                            resultado_limpo = resultado.split('\n\n*️⃣')[0].split('\n\n📋')[0].strip()
                            dados_json = json.loads(resultado_limpo)
                            st.json(dados_json, expanded=True)
                        except:
                            # Se não for JSON válido, exibe como código
                            st.code(resultado, language='json', line_numbers=False)
                        
                        # Desativa o menu após mostrar resultado
                        st.session_state['show_ingredientes_menu'] = False
                    except Exception as e:
                        st.error(f"Erro ao consultar ingredientes: {e}")
                        st.markdown('<div class="chatbot-response">Desculpe, não consegui buscar os ingredientes no momento. Tente novamente mais tarde.</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; font-family: "Courier New", monospace; color: #CCCCCC;'>
    <small>
    🤘 <strong>RockStar Burger</strong> - O sabor do rock na sua fome 🤘<br>
    Chatbot desenvolvido com Python, Streamlit & N.L.P.
    </small>
</div>
""", unsafe_allow_html=True)