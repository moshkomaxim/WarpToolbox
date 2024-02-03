# Warp_speed_toolbox

## Video Demo: https://youtu.be/2YLWz737crk

## Introduction
This project is created for CS50P Course.
This is a command-line tool for a bit of tasks, related to the listing & sorting & checking Cloudflare WARP endpoints.

Early version of this script helped me when I was in the occupied territory of Ukraine. I specially design this tool to create a large amount of profiles with fastest endpoints, because a lot of people was requiring it. This was the only way to access the free Internet, because a large portion of the Web is blocking here, including Google, Youtube, Facebook, Twitter, and etc. They are still blocking them...

This project uses API Zeroteam by [ZeroCloud](https://shop.zeroteam.top/)
and
[CloudflareWarpSpeedTest](https://github.com/peanut996/CloudflareWarpSpeedTest) by Peanut996. Thanks to all of them!

## DISCLAIMER
This tool is not affiliated with or endorsed by Cloudflare. Please use it responsibly and comply with their terms of service.

## Description:
The tool has four main functions/tasks:

- Print N best endpoints sorted by latency.
- Write N best endpoints sorted by latency.
- Create N Wireguard profiles with best endpoints sorted by latency.
- Create N Wireguard profiles with default endpoints.

It built as interactive program. You should answer on the some questions:

- Select your task
- Type amount of IP addresses to process
- Choose the type of IP addresses (IPv4, IPv6 or combined)
- Type of speed/latency test (quick or full). It is performed by the CloudflareWarpSpeedTest binaries
- Also, if you are creating Wireguard profiles with custom endpoints, it ask you about desired MTU size.

## Limitations
This project has some limitations:

- Doesn't support custom filenames (i wanted to keep program as simple as possible)
- Doesn't check endpoint's speed. It checks only latency.
- Doesn't support different speed test modes. It supports only quick mode (scan only 1000 random endpoints from the list) and full mode (scan ALL possible endpoints, take a lot of time). This is due to the limitations of the CloudflareWarpSpeedTest.
- Doesn't support command line flags, and work only as interactive program.
- Doesn't scan full IPv6 range. It is too long

## Plans

I have much more plans for this project:

- Use my own implementation of the speed test
- Possible rebuild program to work using command line flags, not by the interactive input.
- Add checking for the speed of the endpoints, not only latency

If you have any questions - you can write me: moshkomaxim@gmail.com

## License

This software is released under the [GPL v3 license](LICENSE).


