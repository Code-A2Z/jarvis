import streamlit as st
import qrcode
import io

def QRCodeGenerator():
  input_data = st.text_area("Enter data for the QR Code (text, link, number, etc.)")
  if st.button("Generate QR Code"):
    if input_data:
      qr = qrcode.QRCode(
        version=1,
        border=4,
        box_size=10,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
      )
      qr.add_data(input_data)
      qr.make(fit=True)
      img = qr.make_image(fill_color="black", back_color="white")

      buf = io.BytesIO()
      img.save(buf, format="PNG")
      byte_im = buf.getvalue()

      st.image(byte_im, caption="Generated QR Code")
      st.download_button(
        label="Download QR Code",
        data=byte_im,
        file_name="qr_code.png",
        mime="image/png"
      )
    else:
      st.toast("Please enter some data to generate the QR code.", icon="⚠️")
