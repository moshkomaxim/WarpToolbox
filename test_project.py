import sys
import pytest
import re
import os
from tabulate import tabulate
from project import clear_prework
from project import print_introduction
from project import check_platform
from project import get_answers
from project import generate_ipv4_list
from project import generate_ipv6_list
from project import generate_ipv6_segment
from project import write_ip_list
from project import run_speedtest
from project import load_values
from project import print_top
from project import write_result_file
from project import create_profiles
from project import get_mtu
from project import clear_postwork


def test_clean_prework():
    clear_prework()
    assert not os.path.exists("Result.csv")
    assert not os.path.exists("warp0.conf")


def test_print_introduction(capfd):
    text = """Hello! This is my project for CS50P Course. Using this script, you can find the fastest endpoints for Cloudflare WARP servers.
Also, you can generate Wireguard profiles with these endpoints.

This project uses API Zeroteam (https://shop.zeroteam.top/) by ZeroCloud
and
CloudflareWarpSpeedTest (https://github.com/peanut996/CloudflareWarpSpeedTest) by Peanut996

This tool is not affiliated with or endorsed by Cloudflare. Please use it responsibly and comply with their terms of service.\n"""

    print_introduction()
    out, err = capfd.readouterr()
    assert out == text


def test_check_platform():
    SUPPORT_OS = ["Windows", "Darwin", "Linux"]
    os = check_platform()

    assert os in SUPPORT_OS


def test_get_answers(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "test")
    with pytest.raises(SystemExit):
        get_answers()


def test_generate_ipv4_list():
    BASEIP_LIST = ["162.159.192", "162.159.193", "162.159.195", "162.159.204",
                  "188.114.96", "188.114.97", "188.114.98", "188.114.99"
                  ]
    ip_list = generate_ipv4_list()

    for baseip in BASEIP_LIST:
        for i in range(255):
            ip = baseip + '.' + str(i)
            try:
                assert ip in ip_list
            except AssertionError:
                sys.exit("Generated ipv4 address is wrong!")


def test_generate_ipv6_list():
    ip_list = generate_ipv6_list()

    assert len(ip_list) == 1000
    for ip in ip_list:
        check = re.search(r"^2606:4700:d[0,1]::[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}$", ip)
        assert check


def test_generate_ipv6_segment():
    segment = generate_ipv6_segment()
    check = re.search(r"^[0-9A-Fa-f]{1,4}$", segment)
    assert check


def test_write_ip_list():
    ip_list = ["1.1.1.1", "1.0.0.1"]
    write_ip_list(ip_list)

    with open(".tmp1") as file:
        for ip in file:
            assert ip.replace("\n", "") in ip_list


def test_speedtest():
       with pytest.raises(SystemExit):
         run_speedtest("Invalid")


def test_load_values():
    with open(".tmp2", "w") as file:
        file.write("IP:Port,Loss,Latency\n")
        file.write("162.159.195.140:5279,0%,2.22\n")

    data_table = load_values(1)

    assert data_table[0]["IP:Port"] == "162.159.195.140:5279"


def test_print_top(capfd):
    titles = ["#", "IP:Port", "Latency"]
    data = {"N": 0, "IP:Port": "162.159.195.140:5279", "Latency": "40"}

    print_top([data])
    out, err = capfd.readouterr()

    check = tabulate([[data["N"], data["IP:Port"], data["Latency"]]], headers=titles, tablefmt="mixed_grid")
    check += "\n"
    assert check == out


def test_write_result_file():
    data = [{"N": 0, "IP:Port": "162.159.195.140:5279", "Latency": "40"}]

    write_result_file(data)

    assert os.path.exists("Result.csv")


def test_create_profiles():
    data = [{"N": 0, "IP:Port": "162.159.195.140:5279", "Latency": "40"},
            {"N": 1, "IP:Port": "162.159.195.140:5279", "Latency": "40"}]

    create_profiles(data, "profiles-default")

    assert os.path.exists("warp0.conf")
    assert os.path.exists("warp1.conf")


def test_get_mtu(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "1")
    assert get_mtu() == "1280"


def test_clear_postwork():
    clear_postwork()
    assert not os.path.exists(".tmp1")
    assert not os.path.exists(".tmp2")


if __name__ == "__main__":
    main()

