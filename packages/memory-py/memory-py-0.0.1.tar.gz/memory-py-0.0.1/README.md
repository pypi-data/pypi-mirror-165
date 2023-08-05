# `memory`

Approximate memory usage profiler.

## Usage

```
time memory sleep 1
```

Output:

```
rss          0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M
vms         16M     16M     16M     16M     16M     16M     16M     16M     16M     16M     16M
shared       0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M
text         0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M
lib          0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M
data         0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M
dirty        0M      0M      0M      0M      0M      0M      0M      0M      0M      0M      0M

real    0m1.081s
user    0m0.127s
sys     0m0.094s
```

## Install

```
pip3 install memory-py
```
