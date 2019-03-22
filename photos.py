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
    

def list_photos_dates_in_folder():
    pass

if __name__ == '__main__':
    print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))