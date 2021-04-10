import speedtest
import xlwt
from datetime import datetime


def make_test():
    st = speedtest.Speedtest()

    best = st.get_best_server()
    down_bits = st.download()
    print("1")
    up_bits = st.upload()
    print("2")

    return down_bits, up_bits, best["host"]


def app():
    now = datetime.now()
    now_day_month = now.strftime("%d.%m")
    now_time = now.strftime("%H:%M")
    down_bits, up_bits, host= make_test()
    down_mbit = down_bits / 1000000
    up_mbit = up_bits / 1000000

    print("{} {} {:.1f} {:.1f} host: {}".format(now_day_month, now_time, down_mbit, up_mbit, host))


if __name__ == '__main__':
    app()
