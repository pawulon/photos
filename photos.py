import piexif
from datetime import datetime

def get_photo_date(file_path: str) -> datetime:
    photo_details = get_photo_details(file_path)
    return photo_details['Exif'][piexif.ExifIFD.DateTimeOriginal]
    
def get_photo_details(file_path: str) -> dict():
    return piexif.load(file_path)
    

if __name__ == '__main__':
    print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))