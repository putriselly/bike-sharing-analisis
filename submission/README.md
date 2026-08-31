# Proyek Analisis Data: Bike Sharing Dataset

Proyek ini menganalisis data penyewaan sepeda (Bike Sharing Dataset) untuk menjawab pertanyaan bisnis:
1. Bagaimana pengaruh kondisi cuaca (Cerah, Mendung, dan Hujan Ringan) terhadap jumlah penyewaan sepeda selama periode tahun 2011-2012?
2. Bagaimana pola jumlah penyewaan sepeda pada tiap musim (Semi, Panas, Gugur, Dingin) selama periode tahun 2011-2012, dan musim mana yang memiliki rata-rata penyewaan tertinggi?

## Setup Environment - Anaconda

conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt


## Setup Environment - Shell/Terminal (Pipenv)

cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt


## Menjalankan Aplikasi Streamlit

1. Pindah ke folder dashboard (tempat script utama aplikasi berada):

cd dashboard


2. Jalankan dashboard menggunakan perintah Streamlit:

streamlit run dashboard.py


3. Dashboard akan otomatis terbuka di browser melalui alamat http://localhost:8501.

## Dashboard Online
Dashboard versi online (yang sudah di-deploy) dapat diakses melalui link berikut:
(https://plvb3u94nydmqnxgaldaub.streamlit.app/)
