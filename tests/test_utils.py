import os
from src.utils import save_data_into_sqlite, get_all_files, notify, extract_all_data_from_qr_code


def test_get_all_files():
    files_in_resources = ['qr_codes/4.png', 'qr_codes/5.png', 'qr_codes/6.png', 'qr_codes/2.png', 'qr_codes/3.png',
                          'qr_codes/1.png']
    assert list(get_all_files('qr_codes')) == files_in_resources


def test_save_data_into_sqlite():
    data = [['Dummy Date', 'Dummy Time']]
    assert save_data_into_sqlite(data, 'check_tb', 'check_db', if_table_exist='drop') is None
    assert save_data_into_sqlite(data, 'check_tb', 'check_db', if_table_exist='append') is None
    os.remove('check_db')


def test_notify():
    assert notify('Title', 'Description') is None


def test_extract_all_data_from_qr_code():
    directory = 'qr_codes'
    result_from_qr_codes = ['2022-08-02 08:00', '2022-08-02 12:00', '2022-08-02 18:00', '2022-08-01 12:00',
                            '2022-08-01 18:00', '2022-08-01 08:00']
    assert extract_all_data_from_qr_code(directory) == result_from_qr_codes
