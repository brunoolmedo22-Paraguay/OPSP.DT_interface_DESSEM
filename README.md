# 📊 OPSP.DT Interface DESSEM — Dashboard PDO

Plataforma de visualização em Streamlit para resultados do modelo DESSEM – ONS.

> **Versão Refatorada:** Suporte a GitHub + Streamlit Cloud com caminhos relativos

---

## 📁 Estrutura de Pastas

```
OPSP.DT_interface_DESSEM_deploy/
├── presentacion_app.py              ← Script principal (Streamlit)
├── organize_folders.py              ← [Opcional] Script para organizar pastas
├── .gitignore                       ← Configuração do Git
├── README.md                        ← Este arquivo
│
└── DATABASE/                        ← 📌 PASTA DE DADOS (não versionar)
    │
    ├── DS_ONS_032026_RV0D06/       ← Uma data de simulação
    │   ├── pdo_sist.dat            ⭐ OBRIGATÓRIO (colunas sistema por IPER)
    │   ├── pdo_term.dat            ❌ OPCIONAL (geração por usina)
    │   ├── pdo_sist_arq.txt        🗑️ Pode deletar
    │   └── pdo_term_arq.txt        🗑️ Pode deletar
    │
    ├── DS_ONS_062026_RV2D15/
    │   ├── pdo_sist.dat
    │   ├── pdo_term.dat
    │   └── ...
    │
    └── [outras datas...]
```

---

## 🚀 Início Rápido

### 1. **Setup Local**

```bash
# Criar estrutura
mkdir OPSP.DT_interface_DESSEM_deploy
cd OPSP.DT_interface_DESSEM_deploy

# Clonar repo (se já em GitHub)
git clone https://github.com/seu-usuario/OPSP.DT_interface_DESSEM_deploy.git

# Ou: criar manualmente
mkdir DATABASE

# Copiar arquivos DESSEM de Downloads/
cp -r ~/Downloads/DS_ONS_* DATABASE/
```

### 2. **Instalar Dependências**

```bash
pip install streamlit pandas numpy plotly
```

### 3. **Rodar Localmente**

```bash
streamlit run presentacion_app.py
```

A app abrirá em `http://localhost:8501`

---

## ⭐ O Código Realmente Usa

| Arquivo | Status | Descrição |
|---------|--------|-----------|
| `pdo_sist.dat` | ✅ **OBRIGATÓRIO** | CMO, DEMANDA, geração por fonte, EARM (por IPER) |
| `pdo_term.dat` | ❌ Opcional | Detalhes de usinas térmicas (CVU, geração) |
| `pdo_sist_arq.txt` | 🗑️ Desnecessário | Log/arquivo duplicado, pode deletar |
| `pdo_term_arq.txt` | 🗑️ Desnecessário | Log/arquivo duplicado, pode deletar |
| `*.log` | 🗑️ Desnecessário | Logs, podem deletar |
| Outros arquivos | 🗑️ Desnecessário | Não são lidos, podem deletar |

---

## 📊 Funcionalidades do Dashboard

### 1. **Mix de Geração**
Área-stacked com Renovável, Hidráulica, Térmica + Geração Total

### 2. **CMO & Demanda**
Série temporal dupla (eixos independentes) — CMO em R$/MWh, Demanda em MW

### 3. **Share de Fontes**
Percentual de cada fonte ao longo do dia

### 4. **Curva do Pato & Rampa**
Identifica automaticamente:
- Vale solar (mínimo 10h–16h)
- Pico vespertino
- Rampa de demanda líquida
- Resposta hidráulica

### 5. **Curva de Duração**
Área-stacked ordenada por geração total decrescente

---

## 🎛️ Controles (Sidebar)

- **Data de Operação**: Dropdown com datas disponíveis em `DATABASE/`
- **Subsistema**: SIN, SE, S, NE, N
- **IPER (Hora)**: Slider 1–48 (00:00 → 23:30, intervalos de 30 min)

Exibe a hora em tempo real e a pasta DESSEM ativa

---

## 📦 Dependências

```
streamlit >= 1.20
pandas >= 1.3
numpy >= 1.20
plotly >= 5.0
```

Instalar tudo:
```bash
pip install -r requirements.txt
```

(Gerar arquivo: `pip freeze > requirements.txt`)

---

## 🔧 Configuração de Caminhos

### ✅ Caminhos Relativos (Nova Versão)

```python
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(SCRIPT_DIR, "DATABASE")
```

Detecta automaticamente onde o script `.py` está localizado.

**Funciona em:**
- ✅ Windows, Mac, Linux
- ✅ Local + Streamlit Cloud
- ✅ Qualquer máquina

---

## 🐱 GitHub + Streamlit Cloud

### 1. **Preparar Repo**

```bash
# Criar .gitignore
cp .gitignore seu-repo/

# Adicionar ao Git
git add -A
git commit -m "Refatoração: caminhos relativos + estrutura DATABASE"
```

### 2. **Deploy Streamlit Cloud**

1. Conectar GitHub
2. Selecionar branch
3. Definir arquivo: `presentacion_app.py`
4. Clique em "Deploy"

### 3. **Upload de Dados (Opções)**

**Opção A: Git LFS** (grandes arquivos)
```bash
git lfs track "DATABASE/**/*.dat"
git add .gitattributes
git push
```

**Opção B: Secrets + API** (dados confidenciais)
Streamlit Secrets para links de download

**Opção C: Upload Manual** (via dashboard Streamlit Cloud)

---

## 🧹 Limpeza de Arquivos Desnecessários

### Automático (Python)
```bash
python organize_folders.py
```

Encontra pastas `DS_ONS_*` e move para `DATABASE/`, removendo lixo

### Manual
```bash
# Remover arquivos específicos
rm DATABASE/**/*_arq.txt
rm DATABASE/**/*.log
rm DATABASE/**/*_backup.*
```

---

## 🐛 Troubleshooting

### ❌ "Arquivo não encontrado: pdo_sist.dat"

**Verificar:**
1. Pasta `DATABASE/` existe na raiz do projeto?
2. Dentro de `DATABASE/`, existe pasta `DS_ONS_032026_RV0D06/` (ou outra data)?
3. Dentro dela, existe arquivo `pdo_sist.dat`?

**Estrutura esperada:**
```
./DATABASE/DS_ONS_032026_RV0D06/pdo_sist.dat
```

### ⚠️ "pdo_term.dat" não encontrado

**É normal!** O arquivo é opcional. O dashboard continua funcionando sem ele.

### 🐌 Dashboard lento / crash

Possíveis causas:
- Arquivo `pdo_sist.dat` corrompido ou muito grande
- Falta de RAM para processar Streamlit
- Cache não funcionando

Solução:
```bash
streamlit cache clear
```

---

## 📝 Notas Técnicas

### Codificação
Arquivos DESSEM em **latin1** (ISO-8859-1)
```python
with open(arq_sist, "r", encoding="latin1") as f:
```

### Parsing
Separador: `;` (ponto-e-vírgula)
Decimal: `,` (vírgula, convertido para `.`)

### Cache Streamlit
Funções decoradas com `@st.cache_data` para evitar recarregar arquivos

---

## 🚀 Roadmap

- [ ] Autenticação (para dados confidenciais)
- [ ] Export de gráficos (PDF, PNG)
- [ ] Simulações customizadas
- [ ] Banco de dados (ao invés de arquivos `.dat`)
- [ ] Dashboard de comparação (múltiplas datas lado-a-lado)

---

## 👤 Contribuição & Suporte

**Questões?**
- Abra uma issue no GitHub
- Verifique `SETUP_GUIA.md` e `MUDANCAS_DETALHADAS.md`

---

## 📜 Licença

[Definir sua licença aqui]

---

## 🎯 Checklist Final

Antes de fazer commit/push:

- [ ] Estrutura de pastas criada (`DATABASE/`)
- [ ] Arquivos DESSEM copiados (`pdo_sist.dat` + `pdo_term.dat`)
- [ ] Arquivos desnecessários removidos (`*_arq.txt`, `*.log`)
- [ ] Script testado localmente (`streamlit run presentacion_app.py`)
- [ ] `.gitignore` configurado
- [ ] Nenhum erro no sidebar (exibe `./DATABASE`)
- [ ] Todos os gráficos renderizam corretamente
- [ ] Pronto para GitHub ✅

---

**Desenvolvido para OPSP.DT · Última atualização: 2026-06-23**
