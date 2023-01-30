from pathlib import Path
from shutil import copyfile
import sys
from threading import Thread

def main(folder_for_scan):

    REGISTER_EXTENSIONS = {
        'IMAGES' : ['JPEG', 'PNG', 'JPG', 'SVG'],
        'DOCUMENTS' : ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
        'MUSIC' : ['MP3', 'OGG', 'WAV', 'AMR'],
        'VIDEO' : ['AVI', 'MP4', 'MOV', 'MKV'],
        'ARCHIVES' : ['ZIP', 'GZ', 'TAR'],
        'UNKNOWN': []
    }

    FILES = {
        'IMAGES' : [],
        'DOCUMENTS' : [],
        'MUSIC' : [],
        'VIDEO' : [],
        'ARCHIVES' : [],
        'UNKNOWN' : []
    }

    FOLDERS = []
    EXTENSIONS = []
    for key, val in REGISTER_EXTENSIONS.items():
        for ext in val:
            EXTENSIONS.append(ext)

    def parser(folder: Path) -> None:
        for item in folder.iterdir():
            if item.is_dir():
                if item.name not in ('ARCHIVES', 'VIDEO', 'MUSIC', 'DOCUMENTS', 'IMAGES', 'UNKNOWN'):
                    FOLDERS.append(item)
                    parser(item)
                continue
            ext = Path(item.name).suffix[1:].upper()
            fullname = folder / item.name
            if not ext in EXTENSIONS:
                 FILES['UNKNOWN'].append(fullname)
            else:
                for key, val in REGISTER_EXTENSIONS.items():
                    if ext in val:
                        FILES[key].append(fullname)


    def handle_media(filename: Path, target_folder: Path):
        target_folder.mkdir(exist_ok=True, parents=True)
        copyfile(filename, target_folder / filename.name)
        # filename.replace(target_folder / filename.name)

    parser(Path(folder_for_scan))

    def sort_file(files):
        for file in files:
            handle_media(file, Path(folder_for_scan) / folder)

    # def copy_func(folders):
    #     for folder, files in FILES.items():
    #         for file in files:
    #             handle_media(file, folders / folder)
    # copy_func(Path(folder_for_scan))

    threads = []

    for folder, files in FILES.items():
        th = Thread(target=sort_file, args=(files,))
        th.start()
        threads.append(th)

    [th.join() for th in threads]


if __name__ == '__main__':

    try:
        folder_for_scan = Path(sys.argv[1])
        print(f'Start in folder {folder_for_scan.resolve()}')
    except IndexError:
        print(f'Start this code in terminal like "py this_file.py C:\Folder"')
    else:
        main(folder_for_scan.resolve())

    # folder_for_scan = "D:\Sort"
    # main(folder_for_scan)

