# 🚀 Competitor Dashboard - Revo Capital Case Study

Modern bir competitor analysis dashboard'u ve veri toplama sistemi.

## 📊 Özellikler

### React Dashboard
- ✅ **Modern UI**: Tailwind CSS + Radix UI
- ✅ **Responsive Design**: Tüm cihazlarda mükemmel görünüm
- ✅ **Dark Mode**: Koyu tema desteği
- ✅ **TypeScript**: Tip güvenliği
- ✅ **Real-time Data**: Canlı veri entegrasyonu

### Python Veri Toplama
- ✅ **Google Custom Search**: Gerçek API kullanımı
- ✅ **Competitor Tracking**: 28+ rakip şirket takibi
- ✅ **Rate Limiting**: API koruması
- ✅ **UTF-8 Desteği**: Türkçe karakter desteği
- ✅ **Automatic Updates**: Otomatik veri güncelleme

## 🏗️ Teknoloji Stack

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Radix UI
- Vite

**Backend/Data:**
- Python 3.11+
- Google Custom Search API
- yfinance
- requests

## 🚀 Kurulum

### 1. Repository'yi klonlayın
```bash
git clone https://github.com/enes-uzun/rc-case.git
cd rc-case
```

### 2. Python bağımlılıkları
```bash
pip install requests yfinance
```

### 3. Node.js bağımlılıkları
```bash
npm install
```

## 📈 Kullanım

### React Dashboard'u başlatın
```bash
npm run dev
```
Dashboard: http://localhost:5173

### Veri toplama scriptini çalıştırın
```bash
python data_collector_enhanced.py
```

## 📁 Proje Yapısı

```
├── 📊 Python Veri Sistemi
│   ├── data_collector_enhanced.py   # Ana veri toplama
│   ├── bluedot_data.json           # Bluedot verileri
│   ├── massive_bio_data.json       # Massive Bio verileri
│   └── all_company_data.json       # Birleşik veriler
│
├── 🎨 React Dashboard
│   ├── src/
│   │   ├── App.tsx                 # Ana uygulama
│   │   ├── components/ui/          # UI bileşenleri
│   │   └── data/                   # Veri dosyaları
│   ├── package.json
│   └── vite.config.ts
```

## 🎯 Öne Çıkan Özellikler

### 🔍 Kapsamlı Veri Toplama
- **Bluedot**: 13 competitor + güncel haberler
- **Massive Bio**: 15 competitor + güncel haberler
- **Real-time**: Son 1 ay içindeki haberler

### 📱 Modern Dashboard
- Temiz, profesyonel arayüz
- Responsive tasarım
- Hızlı ve akıcı performans

### 🔄 Otomatik Güncelleme
- Kolay cron job kurulumu
- Windows Task Scheduler desteği
- Rate limiting koruması

## 🏢 Takip Edilen Şirketler

**Bluedot Competitors:**
- EV Connect, ChargeHub, GreenFlux
- Pionix, ChargeLab, Electrify America
- EVCS, Vehya, PlugShare
- + 4 diğer şirket

**Massive Bio Competitors:**
- Deep 6 AI, Elligo Health Research
- TrialJectory, Antidote, Oncoshot
- Arctic Therapeutics, BioPhy
- + 8 diğer şirket

## 📊 Veri Çıktıları

Script şu dosyaları oluşturur:
- `bluedot_data.json` - Bluedot ve rakipleri
- `massive_bio_data.json` - Massive Bio ve rakipleri  
- `all_company_data.json` - Tüm veriler birleşik

## 🛠️ Geliştirme

```bash
# Development server
npm run dev

# Build production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## 📝 Lisans

Bu proje Revo Capital case study için geliştirilmiştir.

---
**Geliştirici:** Enes Uzun  
**Tarih:** Mayıs 2025 