import os
import sys
import time
import uuid
import shutil
import logging
import subprocess


class cgroup(object):

  """
  simple implementation of a cgroup. support creating a cgroup with memory 
  and cpu limits, and the running processes inside of that cgroup
  """
  def __init__(self, cpu, memory, name):

    self.logger = logging.getLogger('cgroupy')
    self.cpu = cpu
    self.memory = memory * 1024 * 1024
    self.name = name
    self.logger.debug("Memory Limit: {}".format(self.memory))
    self.logger.debug("CPU Limit: {}".format(self.cpu))
    self.logger.debug("CGroup Name: {}".format(self.name))
    self.cgroup_root = os.environ.get('CGROUP_ROOT')
    if not self.cgroup_root:
        self.cgroup_root = 'cgroupy'
    self.logger.debug("CGroup root path: {}".format(self.cgroup_root))
    self.cpu_path = "/sys/fs/cgroup/cpu/{}/{}".format(self.cgroup_root, self.name)
    self.memory_path = "/sys/fs/cgroup/memory/{}/{}".format(self.cgroup_root, self.name)

  def setup(self):
    # Check if cgroup already exists or not
    if not self.exists:
      self.logger.info("Creating cgroup at paths: /sys/fs/(cpu,memory)/{}/{}...".format(self.cgroup_root, self.name))
      # Set up cgroup
      os.makedirs(self.cpu_path)
      self.logger.info("Writing CPU Limit of {}  to: {}...".format(self.cpu, self.cpu_path))
      with open("{}/cpu.shares".format(self.cpu_path), 'w+')  as fh:
        fh.write(str(self.cpu))
      self.logger.info("Writing memory Limit of {} to: {}...".format(self.memory, self.memory_path))
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
    self.logger.info("Performing Teardown...")
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
