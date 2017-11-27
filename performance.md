---
layout: default
title: Performance
permalink: /performance/
---
Performance varies considerably based on the complexity of the rendered content, the amount of dynamic content on the page, the size of the produced output and many other factors.

TemPy does not parse strings, does not use regex and does not load .html files, resulting in great speed compared to the traditional frameworks such as Jinja2 and Mako.

Here are a few benchmarks of TemPy in action, used in a Flask app, rendering a template (see code [here](benchmarks))
Used HW: 2010 IMac, CPU:2,8 GHz Intel Core i7 RAM:16 GB 1067 MHz DDR3 Osx: 10.12.6.
Benchmark made using [WRK](https://github.com/wg/wrk)

![TemPy Web Rendering](bench.jpg)

Running 20s test @ http://127.0.0.1:8888/tempy + http://127.0.0.1:8888/j2
  10 threads and 200 connections


Tempy | Avg | Stdev | Max | +/- Stdev
----- | --- | ----- | --- | ---------
Latency | 109.55ms | 52.04ms | 515.33ms | 93.09%
Req/Sec | 118.27 | 37.36 | 240.00 | 73.77%

16111 requests in 20.09s, 96.23MB read
Requests/sec: 801.91
Transfer/sec: 4.79MB

Jinja2 | Avg | Stdev | Max | +/- Stdev
----- | --- | ----- | --- | ---------
Latency | 216.04ms | 16.05ms | 267.06ms | 91.16%
Req/Sec | 59.29 | 20.53 | 151.00 | 71.23%

11841 requests in 20.08s, 72.80MB read
Requests/sec:    589.70
Transfer/sec:      3.63MB

Performance difference is even higher in Jinja2 plain (no Flask) rendering:
![TemPy No-Web Rednering](bench_plain.jpg)