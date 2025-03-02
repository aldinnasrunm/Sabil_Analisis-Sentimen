from flask import Flask, render_template, request
import pickle  # Untuk memuat model dan vectorizer

# Inisialisasi aplikasi Flask
app = Flask(__name__)

# Load model dan vectorizer untuk Automation
model = pickle.load(open('Model/model_auto (1).pkl', 'rb'))
vectorizer = pickle.load(open('Model/vec_auto (1).pkl', 'rb'))

# Fungsi untuk kategori user dan topik
def categorize_user(comment):
    gen_z_keywords = ["wkwk", "anjay", "vibes", "ngegas", "cringe", "gokil", "bjir", "coded", "anjir",
                      "baper", "mager", "yaudah", "pov", "senior", "milenial", "boomer", "toxic"]
    comment = comment.lower()
    for word in gen_z_keywords:
        if word in comment:
            return "Gen Z"
    return "Non Gen Z"

def assign_topic(comment):
    topics = {
        "Kreativitas": ["ide", "kreatif", "inovasi", "original", "karya", "cerdas", "pintar"],
        "Komunikasi": ["bicara", "ngomong", "presentasi", "komunikasi", "sharing", "ngobrol"],
        "Disiplin": ["tepat waktu", "telat", "nelat", "rapi", "rajin", "on time", "disiplin", "teratur", "deadline", "kerja keras"],
        "Kerja Tim": ["kolaborasi", "kerja sama", "tim", "koordinasi", "diskusi", "cooperative"],
        "Motivasi": ["semangat", "motivasi", "inspirasi", "pantang menyerah", "pencapaian", "ngeluh", "cape"],
        "Self-Care Enthusiast": []  # Kategori untuk komentar yang tidak cocok dengan kategori apapun
    }
    comment = comment.lower()
    for topic, keywords in topics.items():
        for keyword in keywords:
            if keyword in comment:
                return topic
    return "Self-Care Enthusiast"

# Route untuk halaman utama
@app.route('/')
def home():
    return render_template('index.html')

# Route untuk prediksi
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        text = request.form['text']  # Ambil input dari textarea
        print(f"Teks yang dimasukkan: {text}")  # Debugging input
        
        # Cek apakah teks tidak kosong
        if not text.strip():
            return render_template('index.html', 
                                   prediction_text='Masukkan teks yang valid.',
                                   user_category='',
                                   topic_category='',
                                   user_text=text)

        transformed_text = vectorizer.transform([text])  # Transformasi teks dengan vectorizer
        prediction = model.predict(transformed_text)  # Prediksi model
        print(f"Hasil Prediksi: {prediction}")  # Debugging hasil prediksi

        sentiment_result = "Positif" if prediction[0] == 1 else "Negatif"  # Hasil sentimen
        user_category = categorize_user(text)  # Kategori user berdasarkan teks
        topic_category = assign_topic(text)  # Kategori topik berdasarkan teks

        return render_template('index.html', 
                               prediction_text=f'{sentiment_result}',
                               user_category=f'{user_category}',
                               topic_category=f'{topic_category}',
                               user_text=text)

# Jalankan aplikasi
if __name__ == '__main__':
    app.run()  # Aktifkan debug untuk membantu troubleshooting
