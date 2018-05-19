import subprocess
import os
import sys


#directory = "test_dir"
directory_grafana = "/tmp/son-monitor/grafana"
directory_prometheus = "/tmp/son-monitor/prometheus"
dirs = [directory_grafana, directory_prometheus]
#print(os.path.exists(directory))

for e in dirs:
  if not os.path.exists(e):
    os.makedirs(e)

for e in dirs:
  process = subprocess.Popen(['chmod', '775', e])
  process.wait()

