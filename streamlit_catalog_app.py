import streamlit as st
import pandas as pd
import requests
import urllib.parse
from pathlib import Path

# ---------------------------------------
# CONFIGURAÇÕES GERAIS
# ---------------------------------------
st.set_page_config(page_title="Catálogo Alcina", layout="wide")

# ---------------------------------------
# LISTA DE MUNICÍPIOS DA REGIÃO METROPOLITANA DE SP
# ---------------------------------------
rm_sp = [
    "Arujá", "Barueri", "Biritiba Mirim", "Caieiras", "Cajamar", "Carapicuíba",
    "Cotia", "Diadema", "Embu das Artes", "Embu-Guaçu", "Ferraz de Vasconcelos",
    "Francisco Morato", "Franco da Rocha", "Guarulhos", "Itapecerica da Serra",
    "Itapevi", "Itaquaquecetuba", "Jandira", "Juquitiba", "Mairiporã", "Mauá",
    "Mogi das Cruzes", "Osasco", "Pirapora do Bom Jesus", "Poá", "Ribeirão Pires",
    "Rio Grande da Serra", "Salesópolis", "Santa Isabel", "Santana de Parnaíba",
    "Santo André", "São Bernardo do Campo", "São Caetano do Sul", "São Lourenço da Serra",
    "São Paulo", "Suzano", "Taboão da Serra", "Vargem Grande Paulista"
]

# ---------------------------------------
# FUNÇÃO PARA CONSULTAR CNPJ
# ---------------------------------------
def consulta_cnpj(cnpj):
    try:
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        response = requests.get(url)
        data = response.json()

        razao = data.get("nome", "").strip()
        cidade = data.get("municipio", "").strip().title()
        uf = data.get("uf", "").strip()

        return razao, cidade, uf
    except Exception as e:
        st.error(f"Erro ao consultar CNPJ: {e}")
        return None, None, None


# ---------------------------------------
# CAMINHOS SEGUROS (pathlib)
# ---------------------------------------
base_dir = Path(__file__).parent
excel_path = base_dir / "produtos.xlsx"
imagens_dir = base_dir / "imagens"

# ---------------------------------------
# NÚMERO DO WHATSAPP
# ---------------------------------------
WHATSAPP_NUM = "5511939626534"

# ---------------------------------------
# CSS DE ESTILO
# ---------------------------------------
st.markdown("""
<style>
.block-container {max-width: 800px; padding: 1rem;}
.produto-card {
    border: 1px solid #e0e0e0;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 20px;
    background-color: #fafafa;
}
.produto-card img {border-radius: 10px; max-width: 100%;}
.btn-whatsapp {
    background-color: #25D366;
    color: white;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 8px;
    font-weight: bold;
    position: fixed;
    bottom: 25px;
    right: 25px;
    z-index: 999;
}
.botao {
    display: inline-block;
    padding: 4px 10px;
    font-size: 20px;
    margin: 0 5px;
    cursor: pointer;
    border-radius: 6px;
    border: 1px solid #333;
    background-color: #fff;
    color: #333;
}
.botao:hover {background-color: #f0f0f0;}
.whatsapp-counter {
    display: inline-block;
    margin-left: 10px;
    background-color: red;
    color: white;
    font-weight: bold;
    padding: 2px 8px;
    border-radius: 50%;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------
# LOGO DA EMPRESA (ajustado)
# ---------------------------------------
st.markdown(
    """
    <div style="text-align: center; margin-top: 40px; margin-bottom: 40px;">
        <img src="https://static.wixstatic.com/media/12ba6a_4323f01ae83046ca849e63d93d452c52~mv2.png"
             style="max-height: 120px;">
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------
# LÓGICA DE FLUXO COM SESSION_STATE
# ---------------------------------------
if "valido" not in st.session_state:
    st.session_state.valido = False
if "razao" not in st.session_state:
    st.session_state.razao = ""
if "cidade" not in st.session_state:
    st.session_state.cidade = ""
if "uf" not in st.session_state:
    st.session_state.uf = ""
if "preco_col" not in st.session_state:
    st.session_state.preco_col = ""
if "cnpj_input" not in st.session_state:
    st.session_state.cnpj_input = ""
if "carrinho" not in st.session_state:
    st.session_state.carrinho = {}

# ---------------------------------------
# ETAPA 1 – VALIDAÇÃO DO CNPJ
# ---------------------------------------
if not st.session_state.valido:
    st.subheader("Antes de acessar o catálogo, valide seu CNPJ:")

    with st.form("pre_tela"):
        local = st.radio(
            "Selecione sua localidade:",
            ("Estou em SP e região metropolitana", "Demais localidades")
        )
        cnpj_input = st.text_input("Informe seu CNPJ (somente números)")
        submit_btn = st.form_submit_button("Continuar")

    if submit_btn:
        if not cnpj_input.isdigit() or len(cnpj_input) not in [8, 14]:
            st.error("CNPJ inválido. Digite apenas números com 8 ou 14 dígitos.")
            st.stop()

        razao, cidade, uf = consulta_cnpj(cnpj_input)
        if not cidade:
            st.error("Não foi possível validar o CNPJ. Tente novamente.")
            st.stop()

        cidade_fmt = cidade.title().strip()

        # --- Validação cruzada ---
        if local == "Estou em SP e região metropolitana" and cidade_fmt not in rm_sp:
            st.error(f"O CNPJ informado ({cidade_fmt} - {uf}) **não pertence à RM-SP**.")
            st.stop()
        elif local == "Demais localidades" and cidade_fmt in rm_sp:
            st.error(f"O CNPJ informado ({cidade_fmt} - {uf}) **pertence à RM-SP**. Escolha a primeira opção.")
            st.stop()

        # Guarda dados na sessão
        st.session_state.valido = True
        st.session_state.razao = razao
        st.session_state.cidade = cidade_fmt
        st.session_state.uf = uf
        st.session_state.cnpj_input = cnpj_input
        st.session_state.preco_col = "Preço_sp" if cidade_fmt in rm_sp else "Preço_demais_locais"

        # Inicializa carrinho se necessário
        df = pd.read_excel(excel_path)
        st.session_state.carrinho = {row["Nome"]: 0 for _, row in df.iterrows()}
        st.rerun()

# ---------------------------------------
# ETAPA 2 – CATÁLOGO
# ---------------------------------------
else:
    razao = st.session_state.razao
    cidade_fmt = st.session_state.cidade
    uf = st.session_state.uf
    preco_col = st.session_state.preco_col
    cnpj_input = st.session_state.cnpj_input

    st.success(f"Olá, {razao} ({cidade_fmt} - {uf})")

    df = pd.read_excel(excel_path)

    st.header("Catálogo de Produtos")

    total = 0
    for _, row in df.iterrows():
        nome = row["Nome"]
        preco = float(row[preco_col])
        qtd = st.session_state.carrinho.get(nome, 0)

        col1, col2 = st.columns([1, 2])
        with col1:
            img_path = imagens_dir / row["Imagem"]
            if img_path.exists():
                st.image(str(img_path))
            else:
                st.write("📷 Imagem não disponível")

        with col2:
            st.markdown(f"<div class='produto-card'><h4>{row['Nome']}</h4>", unsafe_allow_html=True)
            st.write(row["Descrição"])
            st.write(f"Preço: R$ {preco:,.2f}")
            cols = st.columns([1, 1, 1])
            with cols[0]:
                if st.button("➖", key=f"menos_{nome}"):
                    if qtd > 0:
                        st.session_state.carrinho[nome] -= 1
                        st.rerun()
            with cols[1]:
                st.markdown(f"<div class='whatsapp-counter'>{qtd}</div>", unsafe_allow_html=True)
            with cols[2]:
                if st.button("➕", key=f"mais_{nome}"):
                    st.session_state.carrinho[nome] += 1
                    st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        total += qtd * preco

    st.markdown("---")
    st.markdown(f"### Total do carrinho: R$ {total:,.2f}")

    # --- Monta mensagem do carrinho ---
    mensagem_carrinho = f"Olá, aqui é da empresa {razao}, CNPJ {cnpj_input}. \n\nGostaria de comprar:\n"
    for _, row in df.iterrows():
        nome = row["Nome"]
        qtd = st.session_state.carrinho[nome]
        if qtd > 0:
            preco = float(row[preco_col])
            mensagem_carrinho += f"- {nome}  -  {qtd} x R$ {preco:,.2f}\n"

    if total > 0:
        mensagem_carrinho += f"\nTotal do pedido: R$ {total:,.2f}"
        msg_encoded = urllib.parse.quote(mensagem_carrinho)
        whatsapp_link = f"https://wa.me/{WHATSAPP_NUM}?text={msg_encoded}"

        st.markdown(
            f"""
            <a href='{whatsapp_link}' target='_blank' class='btn-whatsapp'>
                Envie via WhatsApp
                <span class='whatsapp-counter'>{sum(st.session_state.carrinho.values())}</span>
                R$ {total:,.2f}
            </a>
            """,
            unsafe_allow_html=True
        )
