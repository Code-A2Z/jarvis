import PyPDF2
import streamlit as st


def readPDF():
  file = st.file_uploader("Upload a PDF file", type=["pdf"])
  if file:
    reader = PyPDF2.PdfReader(file)
    numPage = st.number_input("From which page to start reading?", format="%d", min_value=1, max_value=len(reader.pages))
    page = reader.pages[numPage - 1]
    text = page.extract_text()
    if text:
      st.write(text)
    else:
      st.warning("No text found on this page", icon="⚠️")


def mergePDF():
  uploaded_files = st.file_uploader("Upload PDF files to merge", type=["pdf"], accept_multiple_files=True)
  if uploaded_files:
    pdf_writer = PyPDF2.PdfWriter()
    for file in uploaded_files:
      pdf_reader = PyPDF2.PdfReader(file)
      for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_writer.add_page(page)
    output_pdf = "merged_output.pdf"
    with open(output_pdf, "wb") as f:
      pdf_writer.write(f)
    with open(output_pdf, "rb") as f:
      st.download_button("Download Merged PDF", f, file_name="merged_output.pdf")


def splitPDF():
  file = st.file_uploader("Upload a PDF file to split", type=["pdf"])
  if file:
    pdf_reader = PyPDF2.PdfReader(file)
    start_page = st.number_input("Start page", min_value=1, max_value=len(pdf_reader.pages), value=1)
    end_page = st.number_input("End page", min_value=start_page, max_value=len(pdf_reader.pages), value=len(pdf_reader.pages))
    pdf_writer = PyPDF2.PdfWriter()
    for i in range(start_page - 1, end_page):
      pdf_writer.add_page(pdf_reader.pages[i])
    output_pdf = "split_output.pdf"
    with open(output_pdf, "wb") as f:
      pdf_writer.write(f)
    with open(output_pdf, "rb") as f:
      st.download_button("Download Split PDF", f, file_name="split_output.pdf")


def rotatePDF():
  file = st.file_uploader("Upload a PDF file to rotate", type=["pdf"])
  if file:
    reader = PyPDF2.PdfReader(file)
    writer = PyPDF2.PdfWriter()
    angle = st.selectbox("Select rotation angle (clockwise)", [90, 180, 270])
    for page_num in range(len(reader.pages)):
      page = reader.pages[page_num]
      page.rotate(angle)
      writer.add_page(page)
    output_file = "rotated_output.pdf"
    with open(output_file, "wb") as f:
      writer.write(f)
    with open(output_file, "rb") as f:
      st.download_button("Download Rotated PDF", f, file_name=output_file)


def encryptPDF():
  password = st.text_input("Enter password", type="password", placeholder="your encryption password")
  file = st.file_uploader("Upload a PDF file to encrypt", type=["pdf"])
  if st.button("Encrypt PDF") and password:
    pdf_reader = PyPDF2.PdfReader(file)
    pdf_writer = PyPDF2.PdfWriter()
    for page in pdf_reader.pages:
      pdf_writer.add_page(page)
    pdf_writer.encrypt(password)
    output_pdf = "encrypted_output.pdf"
    with open(output_pdf, "wb") as f:
      pdf_writer.write(f)
    with open(output_pdf, "rb") as f:
      st.download_button("Download Encrypted PDF", f, file_name="encrypted_output.pdf")


def decryptPDF():
  password = st.text_input("Enter password to decrypt", type="password", placeholder="your decryption password")
  file = st.file_uploader("Upload an encrypted PDF file to decrypt", type=["pdf"])
  if st.button("Decrypt PDF") and password and file:
    pdf_reader = PyPDF2.PdfReader(file)
    if pdf_reader.decrypt(password):
      pdf_writer = PyPDF2.PdfWriter()
      for page in pdf_reader.pages:
        pdf_writer.add_page(page)
      output_pdf = "decrypted_output.pdf"
      with open(output_pdf, "wb") as f:
        pdf_writer.write(f)
      with open(output_pdf, "rb") as f:
        st.download_button("Download Decrypted PDF", f, file_name="decrypted_output.pdf")
    else:
      st.error("Incorrect password", icon="🚫")


def PDFToolbox():
  choice = st.selectbox("Choose an operation", ["Read PDF", "Merge PDF", "Split PDF", "Rotate PDF", "Encrypt PDF", "Decrypt PDF"])
  if choice == "Read PDF":
    readPDF()
  elif choice == "Merge PDF":
    mergePDF()
  elif choice == "Split PDF":
    splitPDF()
  elif choice == "Rotate PDF":
    rotatePDF()
  elif choice == "Encrypt PDF":
    encryptPDF()
  elif choice == "Decrypt PDF":
    decryptPDF()
