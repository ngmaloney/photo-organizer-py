import glob
import hashlib
import os
from io import BytesIO
from turtle import mode
from rich import print
from rich.panel import Panel

from PIL import Image, UnidentifiedImageError
from pillow_heif import register_heif_opener
from PIL.ExifTags import TAGS, GPSTAGS

register_heif_opener()


def organize(src: str, dest: str, dry_run: bool, convert: bool, debug: bool):
    copied_file_shas = []
    for file_path in glob.glob(f"{src}/*"):
        try:
            image = Image.open(file_path)
            verified = image.verify()
            # Re-open because verify removes file handle
            image = Image.open(file_path)
            is_jpg = image.format == "JPEG"
        except UnidentifiedImageError:
            verified = False

        exif_data = image.getexif()

        mode = image.mode
        if mode != "RGB":
          image = image.convert("RGB")

        if verified == False:
            print(f"Ignoring {file_path}")
            continue

        # Extract Image Date
        if exif_data != None:
            for tag_id, value in exif_data.items():
              tag_name = TAGS.get(tag_id, tag_id)
              if tag_name == "DateTimeOriginal":
                image_date = value
              elif tag_name == "DateTime":
                image_date = value
        else:
            image_date = os.path.getctime(file_path)

        # Get Image MD5 for naming/deduplication
        # Compressed images (jpg) must be saved first
        buffer = BytesIO()
        buffer.seek(0)
        image.seek(0)
        image.save(buffer, format="JPEG", exif=exif_data)
        buffer.seek(0)
        md5_hash = hashlib.md5(buffer.read()).hexdigest()

        date_year = image_date.split(" ")[0].split(":")[0]
        date_month = image_date.split(" ")[0].split(":")[1]
        date_day = image_date.split(" ")[0].split(":")[2]
        destination_dir = f"{dest}/{date_year}/{date_month}/{date_day}"
        destination_path = f"{destination_dir}/{md5_hash}.jpg"

        if dry_run == True:
          print(f"Dry Run: Copied {file_path} to {destination_path}")

        else:
          if(os.path.exists(destination_path)):
            print(f"Skipping {file_path} as {destination_path} already exists")
            continue

          if(md5_hash not in copied_file_shas):
            copied_file_shas.append(md5_hash)
            os.makedirs(destination_dir, exist_ok=True)
            image.save(destination_path, format="JPEG", exif=exif_data)
            print(f"Copied {file_path} to {destination_path}")

        if debug == True:
          print(
            "Debug Information:",
            Panel(
              f"FilePath: {file_path} \n"
              f"Verified: {verified} \n"
              f"IsJpg: {is_jpg} \n"
              f"Date: {image_date} \n"
              f"MD5: {md5_hash} \n"
              f"Mode: {mode} \n"
              f"Year: {date_year} \n"
              f"Month: {date_month} \n"
              f"Day: {date_day} \n"
              f"Destination: {destination_path} \n"
              f"Exif: {exif_data}"
            )
          )
