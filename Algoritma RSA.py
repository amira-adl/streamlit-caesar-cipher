# Fungsi untuk menghitung (basis^eksponen) mod mod
def pangkat_modular(basis, eksponen, mod):
    hasil = 1 # Inisialisasi pangkat
    basis %= mod # Menjadikan basis lebih kecil dari mod 
    while eksponen > 0: # Melakukan perulangan selama nilai eksponen lebih dari 0 atau positif
        if eksponen % 2 == 1: # Jika ada eksponen ganjil, maka mengalikan hasil dengan basis
            hasil = (hasil * basis) % mod # Memperbarui hasil dengan dikalikan basis
        basis = (basis * basis) % mod # Mengkuadratkan basis untuk langkah selanjutnya
        eksponen //= 2 # Eksponen dibagi dua setiap langkahnya
    return hasil

# Fungsi untuk mencari bilangan relative prima
def gcd(a, b):
    while b:
        a, b = b, a % b # Algoritma Euclidean
    return a

# Fungsi mencari invers dari modulo phi
def invers_modular(e, phi):
    for d in range(2, phi): # Uji semua kemungkinan nilai d dari 2 hingga phi-1 untuk mencari invers dari e
        if (e * d) % phi == 1:
            return d
    return -1 # Jika tidak ada invers

# Membuat pasangan kunci RSA
def buat_kunci():
    p = 13
    q = 17
    n = p * q # Hasil kali p dan q adalah bagian dari kunci publik dan privat
    phi = (p - 1) * (q - 1) # Fungsi Euler 
    for e in range(2, phi): # Mencari nilai e yang memenuhi gcd(e, phi) = 1
        if gcd(e, phi) == 1:
            break
    d = invers_modular(e, phi) # d = kunci privat
    return e, d, n

# Menjalankan Program
pub, priv, n = buat_kunci()
print("Kunci Publik:", (pub, n))
print("Kunci Privat:", (priv, n))

# Pesan string
pesan = "keamanan"
print("Pesan Asli:", pesan)

# Ubah menjadi list ASCII
blok_ascii = [ord(char) for char in pesan]
print("Blok ASCII:", blok_ascii)

# Fungsi enkripsi
def enkripsi(m, e, n):
    return pangkat_modular(m, e, n) # c = m^e mod n

# Enkripsi
ciphertext = [enkripsi(m, pub, n) for m in blok_ascii]
print("Ciphertext:", ciphertext)

# Fungsi dekripsi
def dekripsi(c, d, n):
    return pangkat_modular(c, d, n) # m = c^d mod n

# Dekripsi
Dekripsi = [dekripsi(c, priv, n) for c in ciphertext]
# Ubah ke string lagi
hasil = ''.join(chr(m) for m in Dekripsi)
print("Dekripsi:", hasil)
