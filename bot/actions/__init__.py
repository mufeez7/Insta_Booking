import os
import sys
import django

sys.path.insert(0, "C:/Users/mufeezur.rehman/pythvirenv/venvs/BookingReplicate/")
os.environ["DJANGO_SETTINGS_MODULE"] = "BookingReplicate.settings"
django.setup()