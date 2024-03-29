import hashlib
import logging
import os
from typing import List
from zipfile import ZipFile

from requests import get

pdfs_folder = "_pdfs"
zips_folder = "_zips"
data_folders = (pdfs_folder, zips_folder)


def zip_urls(pdf_urls: List[str], job_identifier: str):
    if not os.path.exists(pdfs_folder):
        os.mkdir(pdfs_folder)
    if not os.path.exists(zips_folder):
        os.mkdir(zips_folder)

    source_folder: str = _process_files(pdf_urls, job_identifier)
    zipped_file: str = _zip_files(source_folder, job_identifier)

    return zipped_file


def _process_files(all_pdfs: List[str], job_identifier: str) -> str:
    files_count: int = len(all_pdfs)

    logging.info("#" * 80)
    logging.info(f"PROCESSING {files_count} FILES")
    logging.info("#" * 80)

    source_folder = _archive_or_create_folder(job_identifier)

    for index, pdf in enumerate(all_pdfs):
        file_name: str = "-".join(pdf.split("/")[-3:])
        file_path: str = os.path.join(source_folder, f"{file_name}.pdf")

        main_logging_header: str = f" #{index + 1:06d}/{files_count:06d} - "
        secondary_logging_header: str = f"{' ' * len(main_logging_header)}"
        logging.info(f"{main_logging_header}{pdf} | {file_name}")

        if os.path.exists(file_path):
            logging.info(f"{secondary_logging_header}File already exists")
            continue

        logging.info(f"{secondary_logging_header}Downloading this file")

        new_pdf: bytes = get(pdf).content
        with open(file_path, "wb") as f:
            f.write(new_pdf)

    return source_folder


def _archive_or_create_folder(job_identifier: str) -> str:
    source_folder: str = os.path.join(pdfs_folder, job_identifier)

    if not os.path.exists(pdfs_folder):
        os.mkdir(pdfs_folder)

    if not os.path.exists(source_folder):
        os.mkdir(source_folder)

    return source_folder


def _zip_files(source_folder: str, job_identifier: str) -> str:
    zip_file_name: str = os.path.join(zips_folder, f"pdfs-{job_identifier}.zip")
    with ZipFile(zip_file_name, "w") as zip_obj:
        for folder_name, _, filenames in os.walk(source_folder):
            for filename in filenames:
                file_path: str = os.path.join(folder_name, filename)
                zip_obj.write(file_path, os.path.basename(file_path))

    return zip_file_name


def encode_file_names(all_pdfs: List[str]) -> str:
    h = hashlib.new("sha256")

    pdfs_encoding_name: str = "-".join(sorted(all_pdfs))
    h.update(pdfs_encoding_name.encode("utf-8"))
    hex_digest: str = h.hexdigest()

    return hex_digest


def clean_up_after_current_job(job_identifier: str) -> None:
    for folder in data_folders:
        _remove_folder_and_contents(folder, job_identifier)


def _remove_folder_and_contents(folder_path: str, job_identifier: str) -> None:
    for folder_name, subfolders, filenames in os.walk(folder_path):
        if len(filenames) == 0:
            logging.info(f"No filenames for job identifier {job_identifier}")
            continue

        # if job_identifier not in folder_name:
        #     continue

        for filename in filenames:
            logging.info(f"Trying to delete file name {filename}")
            if filename.split(".")[-1] == "zip" and job_identifier not in filename:
                continue

            file_path: str = os.path.join(folder_name, filename)
            logging.info(f"Removing {file_path}")
            os.remove(file_path)

        if folder_name != folder_path and folder_name not in data_folders:
            logging.info(f"Removing {folder_name}")
            os.rmdir(folder_name)
