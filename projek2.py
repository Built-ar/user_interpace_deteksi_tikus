import cv2
import sqlite3
import datetime
import soundfile as sf
import sounddevice as sd
from tkinter import Tk, Label, Button, Toplevel, messagebox
from PIL import ImageTk, Image

# Fungsi untuk memasukkan data waktu deteksi tikus ke dalam database SQLite
def insert_data(timestamp):
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()

    # Membuat tabel jika belum ada
    cursor.execute('''CREATE TABLE IF NOT EXISTS detections
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       timestamp TEXT)''')

    # Memasukkan data waktu deteksi ke dalam tabel
    cursor.execute("INSERT INTO detections (timestamp) VALUES (?)", (timestamp,))
    conn.commit()

    conn.close()

# Load cascade classifier untuk mendeteksi tikus
cascade_path = 'Wajah.xml'
cascade_classifier = cv2.CascadeClassifier(cascade_path)

# Fungsi untuk mendeteksi tikus dan mengambil tindakan saat terdeteksi
def detect_mouse(frame):
    # Ubah gambar ke grayscale untuk deteksi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Deteksi tikus menggunakan cascade classifier
    mice = cascade_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Jika ada tikus yang terdeteksi
    if len(mice) > 0:
        # Dapatkan waktu deteksi tikus
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

        # Simpan gambar tikus dengan nama berdasarkan waktu deteksi
        filename = f'Deteksi_{timestamp}.jpg'
        cv2.imwrite(filename, frame)

        # Panggil fungsi untuk memasukkan data waktu deteksi ke dalam database
        insert_data(timestamp)

        # Mainkan suara notifikasi
        audio_data, _ = sf.read('notif2.wav')
        sd.play(audio_data)

        # Tampilkan kotak dan teks pada tikus yang terdeteksi
        for (x, y, w, h) in mice:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, 'Tikus terdeteksi', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Tampilkan frame
    cv2.imshow('Deteksi Tikus', frame)

# Fungsi untuk memulai deteksi tikus
def start_detection():
    #global cap
    #cap = cv2.VideoCapture(0)
    # Memperbarui tampilan video pada label
    #update_video()
    global is_detecting
    is_detecting = True
    update_video()

# Fungsi untuk menghentikan deteksi tikus
def stop_detection():
    global cap
    cap.release()
    cv2.destroyAllWindows()
    
def show_detection_results():
    # Query data waktu deteksi dari database
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM detections")
    rows = cursor.fetchall()
    conn.close()

    # Tampilkan gambar hasil deteksi
    for row in rows:
        timestamp = row[0]
        formatted_timestamp = timestamp.replace(" ", "_")  # Mengganti spasi dengan garis bawah
        filename = f"Deteksi_{formatted_timestamp}.jpg"
        try:
            image = cv2.imread(filename)
            cv2.imshow('Hasil Deteksi', image)
            cv2.waitKey(0)
        except Exception as e:
            print(f"Gagal membuka file {filename}: {e}")

# Fungsi untuk membuka jendela hasil deteksi
def open_detection_results():
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()

    # Mengeksekusi query untuk mendapatkan semua data deteksi
    cursor.execute("SELECT * FROM detections")
    results = cursor.fetchall()

    if len(results) > 0:
        # Membuka jendelabaru untuk menampilkan hasil deteksi
        results_window = Toplevel()
        results_window.title("Hasil Deteksi")

    # Membuat label untuk menampilkan hasil deteksi
    for result in results:
        label = Label(results_window, text=result[1])
        label.pack()
    else:
        messagebox.showinfo("Info", "Belum ada deteksi tikus yang tersimpan.")

    conn.close()

# Fungsi untuk membuka jendela hasil deteksi
def open_detection_results():
    conn = sqlite3.connect('detection.db')
    cursor = conn.cursor()

    # Mengeksekusi query untuk mendapatkan semua data deteksi
    cursor.execute("SELECT * FROM detections")
    results = cursor.fetchall()

    if len(results) > 0:
        # Membuka jendela baru untuk menampilkan hasil deteksi
        results_window = Toplevel()
        results_window.title("Hasil Deteksi")

        for result in results:
            timestamp = result[1]
            image_path = f'Deteksi_{timestamp}.jpg'

            # Menampilkan gambar hasil deteksi
            image = Image.open(image_path)
            image = image.resize((300, 300), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            label = Label(results_window, image=photo)
            label.image = photo  # Menjaga referensi agar gambar tetap ditampilkan
            label.pack()

    else:
        messagebox.showinfo("Info", "Belum ada deteksi tikus yang tersimpan.")

    conn.close()

    #Fungsi untuk memperbarui tampilan video pada label
def update_video():
    ret, frame = cap.read()
    if ret:
        detect_mouse(frame)# Lakukan deteksi tikus
        window.after(10, update_video)# Memperbarui tampilan video setiap 10 milidetik
        
#Membuat jendela GUI
window = Tk()
window.title("Deteksi Tikus")
window.geometry("500x500")

#Membuat label untuk menampilkan video
label = Label(window)
label.pack()

#Membuat tombol untuk memulai dan menghentikan deteksi tikus
start_button = Button(window, text="Start Detection", command=start_detection)
start_button.pack()

stop_button = Button(window, text="Stop Detection", command=stop_detection)
stop_button.pack()

#Membuat tombol untuk membuka jendela hasil deteksi
results_button = Button(window, text="Hasil Deteksi", command=show_detection_results)
results_button.pack()

#Menjalankan GUI
window.mainloop()









