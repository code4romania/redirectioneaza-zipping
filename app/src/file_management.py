import hashlib
import logging
import os
from zipfile import ZipFile

from requests import get

pdfs_folder = "pdfs"
zips_folder = "zips"


def urls_to_zip(pdf_urls):
    if not os.path.exists(pdfs_folder):
        os.mkdir(pdfs_folder)
    if not os.path.exists(zips_folder):
        os.mkdir(zips_folder)

    source_folder: str = _process_files(pdf_urls)
    zipped_file: str = _zip_files(source_folder)

    return zipped_file


def _process_files(all_pdfs) -> str:
    files_count: int = len(all_pdfs)

    logging.info("#" * 80)
    logging.info(f"PROCESSING {files_count} FILES")
    logging.info("#" * 80)

    h = hashlib.new("sha256")
    pdfs_encoding_name: str = "-".join(sorted(all_pdfs))
    h.update(pdfs_encoding_name.encode("utf-8"))
    hex_digest: str = h.hexdigest()

    source_folder = _archive_or_create_folder(hex_digest)

    for index, pdf in enumerate(all_pdfs):
        file_name: str = "-".join(pdf.split("/")[-3:])
        file_path: str = os.path.join(source_folder, f"{file_name}.pdf")

        main_logging_header: str = f" #{index + 1:06d}/{files_count:06d} - "
        secondary_logging_header: str = f"{' ' * len(main_logging_header)}"
        logging.info(f"{main_logging_header}{file_name}")

        if os.path.exists(file_path):
            logging.info(f"{secondary_logging_header}File already exists")
            continue

        logging.info(f"{secondary_logging_header}Downloading this file")

        new_pdf: bytes = get(pdf).content
        with open(file_path, "wb") as f:
            f.write(new_pdf)

    return source_folder


def _archive_or_create_folder(hex_digest) -> str:
    source_folder: str = os.path.join(pdfs_folder, hex_digest)

    if not os.path.exists(pdfs_folder):
        os.mkdir(pdfs_folder)

    if not os.path.exists(source_folder):
        os.mkdir(source_folder)

    return source_folder


def _zip_files(source_folder) -> str:
    file_hash: str = source_folder.split("/")[-1]
    zip_file_name: str = os.path.join(zips_folder, f"pdfs-{file_hash}.zip")
    with ZipFile(zip_file_name, "w") as zip_obj:
        for folder_name, _, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path: str = os.path.join(folder_name, filename)
                zip_obj.write(file_path, os.path.basename(file_path))

    return zip_file_name
