import streamlit as st
import os
from pdf2docx import Converter
import tempfile
from io import BytesIO

# Fonction pour convertir les fichiers PDF en DOCX
def convert_pdf_to_docx(pdf_files):
    converted_files = []
    for pdf_file in pdf_files:
        try:
            # Enregistrer le fichier PDF temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(pdf_file.read())
                tmp_pdf_path = tmp_pdf.name
            
            # Créer un buffer en mémoire pour le fichier DOCX
            docx_buffer = BytesIO()
            
            # Conversion du fichier PDF en DOCX
            cv = Converter(tmp_pdf_path)
            cv.convert(docx_buffer, start=0, end=None)
            cv.close()

            # Supprimer le fichier PDF temporaire
            os.remove(tmp_pdf_path)

            docx_buffer.seek(0)
            converted_files.append((pdf_file.name, docx_buffer))

            # Afficher le bouton de téléchargement dès que le fichier est prêt
            docx_file_name = os.path.splitext(pdf_file.name)[0] + '.docx'
            st.download_button(
                label=f"Télécharger {docx_file_name}",
                data=docx_buffer,
                file_name=docx_file_name,
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        except Exception as e:
            st.error(f"Erreur lors de la conversion de {pdf_file.name} : {e}")

    return converted_files

# Interface Streamlit
def main():
    st.title("Convertisseur PDF en DOCX")

    # Initialiser l'état de session pour les fichiers convertis
    if 'converted_files' not in st.session_state:
        st.session_state.converted_files = []
    if 'conversion_done' not in st.session_state:
        st.session_state.conversion_done = False

    pdf_files = st.file_uploader("Télécharger des fichiers PDF", type="pdf", accept_multiple_files=True)

    if pdf_files:
        if st.button("Convertir"):
            with st.spinner("Conversion en cours..."):
                st.session_state.converted_files = convert_pdf_to_docx(pdf_files)
                st.session_state.conversion_done = True

    if st.session_state.converted_files:
        if st.session_state.conversion_done:
            st.success("Tous les fichiers ont été convertis avec succès!")
            if st.button("Initialiser"):
                st.session_state.converted_files = []
                st.session_state.conversion_done = False
                st.experimental_rerun()

if __name__ == '__main__':
    main()
