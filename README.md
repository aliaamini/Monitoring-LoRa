# 📡 LoRa Monitoring System with ESP32 & Firebase

## 📖 Deskripsi Proyek
Proyek ini merupakan sistem monitoring berbasis **LoRa (Long Range Communication)** menggunakan dua buah ESP32. Sistem ini membaca data lingkungan dari beberapa sensor, mengirimkannya secara nirkabel, menampilkan data dalam GUI Python, serta menyimpannya ke Firebase agar dapat diakses melalui website di perangkat lain.

---

## ⚙️ Arsitektur Sistem

### 🔹 Device 1 (Sender / Node)
- ESP32 + LoRa module
- Sensor:
  - DHT22 (suhu & kelembapan udara)
  - Soil Moisture Sensor (kelembapan tanah)
  - Light Sensor (intensitas cahaya)
- Fungsi:
  - Membaca data sensor
  - Mengirim data melalui LoRa ke Device 2

---

### 🔹 Device 2 (Receiver / Gateway)
- ESP32 + LoRa module
- Fungsi:
  - Menerima data dari Device 1
  - Mengirim data ke PC/Laptop melalui Serial

---

### 🔹 PC/Laptop (Python GUI)
- Menampilkan data sensor dalam GUI
- Setelah data diterima:
  - Mengirim data ke Firebase

---

### 🔹 Firebase & Website
- Data disimpan di Firebase
- Website mengambil data dari Firebase
- Data dapat diakses secara real-time dari device lain

---

## 🔄 Alur Sistem

1. Sensor membaca data lingkungan  
2. ESP32 (Device 1) mengirim data via LoRa  
3. ESP32 (Device 2) menerima data  
4. Data dikirim ke PC melalui Serial  
5. Python GUI membaca dan menampilkan data  
6. Python mengirim data ke Firebase  
7. Website mengambil data dari Firebase  

---

## 🧰 Teknologi yang Digunakan

- ESP32  
- LoRa Module (SX1278 / SX1276)  
- Python (GUI + Firebase)  
- Firebase Realtime Database / Firestore  
- HTML, CSS, JavaScript  

---

## 📦 Struktur Folder
