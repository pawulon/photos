import os
import piexif
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class Photo:
    path: str
    size: bytes
    date: datetime


@dataclass
class PhotoAlbum:
    path: str
    start_date: datetime
    end_date: datetime
    size: bytes
    photo_count: int
    files_without_date: List[Photo]

    def __post_init__(self):
        if self.start_date == datetime.max:
            self.start_date = self.end_date = None


    def __str__(self):
        return f'''PhotoAlbum {self.path}
        Start date: {self.start_date}
        End date: {self.end_date}
        Album size: {self.size / 1024 / 1024} MB
        Photos count: {self.photo_count}'''


def get_photo_date(file_path: str) -> Optional[datetime]:
    photo_details = get_photo_details(file_path)
    photo_details_exif = photo_details['Exif']
    photo_date_time_field = piexif.ExifIFD.DateTimeOriginal
    try:
        photo_date_time = photo_details_exif[photo_date_time_field]
        photo_date_time_str = photo_date_time.decode('utf-8')
        return datetime.strptime(photo_date_time_str, '%Y:%m:%d %H:%M:%S')
    except KeyError:
        return None


def get_photo_size(file_path: str) -> bytes:
    return os.path.getsize(file_path)


def get_photo_details(file_path: str) -> Dict[str, Dict]:
    return piexif.load(file_path)


def get_photos_from_folder(folder_path: str) -> List[Photo]:
    photos = []
    for root, dirs, files in os.walk(folder_path):
        print(root)
        for file in files:
            # if file.endswith('JPG'):
            file_path = os.path.join(root, file)
            photo_date = get_photo_date(file_path)
            photo_size = get_photo_size(file_path)
            photos.append(Photo(path=file_path, size=photo_size, date=photo_date))
    return photos


def get_photo_album(folder_path: str) -> PhotoAlbum:
    min_date = datetime.max
    max_date = datetime.min
    photo_count = 0
    album_size = 0
    photos_without_date = []
    for photo in get_photos_from_folder(folder_path):
        photo_count += 1
        album_size += photo.size
        if photo.date:
            if photo.date > max_date:
                max_date = photo.date
            if photo.date < min_date:
                min_date = photo.date
        else:
            photos_without_date.append(photo)

    return PhotoAlbum(path=folder_path, start_date=min_date, end_date=max_date,
                      size=album_size, photo_count=photo_count, files_without_date=photos_without_date)


def find_dates_anomalies(folder_path: str) -> List[Tuple]:
    anomalies = []
    oldest_date = datetime.min
    last_file = None
    for photo in get_photos_from_folder(folder_path):
        if photo.date < oldest_date:
            print(f'ALERT! {photo_path} is older than {last_file}.')
            print(f'       {oldest_date} is older than {photo_date}.')
            anomalies.append(photo)
    return anomalies


# def analyze_photo_folder(folder_path: str) -> None:


if __name__ == '__main__':
    print(get_photo_album(r'C:\temp\test'))
    # print(find_dates_anomalies(r'C:\Users\DOM\Pictures\165___07'))
    # print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))
