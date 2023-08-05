# cgroupy
cgroupy is a python module that provides a simple intrface for managing cgroups

# Installation
You can install `cgroupy` using pip:

```
pip install cgroupy
```

# Usage
```
>>> from cgroupy import cgroup
>>> c = cgroup(1000,1000,'test')
>>> c.setup()
>>> c.execute('sleep 100', join=False)
[]
>>> c.execute('sleep 100', join=False)
[]
>>> c.tasks
{'8177', '8181'}
>>> c.teardown()
```

`with` syntax is also supported for automated setup and teardown:

```
>>> with cgroup(1000,1000,'test') as c:
...   c.execute('echo hello world')
... 
hello world
```
