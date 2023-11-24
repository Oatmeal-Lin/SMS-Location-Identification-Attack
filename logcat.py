# SEND SMS logs
import csv
import subprocess
import sys
import re
import time
from datetime import datetime

ADB_ID = 'SED0221625000077'

ADB_PATH = 'ADB_PATH'

HEADER_LIST = ["NO", "sender_phone", "sender_num", "sender_address",
               "receiver_phone", "receiver_num", "receiver_address",
               "SEND_1", "SEND_2", "SEND_3",
               "ACKNOWLEDGEMENT_1", "ACKNOWLEDGEMENT_2",
               "REPORT_1", "REPORT_2"]


def is_keyword(line):
    keyword = {"SEND_1": "sendImsSms: serial", "SEND_2": ">AT+CMMS=", "SEND_3": ">AT+CMGS=",
               "ACKNOWLEDGEMENT_1": "sendImsSmsResponse: serial", "ACKNOWLEDGEMENT_2": "< IMS_SEND_SMS",
               "REPORT_1": "<+CDS:", "REPORT_2": "< UNSOL_RESPONSE_NEW_SMS_STATUS_REPORT"}

    for key, value in keyword.items():
        if value in line:
            regex = "\\d{1,2}-\\d{1,2}\\s\\d{1,2}:\\d{1,2}:\\d{1,2}.\\d{1,3}"
            t = re.search(regex, line)[0]
            return key, get_time(t)
    return "", ""


def is_new_line(datalist, key):
    flag = False
    for i in HEADER_LIST:
        if not flag:
            if key == i:
                flag = True
        else:
            if datalist[i]:
                return True
    return False


def get_from_radio_txt(path):
    init_csv()
    index = 0

    f = open(path, encoding="UTF-8")
    lines = f.readlines()
    data_list = init_data_list(index)

    for line in lines:
        key, t = is_keyword(line)
        if key:
            if is_new_line(data_list, key):
                write_csv(data_list)
                index = index + 1
                data_list = init_data_list(index)
            data_list[key] = t
    write_csv(data_list)


def get_time(t):
    d = datetime.strptime("2023-" + t, "%Y-%m-%d %H:%M:%S.%f")
    return (time.mktime(d.timetuple())) + d.microsecond / 1000000.0


def run_shell(shell):
    init_csv()
    index = 0

    cmd = subprocess.Popen(shell, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    while True:
        line = cmd.stdout.readline()
        ln = line.decode("UTF-8").strip("b'").strip("\n")

        data_list = init_data_list(index)

        key, t = is_keyword(ln)

        if key:
            if is_new_line(data_list, key):
                write_csv(data_list)
                index = index + 1
                data_list = init_data_list(index)
            data_list[key] = t

        if line == b'' or subprocess.Popen.poll(cmd) == 0:
            cmd.stdout.close()
            break

    write_csv(data_list)


def init_data_list(index):
    return {"NO": index,
            "sender_phone": "huawei-p50-pro", "sender_num": "", "sender_address": "xicun-c3",
            "receiver_phone": "iphone13p", "receiver_num": "15985778118", "receiver_address": "xicun-c3",
            "SEND_1": "", "SEND_2": "", "SEND_3": "",
            "ACKNOWLEDGEMENT_1": "", "ACKNOWLEDGEMENT_2": "",
            "REPORT_1": "", "REPORT_2": ""}


def init_csv():
    with open("data.csv", mode="a+", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, HEADER_LIST)
        writer.writeheader()


def write_csv(data):
    with open("data.csv", mode="a+", encoding="UTF-8", newline="") as f:
        writer = csv.DictWriter(f, HEADER_LIST)
        writer.writerow(data)


if __name__ == '__main__':
    print(run_shell(ADB_PATH + " -s " + ADB_ID + " logcat -b radio"))
    # get_from_radio_txt("./radio2.txt")
