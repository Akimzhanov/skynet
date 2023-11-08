from datetime import datetime

def get_data():
     format= '%Y-%m-%d  %H:%M'
     return datetime.now().strftime(format)
