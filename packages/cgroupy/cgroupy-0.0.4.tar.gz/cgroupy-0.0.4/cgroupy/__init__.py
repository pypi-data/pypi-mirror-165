import os
import sys
import uuid
import shutil
import subprocess
import time

class cgroup(object):

  """
  simple implementation of a cgroup. support creating a cgroup with memory 
  and cpu limits, and the running processes inside of that cgroup
  """
  def __init__(self, cpu, memory, name):

    self.cpu = cpu
    self.memory = memory * 1024 * 1024
    self.name = name
    self.cgroup_root = os.environ.get('CGROUP_ROOT')
    if not self.cgroup_root:
        self.cgroup_root = 'cgroupy'
    self.cpu_path = "/sys/fs/cgroup/cpu/{}/{}".format(self.cgroup_root, self.name)
    self.memory_path = "/sys/fs/cgroup/memory/{}/{}".format(self.cgroup_root, self.name)

  def setup(self):
    # Check if cgroup already exists or not
    if not self.exists:
      # Set up cgroup
      os.makedirs(self.cpu_path)
      with open("{}/cpu.shares".format(self.cpu_path), 'w+')  as fh:
        fh.write(str(self.cpu))

      print("{}/memory.limit_in_bytes".format(self.memory_path))
      os.makedirs(str(self.memory_path))
      with open("{}/memory.limit_in_bytes".format(self.memory_path), 'w')  as fh:
        fh.truncate()
        fh.write(str(self.memory).strip())
 
  @property
  def tasks(self):
    tasks = []
    for path in (self.cpu_path, self.memory_path):
      tasks_file = "{}/tasks".format(path)
      with open(tasks_file, 'r') as fh:
        for line in fh.readlines():
          tasks.append(line.strip())
    return set(tasks)

  @property 
  def exists(self):
    for path in (self.cpu_path, self.memory_path):
      if not os.path.exists(path):
        return False
    return True

  def __enter__(self):
    self.setup()
    return self

  def __exit__(self, type, value, traceback):
    self.teardown()

  def teardown(self):
    print("Performing Teardown...")
    os.rmdir(self.cpu_path)
    os.rmdir(self.memory_path)

  def execute(self, command, join=True):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    self.add_pid(process.pid)
    return process
 
  def add_pid(self, pid):
    for path in (self.cpu_path, self.memory_path):
      tasks_file = "{}/tasks".format(path)
      with open(tasks_file, 'a') as fh:
        fh.write(str(pid)) 
