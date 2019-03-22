import os
import piexif
from datetime import datetime

def get_photo_date(file_path: str) -> datetime:
    photo_details = get_photo_details(file_path)
    photo_details_exif = photo_details['Exif']
    photo_date_time_field = piexif.ExifIFD.DateTimeOriginal
    photo_date_time = photo_details_exif[photo_date_time_field]
    photo_date_time_str = photo_date_time.decode('utf-8')
    return datetime.strptime(photo_date_time_str, '%Y:%m:%d %H:%M:%S')
    
def get_photo_details(file_path: str) -> dict():
    return piexif.load(file_path)
    

def list_photos_dates_in_folder(folder_path: str) -> None:
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('JPG'):
                file_path = os.path.join(root, file)
                print(file, get_photo_date(file_path))

if __name__ == '__main__':
    list_photos_dates_in_folder(r'C:\Users\DOM\Pictures\165___07')
    # print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))