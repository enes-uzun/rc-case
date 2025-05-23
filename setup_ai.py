#!/usr/bin/env python3
"""
Competitor Dashboard AI Integration Setup Script
Bu script AI özelliklerini projeye entegre etmek için gerekli adımları gerçekleştirir.
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Python versiyonunu kontrol et"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 veya üzeri gerekli!")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK")

def install_python_dependencies():
    """Python AI service dependencies'ları yükle"""
    print("📦 Python dependencies yükleniyor...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies başarıyla yüklendi")
    except subprocess.CalledProcessError:
        print("❌ Python dependencies yüklenirken hata oluştu")
        sys.exit(1)

def setup_environment():
    """Environment variables'ı ayarla"""
    print("🔧 Environment dosyası kontrol ediliyor...")
    
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists():
        if env_example.exists():
            # Copy example to .env
            with open(env_example, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env dosyası oluşturuldu (env.example'dan kopyalandı)")
        else:
            # Create basic .env
            env_content = """# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# AI Service Configuration
AI_SERVICE_URL=http://localhost:8000
AI_SERVICE_ENABLED=true

# Application Configuration
REACT_APP_AI_FEATURES_ENABLED=true
REACT_APP_AI_SERVICE_URL=http://localhost:8000
"""
            with open(env_file, 'w') as f:
                f.write(env_content)
            print("✅ .env dosyası oluşturuldu")
    else:
        print("✅ .env dosyası zaten mevcut")
    
    print("⚠️  OpenAI API anahtarını .env dosyasında OPENAI_API_KEY değişkenine ayarlamayı unutmayın!")

def check_openai_key():
    """OpenAI API anahtarını kontrol et"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API anahtarı bulunamadı!")
        print("💡 Aşağıdaki adımları takip edin:")
        print("   1. .env dosyasını açın")
        print("   2. OPENAI_API_KEY=your_actual_key_here şeklinde ayarlayın")
        print("   3. API anahtarınızı https://platform.openai.com/api-keys adresinden alabilirsiniz")
        return False
    else:
        print("✅ OpenAI API anahtarı ayarlanmış")
        return True

def create_start_scripts():
    """Başlatma scriptleri oluştur"""
    print("📝 Başlatma scriptleri oluşturuluyor...")
    
    # AI Service start script
    ai_start_script = """#!/bin/bash
echo "🚀 Starting AI Service..."
export PYTHONPATH=$PYTHONPATH:$(pwd)
python ai_service.py
"""
    
    with open("start_ai_service.sh", "w") as f:
        f.write(ai_start_script)
    
    os.chmod("start_ai_service.sh", 0o755)
    
    # Combined start script
    combined_script = """#!/bin/bash
echo "🚀 Starting Competitor Dashboard with AI Features..."

# Start AI service in background
echo "Starting AI Service..."
python ai_service.py &
AI_PID=$!

# Wait a bit for AI service to start
sleep 3

# Start frontend
echo "Starting Frontend..."
cd case1
npm run dev &
FRONTEND_PID=$!

echo "✅ Services started:"
echo "   🤖 AI Service: http://localhost:8000"
echo "   🌐 Frontend: http://localhost:5173"
echo "   📚 AI API Docs: http://localhost:8000/docs"

# Function to cleanup processes
cleanup() {
    echo "🛑 Stopping services..."
    kill $AI_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# Wait for processes
wait
"""
    
    with open("start_full_stack.sh", "w") as f:
        f.write(combined_script)
    
    os.chmod("start_full_stack.sh", 0o755)
    
    print("✅ Başlatma scriptleri oluşturuldu:")
    print("   - start_ai_service.sh (Sadece AI service)")
    print("   - start_full_stack.sh (AI + Frontend birlikte)")

def test_ai_service():
    """AI service'in çalışıp çalışmadığını test et"""
    print("🧪 AI Service test ediliyor...")
    try:
        import requests
        response = requests.get("http://localhost:8000", timeout=5)
        if response.status_code == 200:
            print("✅ AI Service çalışıyor")
            return True
    except:
        pass
    print("⚠️  AI Service şu anda çalışmıyor (Normal - henüz başlatmadık)")
    return False

def create_readme():
    """AI features için README oluştur"""
    readme_content = """# 🤖 AI-Enhanced Competitor Dashboard

Bu proje OpenAI GPT-4 ile geliştirilmiş rakip analizi dashboard'u içerir.

## 🚀 Hızlı Başlangıç

### 1. Setup
```bash
python setup_ai.py
```

### 2. OpenAI API Anahtarını Ayarla
`.env` dosyasını açın ve API anahtarınızı ayarlayın:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3. Servisleri Başlat
```bash
# Tüm servisleri birlikte başlat
./start_full_stack.sh

# Veya ayrı ayrı:
python ai_service.py          # AI Service (Port 8000)
cd case1 && npm run dev       # Frontend (Port 5173)
```

## 🤖 AI Özellikleri

### 📊 Sentiment Analysis
- Her haber için otomatik pozitif/negatif/nötr analizi
- Güven skoru ve iş etkisi değerlendirmesi
- Görsel sentiment göstergeleri

### 🧠 Weekly Insights
- AI-powered haftalık pazar analizi
- Fırsatlar ve tehditler analizi
- Stratejik öneriler
- Market trend tespiti

### 🎯 Smart Alerts
- Yüksek etkili haberler için otomatik uyarılar
- Rakip aktivite analizi
- Iş relevansı skorlaması

## 📡 API Endpoints

- `GET /` - Service status
- `POST /api/ai/analyze-sentiment` - News sentiment analysis
- `POST /api/ai/generate-insights` - Weekly insights generation
- `POST /api/ai/full-analysis` - Comprehensive analysis

API dokümantasyonu: http://localhost:8000/docs

## 🔧 Konfigürasyon

Environment variables:
- `OPENAI_API_KEY` - OpenAI API anahtarı (gerekli)
- `AI_SERVICE_URL` - AI service URL'i
- `REACT_APP_AI_FEATURES_ENABLED` - Frontend AI özelliklerini aktif/pasif

## 🚨 Troubleshooting

### AI Service bağlantı hatası
1. AI service'in çalıştığından emin olun: `python ai_service.py`
2. Port 8000'in boş olduğunu kontrol edin
3. OpenAI API anahtarının doğru ayarlandığından emin olun

### Frontend AI özellikleri görünmüyor
1. AI service çalışıyor olmalı
2. CORS ayarlarını kontrol edin
3. Browser console'da hata mesajlarını kontrol edin

## 💰 Maliyet Optimizasyonu

- GPT-4o-mini modeli kullanılıyor (cost-effective)
- Rate limiting implementasyonu
- Cache mekanizması (gelecek versiyonlarda)

## 📈 Sonraki Adımlar

- [ ] Real-time alerts sistemi
- [ ] Advanced trend prediction
- [ ] Multi-language support
- [ ] Custom AI model training
"""

    with open("AI_README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ AI_README.md oluşturuldu")

def main():
    print("🤖 AI-Enhanced Competitor Dashboard Setup")
    print("=" * 50)
    
    # Checks
    check_python_version()
    
    # Setup
    install_python_dependencies()
    setup_environment()
    
    # Load environment
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key_set = check_openai_key()
    
    # Create scripts and docs
    create_start_scripts()
    create_readme()
    
    print("\n🎉 Setup tamamlandı!")
    print("=" * 50)
    
    if api_key_set:
        print("✅ Tüm gereksinimler karşılandı")
        print("\n🚀 Başlatmak için:")
        print("   ./start_full_stack.sh")
        print("\n📚 Dokümantasyon:")
        print("   AI_README.md dosyasını okuyun")
    else:
        print("⚠️  OpenAI API anahtarını ayarladıktan sonra:")
        print("   ./start_full_stack.sh")
    
    print("\n🌐 Erişim URL'leri:")
    print("   Frontend: http://localhost:5173")
    print("   AI Service: http://localhost:8000")
    print("   API Docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 