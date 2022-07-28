"""
Utils
-----
"""
import cv2
from pyzbar.pyzbar import decode
import os
import sqlite3
import simpleaudio as sa


NOTIFY_SOUND = 'resources/medicine_reminder.wav'


def notify(title: str, text: str):
    """

    :param title: string to display as title
    :param text: text to display for notification
    """
    wave_obj = sa.WaveObject.from_wave_file(NOTIFY_SOUND)
    play_obj = wave_obj.play()
    os.system("""
              osascript -e 'display notification "{}" with title "{}"'
              """.format(text, title))
    play_obj.wait_done()


def get_all_files(directory: str, formats=None):
    """
    Retrieve Files from a directory
    :param directory: directory path
    :param formats: list of formats in string i.e. ['png', 'jpg']
    :return: iterator to all files
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if formats is None or file.split('.')[-1] in formats:
                yield directory + '/' + file


def extract_data_from_qr_code(image_path: str):
    """
    This function extracts data from qr_code image
    :param image_path: string path of image
    """
    for code in decode(cv2.imread(image_path)):
        data = code.data.decode('utf-8')
        yield data


def extract_all_data_from_qr_code(path_folder: str):
    """
    Extract qr codes from all the images in a directory
    :param path_folder: string of path folder containing images
    :return: list of datetime string extracted from qr_codes
    """
    data_list = []
    for image_path in get_all_files(path_folder, ['png']):
        data_list += list(extract_data_from_qr_code(image_path))
    return data_list


def save_data_into_sqlite(data: list, table_name: str, database_file_name: str, if_table_exist: str='append'):
    """
    Saves data into Sqlite database
    :param data: data comes as list within (i.e. [['date','time'],['date', 'time']])
    :param table_name: str
    :param database_file_name: str
    :param if_table_exist: if table exist what to do, append or drop
    """

    con = sqlite3.connect(database_file_name)
    cur = con.cursor()
    if if_table_exist == 'drop':
        cur.execute("DROP TABLE IF EXISTS {}".format(table_name))
    cur.execute('''CREATE TABLE IF NOT EXISTS {}
        (date text, time text)'''.format(table_name))

    cur.executemany(f"INSERT OR IGNORE INTO {table_name} VALUES (?, ?)", data)
    con.commit()
