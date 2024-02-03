import subprocess
import sys
import platform
import csv
import requests
from random import randint
from tabulate import tabulate


# Set CMD commands depend on the OS platform
REMOVE_CMD = "rm"
CLEAR_CMD = "clear"
COMBINE_CMD = ";"
if platform.system() == "Windows":
  REMOVE_CMD = "del"
  CLEAR_CMD = "cls"
  COMBINE_CMD = "&"


# Clear workspace
def clear_prework():
  subprocess.run(f"{REMOVE_CMD} warp*.conf {COMBINE_CMD} {REMOVE_CMD} Result.csv {COMBINE_CMD} {CLEAR_CMD}", shell=True)


# Print introduction
def print_introduction():
  text = """Hello! This is my project for CS50P Course. Using this script, you can find the fastest endpoints for Cloudflare WARP servers.
Also, you can generate Wireguard profiles with these endpoints.

This project uses API Zeroteam (https://shop.zeroteam.top/) by ZeroCloud
and
CloudflareWarpSpeedTest (https://github.com/peanut996/CloudflareWarpSpeedTest) by Peanut996

This tool is not affiliated with or endorsed by Cloudflare. Please use it responsibly and comply with their terms of service."""
  print(text)


# Get platform
def check_platform():
  SUPPORT_OS = ["Windows", "Darwin", "Linux"]
  SUPPORT_CPU = ["AMD64", "x86_64"]

  os = platform.system()
  cpu = platform.machine()

  if os not in SUPPORT_OS:
    sys.exit("Unsupported operating system")
  if cpu not in SUPPORT_CPU:
    sys.exit("Unsupported CPU")

  return os


# Get answer
def get_answers():
  task = input("\nWhat kind of result should I output?: \n" \
               "1. Print N best latency endpoints.\n" \
               "2. Write N best latency endpoints to the file.\n" \
               "3. Create N Wireguard profiles with best endpoints.\n" \
               "4. Create N Wireguard profiles with default endpoint.\n" \
               "Answer: "
               ).strip()

  print()

  if task == '1':
    task = "print"
    string = "How many IP do you want to print?\nAnswer: "
  elif task == "2":
    task = "write"
    string = "How many IP do you want to save in the file?\nAnswer: "
  elif task == "3":
    task = "profiles"
    string = "How many profiles do you want to create?\nAnswer: "
  elif task == "4":
    task = "profiles-default"
    string = "How many profiles do you want to create?\nAnswer: "
  else:
    sys.exit("Invalid task!")

  try:
    amount = int(input(string))
  except ValueError:
    sys.exit("Invalid number!")

  ip_type = input("\nChoose the type of the IP version:\n" \
                  "1. IPv4 \n" \
                  "2. IPv6 \n" \
                  "3. Combined \n" \
                  "Answer: " \
                  ).strip()

  print()

  if ip_type == "1":
    ip_type = "IPv4"
  elif ip_type == "2":
    ip_type = "IPv6"
  elif ip_type == "3":
    ip_type = "Combined"
  else:
    sys.exit("Invalid type!")

  return {"ip_type": ip_type, "task": task, "amount": amount}


# Generate IPv4 list
def generate_ipv4_list():
  MAX_N = 255
  BASEIP_LIST = ["162.159.192", "162.159.193", "162.159.195", "162.159.204",
                  "188.114.96", "188.114.97", "188.114.98", "188.114.99"
                 ]
  ip_list = []

  for baseip in BASEIP_LIST:
    for i in range(MAX_N):
      ip = baseip + "." + str(i)
      ip_list.append(ip)

  return ip_list


# Generate IPv6 list
def generate_ipv6_list():
  LIST_LEN = 1000
  BASEIP_LIST = ["2606:4700:d0::", "2606:4700:d1::"]
  ip_list = []

  for i in range(LIST_LEN):
      base_ip = BASEIP_LIST[i // (LIST_LEN // len(BASEIP_LIST))]
      ip = base_ip

      for j in range(4):
        ip += generate_ipv6_segment()
        if j != 3:
          ip += ":"

      if ip in ip_list:
        continue

      ip_list.append(ip)

  ip_list.sort()

  return ip_list


# Generate IPv6 segment
def generate_ipv6_segment():
  segment = (randint(0, 32767) * 2) + (randint(0, 32767) % 2)
  segment = format(segment, 'x')
  segment = str(segment)

  return segment


# Write IP list to a temporary file
def write_ip_list(ip_list):
  with open(".tmp1", "w") as file:
    for ip in ip_list:
      file.write(f"{ip}\n")


# Run speed test binary
def run_speedtest(platform):
  if platform not in ["Windows", "Linux", "Darwin"]:
    sys.exit("Invalid platform!")

  test_mode = input("What type of the speed test do you want? \n" \
                    "1. Quick test (test random addreses) \n" \
                    "2. Full test (test all addreses, can take up to 5 minutes, but find best IP) \n" \
                    "Answer: " \
                   )
  print()

  if test_mode == "1":
    run_string = "./HOLDER -f .tmp1 -q=true -t 8 -n 200 -p 0 -o .tmp2"
  elif test_mode == "2":
    run_string = "./HOLDER -f .tmp1 -q=false -t 2 -n 200 -p 0 -o .tmp2"
  else:
    sys.exit("Invalid mode!")

  if platform == "Windows":
    run_string = run_string.replace("./HOLDER", "speedtest_windows.exe")
  elif platform == "Linux" or platform == "Darwin":
    subprocess.run(f"chmod +x speedtest_{platform.lower()}", shell=True)
    run_string = run_string.replace("HOLDER", f"speedtest_{platform.lower()}")

  subprocess.run(run_string, shell=True)


# Load values from the result file
def load_values(amount):
  data_table = []

  try:
    file = open(".tmp2", "r")
  except FileNotFoundError:
    sys.exit("Can't connect to the server! Check your Internet connection")

  csv_reader = csv.DictReader(file)
  for row, n in zip(csv_reader, range(amount)):
    data_table.append({"N": n + 1, "IP:Port": row["IP:Port"], "Latency": row["Latency"]})

  return data_table


# Print top N IP addreses ranking by latency
def print_top(data_table):
  titles = ["#", "IP:Port", "Latency"]
  print_list = []
  for row in data_table:
    print_list.append([row["N"], row["IP:Port"], row["Latency"]])

  print(tabulate(print_list, headers=titles, tablefmt="mixed_grid"))


# Write to the file top N IP addreses ranking by latency
def write_result_file(data_table):
  file_name = "Result.csv"
  fields = ["Endpoint", "Latency"]

  with open(file_name, "w") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerow(fields)
    for ip in data_table:
      csvwriter.writerow([ip["IP:Port"], ip["Latency"]])

  print(f"Done! IP saved in file {file_name}")


# Create profiles
def create_profiles(data_table, mode):
  amount = len(data_table)
  
  if mode == "profiles":
    mtu = get_mtu()

  for n in range(amount):
    # Get new generated profiles by API ZeroTeam
    print(f"Creating {n+1} of {amount} profile...")
    data = requests.get("https://api.zeroteam.top/warp?format=wireguard").text

    if mode == "profiles":
      data = data.replace("engage.cloudflareclient.com:2408", data_table[n]["IP:Port"])
      data = data.replace("MTU = 1280", f"MTU = {mtu}")

    with open(f"warp{n}.conf", "w") as file:
      file.write(data)

  subprocess.run(f"{CLEAR_CMD}", shell=True)

  print(f"Done! {amount} profiles created")


# Get MTU value
def get_mtu():
  answer = input("\nWhat MTU value do you want to set?\n" \
                     "1. MTU 1280. Default, stable, work in most cases\n" \
                     "2. MTU 1500. Sometimes much much more perfomance\n" \
                     "3. Your value\n"
                     "Answer: "
                    )
  subprocess.run(f"{CLEAR_CMD}", shell=True)

  if answer == "1":
    mtu = "1280"
  elif answer == "2":
    mtu = "1500"
  elif answer == "3":
    mtu = input("\nType your MTU value: ")
    try:
      if int(mtu) < 1:
        sys.exit("Invalid MTU Value")
    except ValueError:
      sys.exit("Invalid MTU value!")
  else:
    sys.exit("Invalid answer!")

  return mtu


# Clean temp files
def clear_postwork():
  subprocess.run(f"{REMOVE_CMD} .tmp1 {COMBINE_CMD} {REMOVE_CMD} .tmp2 {COMBINE_CMD} {CLEAR_CMD}", shell=True)


# Main function
def main():
  clear_prework()

  print_introduction()
  platform = check_platform()

  answers = get_answers()
  task = answers["task"]

  if answers["ip_type"] == "IPv4":
    ip_list = generate_ipv4_list()
  elif answers["ip_type"] == "IPv6":
    ip_list = generate_ipv6_list()
  elif answers["ip_type"] == "Combined":
    ip_list = generate_ipv4_list() + generate_ipv6_list()

  write_ip_list(ip_list)

  run_speedtest(platform)

  data_table = load_values(answers["amount"])

  clear_postwork()

  if task == "print":
    print_top(data_table)
  elif task == "write":
    write_result_file(data_table)
  elif task in ["profiles", "profiles-default"]:
    create_profiles(data_table, task)


if __name__ == "__main__":
  main()
