# 💾 Informações de Backup

## 📁 Backups Criados

### `app_backup_20251107_080449.py`
- **Data**: 07/11/2025 às 08:04:49
- **Tamanho**: 56,783 bytes
- **Versão**: Funcional com todas as correções aplicadas
- **Status**: ✅ **ESTÁVEL E TESTADO**

### 🎨 Configurações desta versão:

**Visual:**
- Fundo: Roxo Púrpura (`#4A0E4E`)
- Título: Vermelho sangue (`#E50000`)
- Estrelas brancas animadas no fundo
- Botões roxos com borda vermelha

**Funcionalidades:**
- ✅ 11 intenções detectadas (greeting, goodbye, thanks, purchase, menu, prices, delivery_time, complaint, hours, ingredientes, fallback)
- ✅ 504 exemplos de treinamento com erros de grafia
- ✅ Integração API Deepseek R1 (via OpenRouter)
- ✅ Sistema de retry com 5 tentativas e backoff exponencial
- ✅ Fallback automático com 9 receitas pré-cadastradas
- ✅ Cache inteligente de ingredientes
- ✅ Visualização JSON expansível
- ✅ Formatação correta de preços (R$ sem truncagem)
- ✅ Menu completo de lanches e bebidas
- ✅ Sidebar com lista de intenções

**Correções Aplicadas:**
- ✅ Bug "quanto custa o lanche" → filtro de palavras genéricas expandido
- ✅ Formatação de cifrão (`$`) → convertido para entidade HTML (`&#36;`)
- ✅ API key configurada e validada
- ✅ Intenção de ingredientes adicionada ao sidebar

**Dependências:**
- streamlit>=1.28.0
- nltk>=3.8
- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
- requests>=2.31.0

---

## 🔄 Como Restaurar um Backup

Se precisar voltar para esta versão:

```powershell
# Fazer backup do app.py atual (caso queira)
Copy-Item app.py app_current_backup.py

# Restaurar o backup
Copy-Item app_backup_20251107_080449.py app.py

# Reiniciar Streamlit
Get-Process python* | Stop-Process -Force -ErrorAction SilentlyContinue
python -m streamlit run app.py
```

---

## 📝 Notas

- Backups são automaticamente ignorados pelo Git (`.gitignore`)
- Mantenha pelo menos 2-3 backups de versões estáveis
- Use nomenclatura com timestamp: `app_backup_YYYYMMDD_HHMMSS.py`

---

## 🎯 Próximas Versões

Se fizer mudanças significativas, crie um novo backup:

```powershell
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
Copy-Item app.py "app_backup_$timestamp.py"
Write-Output "Backup criado: app_backup_$timestamp.py"
```

---

**Última atualização**: 07/11/2025 às 08:04:49
