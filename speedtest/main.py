import speedtest
import xlwt
from datetime import datetime
import os
import shelve
import time

stt = speedtest.Speedtest()


class AppTestSpeed:
    def __init__(self, bin_file_name, xlsx_file_name):
        self.test_result = self.test_speed()
        self.save_result(bin_file_name)
        self.write_to_xlsx(bin_file_name, xlsx_file_name)
        self.print_to_console()

    def print_to_console(self):
        print("{} : down - {:.1f}, up - {:.1f}".format(self.test_result[1],
                                                       self.test_result[2],
                                                       self.test_result[3]))

    def test_speed(self):
        st = speedtest.Speedtest()
        now = datetime.now()
        best = st.get_best_server()
        divider = 1_000_000
        return (now.strftime("%d.%m"), now.strftime("%H:%M"),
                st.download() / divider, st.upload() / divider, best["host"])

    def save_result(self, path):
        if os.path.isfile(path + ".dat"):
            with shelve.open(path) as f:
                temp = f["result"]
                temp.append(self.test_result)
                f["result"] = temp
        else:
            with shelve.open(path) as f:
                f["result"] = [self.test_result]

    def write_to_xlsx(self, bin_path, xlsx_path):
        if not os.path.isfile(bin_path + ".dat"):
            return

        with shelve.open(bin_path) as f:
            data = f["result"]
        wb = xlwt.Workbook()
        ws = wb.add_sheet("result")

        ws.write(0, 0, "Date")
        ws.write(0, 1, "Time")
        ws.write(0, 2, "Download speed mbit/s")
        ws.write(0, 3, "Upload speed mbit/s")
        ws.write(0, 4, "Host")

        for i in range(len(data)):
            row = i + 1
            ws.write(row, 0, data[i][0])
            ws.write(row, 1, data[i][1])
            ws.write(row, 2, data[i][2])
            ws.write(row, 3, data[i][3])
            ws.write(row, 4, data[i][4])

        wb.save(xlsx_path)


if __name__ == '__main__':
    while True:
        AppTestSpeed("result", "result.xls")
        time.sleep(60*10)
