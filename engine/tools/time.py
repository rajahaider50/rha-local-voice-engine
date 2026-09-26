import datetime

class TimeTools:
    @staticmethod
    def get_current_time() -> str:
        now = datetime.datetime.now()
        return now.strftime("%I:%M %p")
        
    @staticmethod
    def get_current_date() -> str:
        now = datetime.datetime.now()
        return now.strftime("%A, %B %d, %Y")
