import streamlit as st
import sqlite3
from datetime import datetime
import pandas as pd

# --- FUNGSI ENKRIPSI DAN DEKRIPSI ---
def caesar_cipher(text, k):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + k) % 26 + base)
        else:
            result += char
    return result

# --- FORMAT RUPIAH ---
def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ecommerce (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            category TEXT,
            price REAL,
            key INTEGER,
            encrypted_name TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_to_db(name, category, price, key, encrypted_name):
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''
        INSERT INTO ecommerce (product_name, category, price, key, encrypted_name, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, category, price, key, encrypted_name, timestamp))
    conn.commit()
    conn.close()

def fetch_history():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('SELECT * FROM ecommerce ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def clear_history():
    conn = sqlite3.connect('ecommerce.db')
    c = conn.cursor()
    c.execute('DELETE FROM ecommerce')
    conn.commit()
    conn.close()

# --- APLIKASI STREAMLIT ---
st.set_page_config(page_title="🛍️ Enkripsi Produk E-Commerce", layout="wide")
st.title("🛡️ Aplikasi Enkripsi Nama Produk E-Commerce")
st.markdown("Masukkan informasi produk untuk dienkripsi dan disimpan. Sistem ini juga menyediakan proses dekripsi otomatis.")

# Inisialisasi database
init_db()

# --- FORM INPUT DATA PRODUK ---
with st.form("form_input", clear_on_submit=True):
    st.subheader("📝 Input Produk")
    name = st.text_input("Nama Produk", placeholder="Contoh: Laptop Gaming Asus")
    category = st.selectbox(
        "Kategori Produk",
        ["Elektronik", "Fashion", "Makanan & Minuman", "Kesehatan", "Rumah Tangga", "Olahraga", "Hobi", "Lainnya"]
    )
    price = st.number_input("Harga (Rp)", min_value=0.0, step=1000.0, format="%.2f")
    key = st.slider("Kunci Enkripsi", 1, 25, 3)
    submitted = st.form_submit_button("🔐 Enkripsi & Simpan")

    if submitted:
        if name.strip() == "":
            st.warning("⚠️ Nama produk tidak boleh kosong.")
        else:
            encrypted = caesar_cipher(name.lower(), key)
            insert_to_db(name, category, price, key, encrypted)
            st.success(f"✅ Produk berhasil disimpan dan terenkripsi.")

# --- TAMPILKAN RIWAYAT ENKRIPSI ---
st.subheader("📄 Riwayat Produk Terenkripsi")
rows = fetch_history()
if rows:
    processed_rows = []
    for row in rows:
        id_, name, category, price, key, encrypted, timestamp = row
        decrypted = caesar_cipher(encrypted, -key)
        processed_rows.append((id_, name, category, format_rupiah(price), key, encrypted, decrypted, timestamp))

    df = pd.DataFrame(processed_rows, columns=[
        "ID", "Nama Produk", "Kategori", "Harga", "Kunci", "Terenkripsi", "Terdekripsi", "Waktu"
    ])

    st.dataframe(df.drop(columns=["ID"]), use_container_width=True, height=400)

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Hapus Semua Riwayat"):
            clear_history()
            st.warning("🧹 Riwayat telah dihapus.")
            st.rerun()
    with col2:
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Unduh Riwayat (.csv)", csv, "riwayat_produk.csv", "text/csv")
else:
    st.info("📭 Belum ada data produk yang terenkripsi.")
