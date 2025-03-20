import gradio as gr
import pytesseract
from pdf2image import convert_from_path
import fitz  # PyMuPDF
from PIL import Image
import cv2
import numpy as np
import os
from typing import List

# Configurar Tesseract no Render
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Criar pasta de saída
OUTPUT_FOLDER = "output"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Melhorar a qualidade da imagem antes do OCR
def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return Image.fromarray(binary)

# Converter PDFs escaneados para pesquisáveis
def make_pdf_searchable(pdf_path):
    images = convert_from_path(pdf_path, dpi=300)
    pdf_writer = fitz.open()

    for image in images:
        processed_img = preprocess_image(image)
        text_pdf = pytesseract.image_to_pdf_or_hocr(processed_img, lang="por", config="--psm 6")
        ocr_page = fitz.open("pdf", text_pdf)
        pdf_writer.insert_pdf(ocr_page)

    output_pdf = os.path.join(OUTPUT_FOLDER, "pesquisavel_" + os.path.basename(pdf_path))
    pdf_writer.save(output_pdf)
    return output_pdf

# Processar múltiplos arquivos
def process_multiple_pdfs(pdf_files: List[str]):
    output_files = [make_pdf_searchable(pdf) for pdf in pdf_files]
    return output_files

# Criar interface do Gradio
demo = gr.Interface(
    fn=process_multiple_pdfs,
    inputs=gr.File(label="Envie seus PDFs", file_types=[".pdf"], type="filepath", file_count="multiple"),
    outputs=gr.Files(label="Baixar PDFs Convertidos"),
    title="Conversor de PDF Pesquisável",
    description="Envie um ou mais PDFs escaneados para torná-los pesquisáveis!",
    allow_flagging="never"
)

# Iniciar o Gradio no Render.com
demo.launch(server_name="0.0.0.0", server_port=8080)
