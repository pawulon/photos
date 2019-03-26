import os
import piexif
from datetime import datetime
from typing import List, Tuple, Dict, Optional
from dataclasses import dataclass


@dataclass
class MediaFile:
    path: str
    size: bytes
    date: datetime
    is_image: bool


@dataclass
class MediaAlbum:
    path: str
    start_date: datetime
    end_date: datetime
    size: bytes
    files_count: int
    photos_without_date: List[MediaFile]
    non_image_files: List[MediaFile]

    def __post_init__(self):
        if self.start_date == datetime.max:
            self.start_date = self.end_date = None

    def __str__(self):
        album_description = f'PhotoAlbum {self.path}'
        if self.start_date:
            album_description += f'\n\tPhotos start date: {self.start_date}'
            album_description += f'\n\tPhotos end date: {self.end_date}'
        album_description += f'\n\tAlbum size: {self.size / 1024 / 1024} MB'
        album_description += f'\n\tFiles count: {self.files_count}'
        if self.non_image_files:
            album_description += f'\n\tNon image files: {[file.path for file in self.non_image_files]}'
        if self.photos_without_date:
            album_description += f'\n\tPhotos without date: {[file.path for file in self.photos_without_date]}'
        return album_description


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


def get_file_size(file_path: str) -> bytes:
    return os.path.getsize(file_path)


def get_photo_details(file_path: str) -> Dict[str, Dict]:
    return piexif.load(file_path)


def get_files_from_folder(folder_path: str) -> List[MediaFile]:
    photos = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            is_image = True
            try:
                photo_date = get_photo_date(file_path)
            except piexif._exceptions.InvalidImageDataError:
                photo_date = None
                is_image = False
            photo_size = get_file_size(file_path)
            photos.append(MediaFile(path=file_path, size=photo_size, date=photo_date, is_image=is_image))
    return photos


def get_media_album(folder_path: str) -> MediaAlbum:
    min_date = datetime.max
    max_date = datetime.min
    files_count = 0
    album_size = 0
    photos_without_date = []
    non_image_files = []

    for media_file in get_files_from_folder(folder_path):
        files_count += 1
        album_size += media_file.size
        if media_file.is_image:
            if media_file.date:
                if media_file.date > max_date:
                    max_date = media_file.date
                if media_file.date < min_date:
                    min_date = media_file.date
            else:
                photos_without_date.append(media_file)
        else:
            non_image_files.append(media_file)

    return MediaAlbum(path=folder_path, start_date=min_date, end_date=max_date,
                      size=album_size, files_count=files_count, photos_without_date=photos_without_date,
                      non_image_files=non_image_files)


def find_dates_anomalies(folder_path: str) -> List[Tuple]:
    anomalies = []
    oldest_date = datetime.min
    last_file = None
    for photo in get_files_from_folder(folder_path):
        if photo.date < oldest_date:
            print(f'ALERT! {photo_path} is older than {last_file}.')
            print(f'       {oldest_date} is older than {photo_date}.')
            anomalies.append(photo)
    return anomalies


# def analyze_photo_folder(folder_path: str) -> None:


if __name__ == '__main__':
    print(get_media_album(r'C:\temp\test'))
    # print(find_dates_anomalies(r'C:\Users\DOM\Pictures\165___07'))
    # print(get_photo_date(r'C:\Users\DOM\Pictures\165___07\IMG_0676.JPG'))
