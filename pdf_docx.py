import streamlit as st
import os
from pdf2docx import Converter
import tempfile

# Fonction pour convertir les fichiers PDF en DOCX
def convert_pdf_to_docx(pdf_files, output_dir):
    for pdf_file in pdf_files:
        try:
            # Enregistrer le fichier PDF temporairement
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
                tmp_pdf.write(pdf_file.read())
                tmp_pdf_path = tmp_pdf.name
            
            # Définir le chemin du fichier DOCX
            docx_path = os.path.join(output_dir, os.path.splitext(pdf_file.name)[0] + '.docx')
            
            # Conversion du fichier PDF en DOCX
            cv = Converter(tmp_pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            # Supprimer le fichier PDF temporaire
            os.remove(tmp_pdf_path)

            st.write(f"Fichier converti : {docx_path}")
        except Exception as e:
            st.error(f"Erreur lors de la conversion de {pdf_file.name} : {e}")

    st.success("Conversion terminée avec succès!")

# Interface Streamlit
def main():
    st.title("Convertisseur PDFs en DOCX")

    pdf_files = st.file_uploader("Télécharger des fichiers PDF", type="pdf", accept_multiple_files=True)
    output_dir = st.text_input("Entrez le chemin du répertoire de sortie")

    if pdf_files and output_dir:
        if st.button("Convertir"):
            if os.path.isdir(output_dir):
                with st.spinner("Conversion en cours..."):
                    convert_pdf_to_docx(pdf_files, output_dir)
                if st.button("Initialiser"):
                    st.experimental_rerun()
            else:
                st.error("Le répertoire de sortie spécifié n'existe pas. Veuillez réessayer.")

if __name__ == '__main__':
    main()
