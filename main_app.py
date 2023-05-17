import tkinter as tk
from PIL import ImageTk, Image


# Fungsi yang dipanggil saat tombol "Mulai Deteksi" ditekan
def mulai_deteksi():
    # Tambahkan kode untuk memulai proses deteksi tikus di sini
    update_output_layer("Mulai Deteksi")
    update_judul("Mulai Deteksi")
    
    #warna Tombol
    mulai_button.config(bg="#4E9258")
    stop_button.config(bg="white")
    hasil_button.config(bg="white")
 

# Fungsi yang dipanggil saat tombol "Stop Deteksi" ditekan
def stop_deteksi():
    # Tambahkan kode untuk menghentikan proses deteksi tikus di sini
    update_output_layer("Stop Deteksi")
    update_judul("Stop Deteksi")
    
    
    #warna Tombol
    mulai_button.config(bg="white")
    stop_button.config(bg="#4E9258")
    hasil_button.config(bg="white")
    
 

# Fungsi yang dipanggil saat tombol "Lihat Hasil" ditekan
def lihat_hasil():
    # Tambahkan kode untuk menampilkan hasil deteksi tikus di layer output di sini
    update_output_layer("Hasil Deteksi")
    update_judul("Hasil Deteksi")
    
    #warna Tombol
    mulai_button.config(bg="white")
    stop_button.config(bg="white")
    hasil_button.config(bg="#4E9258")
 
    
# Fungsi untuk mengupdate atau merefresh layer output
def update_output_layer(text):
    output_layer.delete("all")
    output_layer.create_text(250, 200, text=text, font=("Arial", 20), fill="black")
    update_border()
    
    

# Fungsi untuk menggambar atau memperbarui border pada layer output
def update_border():
    border_color = "black"
    border_width = 3

    x1, y1 = border_width, border_width
    x2, y2 = 500 - border_width, 400 - border_width

    output_layer.create_rectangle(x1, y1, x2, y2, outline=border_color, width=border_width)


def update_judul(text):
    judul_label.config(text=text)
    
    
# Membuat jendela utama
window = tk.Tk()
window.title("Deteksi Tikus")
window.geometry("680x460")
window.resizable(False, False)
window.config(bg="#C3FDB8")

# Fungsi untuk menampilkan gambar di layer output
def set_background_image(window, image_path):
    # Buka gambar sebagai latar belakang
    background_image = ImageTk.PhotoImage(Image.open(image_path))

    # Buat label sebagai kontainer gambar
    background_label = tk.Label(window, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Menyimpan referensi gambar agar tidak terhapus oleh garbage collector
    window.image = background_image

# Membuat tombol-tombol dan menempatkannya di sebelah kiri
left_frame = tk.Frame(window)
left_frame.pack(side=tk.LEFT, padx=10, pady=10)
left_frame.config(bg="#C3FDB8")

# Menentukan ukuran tombol
button_width = 15
button_height = 3

# Membuat tombol-tombol dengan ukuran yang sama
mulai_button = tk.Button(left_frame, text="Mulai Deteksi", command=mulai_deteksi, width=button_width, height=button_height)
mulai_button.pack(pady=5)

stop_button = tk.Button(left_frame, text="Stop Deteksi", command=stop_deteksi, width=button_width, height=button_height)
stop_button.pack(pady=5)

hasil_button = tk.Button(left_frame, text="Lihat Hasil", command=lihat_hasil, width=button_width, height=button_height)
hasil_button.pack(pady=5)

# Membuat layer output di sebelah kanan
right_frame = tk.Frame(window)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10)
right_frame.config(bg="red")


# Membuat judul di atas layer output
judul_label = tk.Label(right_frame, text="", font=("Arial", 12, "bold"))
judul_label.pack()
judul_label.config(bg="white")

# Mengatur border pada layer output
border_color = "black"
border_width = 3


output_layer= tk.Canvas(right_frame, width=500, height=400, bg="yellow")
output_layer.pack()

x1, y1 = border_width, border_width
x2, y2 = 500 - border_width, 400 - border_width

output_layer.create_rectangle(x1, y1, x2, y2, outline=border_color, width=border_width)


# Menjalankan loop utama aplikasi
window.mainloop()

