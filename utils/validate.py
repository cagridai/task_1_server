from datetime import datetime

# Geçerli bir tarih formatı olup olmadığını kontrol eder
def validate_date(date_text):
    try:
        return datetime.strptime(date_text, '%Y-%m-%d').date()  # Gün-ay-yıl formatı
    except ValueError:
        return None

# Geçerli bir zaman formatı olup olmadığını kontrol eder
def validate_time(time_text):
    try:
        return datetime.strptime(time_text, '%H:%M').time()  # Saat:dakika formatı
    except ValueError:
        return None
