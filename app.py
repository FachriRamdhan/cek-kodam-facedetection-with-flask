from flask import Flask, render_template, Response, jsonify
import cv2
import random

app = Flask(__name__)

# Daftar nama legenda
names = [
    "Roro Jonggrang", "Jaka Tarub", "Malin Kundang", "Sangkuriang", 
    "Si Pitung", "Legenda Danau Toba", "Bidadari", "Kancil", 
    "Nyai Roro Kidul", "Ki Ageng Selo", "Timun Mas", "Lutung Kasarung", 
    "Si Joko Lindok", "Jenglot", "Siti Nurbaya", "Gatotkaca", 
    "Bima", "Arjuna", "Dewi Sri", "Siti Hawa", 
    "Tangkuban Perahu", "Puspita", "Nyi Roro Kidul", "Si Kancil", 
    "Semar", "Joko Tarub", "Putri Cinta", "Nyi Blorong", 
    "Sangkuriang", "Raja Wali", "Ken Arok", "Singa Putih", "Kera Sakti", 
    "Kucing Garong", "Putri Salju", "Ga ada wkwk", "Kaga punya wkwk"
]

# Variabel global untuk menyimpan nama yang ditampilkan
current_animal = None

# Inisialisasi webcam
cap = cv2.VideoCapture(0)

def generate_frames():
    global current_animal
    while True:
        success, frame = cap.read()
        if not success:
            break
        # Deteksi wajah (misalnya dengan Haar Cascade)
        # Jika wajah terdeteksi, ambil nama random
        # Contoh deteksi sederhana (ganti dengan logika deteksi nyata)
        if random.choice([True, False]):  # Simulasi deteksi wajah
            if current_animal is None:
                current_animal = random.choice(names)
        
        # Mengubah frame ke JPEG untuk streaming
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/current_animal')
def current_animal_endpoint():
    return jsonify({'animal': current_animal})

@app.route('/refresh')
def refresh():
    global current_animal
    current_animal = None
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
