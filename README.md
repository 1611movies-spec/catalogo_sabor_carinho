# 🍰 Catálogo Sabor & Carinho

Um catálogo digital de produtos desenvolvido para **WhatsApp Business**, permitindo que clientes visualizem os produtos online, escolham o que desejam e gerem automaticamente mensagens de pedido pelo WhatsApp.  
Desenvolvido com **Python** e **Streamlit**, com foco em **visual mobile-friendly**.

---

## 🎯 Objetivo

Criar uma forma simples e moderna de apresentar produtos de forma online, sem precisar de site próprio.  
Os clientes podem:
- Navegar pelos produtos de maneira rápida e intuitiva  
- Visualizar preços e descrições  
- Montar pedidos e enviar automaticamente pelo WhatsApp  

---

## 🧠 Tecnologias Utilizadas

- **Python 3.11+**
- **Streamlit** — Interface web
- **Pandas** — Leitura de planilha de produtos (`produtos.xlsx`)
- **openpyxl** — Manipulação de Excel
- **Git / GitHub** — Controle de versão
- **Streamlit Cloud** — Deploy online gratuito

---

## 📂 Estrutura do Projeto

```
catalogo_sabor_carinho/
├── streamlit_catalog_app.py      # Arquivo principal da aplicação
├── requirements.txt              # Dependências do projeto
├── produtos.xlsx                 # Planilha de produtos
├── imagens/                      # Pasta de imagens dos produtos
└── README.md                     # Este arquivo
```

---

## ⚙️ Instalação Local

### 1️⃣ Clone o repositório
```bash
git clone https://github.com/1611movies-spec/catalogo_sabor_carinho.git
cd catalogo_sabor_carinho
```

### 2️⃣ Crie e ative um ambiente virtual (opcional, mas recomendado)
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Instale as dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Execute localmente
```bash
streamlit run streamlit_catalog_app.py
```

A aplicação abrirá automaticamente em [http://localhost:8501](http://localhost:8501).

---

## 🚀 Deploy no Streamlit Cloud

1. Vá para [https://share.streamlit.io](https://share.streamlit.io)
2. Clique em **New app**
3. Configure:
   - **Repository:** `https://github.com/1611movies-spec/catalogo_sabor_carinho.git`
   - **Branch:** `main`
   - **Main file path:** `streamlit_catalog_app.py`
4. Clique em **Deploy**

Em poucos segundos, o app estará online com um link do tipo:
```
https://saborecarinho.streamlit.app
```

---

## 💬 Envio automático para WhatsApp

O app gera automaticamente uma mensagem personalizada no formato:
```
Olá! Gostaria de fazer o pedido:
- Produto: [nome]
- Quantidade: [x]
```

Ao clicar, o cliente é redirecionado para o WhatsApp com a mensagem pronta para envio.

---

## 🧩 Dependências principais

As bibliotecas estão listadas no arquivo `requirements.txt`.  
Principais pacotes:
```
streamlit
pandas
openpyxl
```

---

## 🧠 Observações Técnicas

- Certifique-se de que o arquivo `produtos.xlsx` contém colunas como **Nome**, **Preço**, **Descrição**, **Imagem**.
- O Streamlit Cloud **não acessa arquivos locais** — tudo deve estar no GitHub.
- Sempre teste localmente antes de enviar atualizações:
  ```bash
  streamlit run streamlit_catalog_app.py
  ```

---

## 👨‍💻 Autor

**Simão (1611movies)**  
🎥 Criador de conteúdo e desenvolvedor independente  
📫 Contato: [https://github.com/1611movies-spec](https://github.com/1611movies-spec)

---

## 🧾 Licença

Este projeto é distribuído sob a licença **MIT** — sinta-se à vontade para usar, modificar e compartilhar.

---

> 💡 *Dica:* Este README segue o padrão profissional usado em projetos Python open-source e serve também como documentação para apresentação a clientes ou patrocinadores.
