from config import Config
import re, os

class CommonFunctions:

    @staticmethod
    def validate_email(email):  
        """Custom email validation function"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None


