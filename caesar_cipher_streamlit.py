import streamlit as st

st.title("Caesar Cipher Enkripsi & Dekripsi")

text = st.text_input("Masukkan teks (huruf kecil saja):", "")
key = st.number_input("Masukkan kunci (key):", min_value=0, max_value=25, value=3)
mode = st.radio("Pilih mode:", ("Enkripsi", "Dekripsi"))

def caesar_cipher(text, k, mode="encrypt"):
    result = ''
    for i in range(len(text)):
        if text[i].isalpha():
            if mode == "encrypt":
                c = ((ord(text[i]) + k - 97) % 26) + 97
            elif mode == "decrypt":
                c = ((ord(text[i]) - k - 97) % 26) + 97
            result += chr(c)
        else:
            result += text[i]
    return result

if st.button("Proses"):
    if mode == "Enkripsi":
        output = caesar_cipher(text, key, mode="encrypt")
        st.success(f"Hasil Enkripsi: {output}")
    else:
        output = caesar_cipher(text, key, mode="decrypt")
        st.success(f"Hasil Dekripsi: {output}")
