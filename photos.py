import os
import piexif
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

def get_photo_date(file_path: str) -> datetime:
    photo_details = get_photo_details(file_path)
    photo_details_exif = photo_details['Exif']
    photo_date_time_field = piexif.ExifIFD.DateTimeOriginal
    photo_date_time = photo_details_exif[photo_date_time_field]
    photo_date_time_str = photo_date_time.decode('utf-8')
    return datetime.strptime(photo_date_time_str, '%Y:%m:%d %H:%M:%S')
    
def get_photo_details(file_path: str) -> Dict[str, Dict]:
    return piexif.load(file_path)
    

def get_photos_dates_in_folder(folder_path: str) -> List[Tuple[str, datetime]]:
    photos_dates = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('JPG'):
                file_path = os.path.join(root, file)
                photo_date = get_photo_date(file_path)
                photos_dates.append((file_path, photo_date))
    return photos_dates

def list_photos_dates(folder_path: str) -> None:
    for photo_date in get_photos_dates_in_folder(folder_path):
        print(photo_date[0], photo_date[1])

def find_dates_anomalies(folder_path: str) -> List[Tuple]:
    anomalies = []
    oldest_date = datetime.min
    last_file = None
    for photo_path, photo_date in get_photos_dates_in_folder(folder_path):
        if photo_date < oldest_date:
            print(f'ALERT! {photo_path} is older than {last_file}.')
            print(f'       {oldest_date} is older than {photo_date}.')            
            anomalies.append((photo_path, photo_date))
    return anomalies
            
if __name__ == '__main__':
    # list_photos_dates(r'C:\Users\DOM\Pictures\165___07')
    print(find_dates_anomalies(r'C:\Users\DOM\Pictures\165___07'))
    # print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))