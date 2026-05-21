import streamlit as st
import openai

# -------------------------
# CONFIGURATION DE LA PAGE
# -------------------------
st.set_page_config(page_title="ShortsScript IA", page_icon="🎬", layout="wide")

# Police Poppins pour le design pro
st.markdown("""
<style>
@import url('https://googleapis.com');
html, body, div, p, h1, h2, h3, h4, h5, h6, span {
    font-family: 'Poppins', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)

# -------------------------
# BARRE LATÉRALE : CONFIGURATION API
# -------------------------
with st.sidebar:
    st.title("⚙️ Configuration")
    api_key = st.text_input("Clé API OpenAI", type="password", help="Insérez votre clé OpenAI pour tester le script.")
    st.info("💡 Pour la version finale payante, vous masquerez cette case et utiliserez vos propres variables d'environnement (st.secrets) pour facturer vos clients.")

# -------------------------
# CORPS DE LA PAGE
# -------------------------
st.title("🎬 ShortScript IA")
st.subheader("Générez des scripts de vidéos courtes (TikTok, Reels, Shorts) à haute rétention.")

# Formulaire en une seule ligne/bloc
with st.container(border=True):
    col_input, col_style = st.columns([2, 1])
    
    with col_input:
        sujet = st.text_area("Quel est le sujet de votre vidéo ? (ou collez un article/idées brutes)", 
                             placeholder="Ex: 3 astuces psychologiques pour vendre n'importe quel produit sans forcer...")
        
    with col_style:
        style = st.selectbox("Style de la vidéo", [
            "🔥 Storytelling (Captivant / Émotion)", 
            "🧠 Éducatif (Clair / Scientifique)", 
            "⚡ Controverse / Avis tranché (Fort engagement)",
            "🛠️ Tutoriel Rapide (Actionnable)"
        ])
        ton = st.selectbox("Ton de la voix", ["Énergique", "Mystérieux", "Professionnel", "Amical"])

    generer = st.button("🚀 Générer le Script Vidéo Pro", use_container_width=True)

# -------------------------
# LOGIQUE GÉNÉRATION IA
# -------------------------
if generer:
    if not api_key:
        st.error("⚠️ Veuillez entrer votre clé API OpenAI dans la barre latérale pour tester.")
    elif not sujet:
        st.error("⚠️ Veuillez décrire le sujet de votre vidéo.")
    else:
        with st.spinner("L'IA analyse les algorithmes et rédige votre script..."):
            try:
                # Initialisation du client OpenAI
                client = openai.OpenAI(api_key=api_key)
                
                # Prompt système ultra précis pour structurer la réponse de l'IA
                prompt_systeme = """Tu es un expert mondial en ghostwriting et en création de vidéos courtes virales (TikTok, Instagram Reels, YouTube Shorts).
                Ton but est d'écrire un script de moins de 60 secondes structuré de manière chirurgicale pour retenir l'attention.
                
                Tu dois obligatoirement formater ta réponse sous forme de tableau Markdown avec exactement 3 colonnes :
                1. **Section** (ex: Hook (0-5s), Corps (5-45s), CTA (45-60s))
                2. **Voix Off (Ce qu'il faut dire)** (Texte rythmé, phrases courtes, mots percutants)
                3. **Visuel & B-Roll (Ce qu'il faut montrer)** (Instructions visuelles précises pour le montage : gros plan, texte à l'écran, transition rapide, etc.)
                
                Ne fais aucune introduction ni conclusion, commence directement par le tableau Markdown."""

                prompt_utilisateur = f"Rédige un script vidéo sur le sujet suivant : '{sujet}'.\nStyle : {style}\nTon : {ton}."

                # Appel à l'API OpenAI
                reponse = client.chat.completions.create(
                    model="gpt-4o-mini", # Modèle rapide et très économique
                    messages=[
                        {"role": "system", "content": prompt_systeme},
                        {"role": "user", "content": prompt_utilisateur}
                    ],
                    temperature=0.7
                )
                
                # Affichage du résultat
                script_genere = reponse.choices[0].message.content
                
                st.success("✨ Votre script à haute rétention est prêt !")
                
                # Zone d'affichage du tableau
                st.markdown(script_genere)
                
                # Option pratique pour le client
                st.text_area("Copier le script brut :", value=script_genere, height=200)

            except Exception as e:
                st.error(f"Une erreur est survenue avec l'API : {str(e)}")
