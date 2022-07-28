"""
Main
----
"""
from queue import PriorityQueue
from datetime import datetime
import time
from src.utils import extract_all_data_from_qr_code, save_data_into_sqlite, notify

SLEEP_TIME = 10  # in seconds
QR_CODES_DIR = 'qr_codes'
DATABASE_NAME = 'kl_health.db'
TABLE_NAME = 'notifications'

NOTIFICATION_TITLE = 'KL Health Care'
NOTIFICATION_DESCRIPTION = 'Its time to take medication!'


def main():
    """
    KL Health Notification Program
    """
    data_list = extract_all_data_from_qr_code(QR_CODES_DIR)
    data = []
    for i in data_list:
        data.append(i.split())
    save_data_into_sqlite(data, TABLE_NAME, DATABASE_NAME, if_table_exist='drop')

    q = PriorityQueue()
    for i in data_list:
        q.put(datetime.strptime(i, '%Y-%m-%d %H:%M'))

    while True:
        if q.empty():
            break
        notification = q.get()
        while True:
            if notification <= datetime.now():
                notify(NOTIFICATION_TITLE, NOTIFICATION_DESCRIPTION)
                break
            else:
                time.sleep(SLEEP_TIME)


if __name__ == '__main__':
    main()
