# cgroupy
cgroupy is a python module that provides a simple interface for managing cgroups

# Installation
You can install `cgroupy` using pip:

```
pip install cgroupy
```

# Usage

`cgroupy` impelemets a `cgroup` object. This object can be used to both create a new cgroup, and to interact with an existing one.  When you initialize a `cgroup` object, you cand specify the CPU and memory limits you wish to set. Memory is specified in megabytes, and CPU limits are specified in CPU shares/megahertz.

Once a `cgroup` object is initialized, you can check if it exists, create it if it does not, run processes inside it, and destroy it like so:

```
>>> from cgroupy import cgroup
>>> c = cgroup('test', memory=1000, cpu=1000)
>>> c.exists
False
>>> c.setup()
>>> c.exists
True
>>> process = c.execute('echo hello world')
>>> print(process.communicate())
(b'hello world\n', b'')
>>> c.teardown()
>>> c.exists
False
```
IN addition to the `cgroup.execute` method that lets you run an arbitrary command inside of your cgroup, you can add a running PID to the cgroup, or launch new processes from python and add them:
```
>>> from cgroupy import cgroup
>>> import multiprocessing
>>> import time
>>> def test():
...   time.sleep(150)
... 
>>> c = cgroup('test')
>>> c.setup()
>>> p = multiprocessing.Process(target=test)
>>> p.start()
>>> c.add_pid(p.pid)
>>> c.add_pid(p.pid)
>>> c.tasks
{'17202'}
>>> p.pid
17202
```

`with` syntax is also supported for automated setup and teardown:

```
>>> with cgroup('test', memory=1000, cpu=500) as c:
...   c.execute('echo hello world')
 
(b'hello world\n', b'')
```
