import nltk
import ssl

# Ignora verificação SSL (pode ajudar com alguns firewalls)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

print("🔽 Baixando dados do NLTK...")
print("=" * 50)

# Lista de pacotes necessários
pacotes = ['punkt', 'wordnet', 'omw-1.4', 'stopwords']

for pacote in pacotes:
    print(f"\n📦 Baixando {pacote}...")
    try:
        nltk.download(pacote, quiet=False)
        print(f"✅ {pacote} baixado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao baixar {pacote}: {e}")

print("\n" + "=" * 50)
print("✅ Processo concluído!")
print("\nVerificando instalação:")
print("-" * 50)

# Testa se os dados foram instalados
try:
    from nltk.corpus import wordnet
    print("✅ wordnet OK")
except:
    print("❌ wordnet FALHOU")

try:
    from nltk.corpus import stopwords
    print("✅ stopwords OK")
except:
    print("❌ stopwords FALHOU")

try:
    from nltk.tokenize import word_tokenize
    word_tokenize("teste")
    print("✅ punkt OK")
except:
    print("❌ punkt FALHOU")
