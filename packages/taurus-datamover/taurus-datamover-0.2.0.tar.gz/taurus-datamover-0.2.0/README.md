# Taurus Datamover

Python wrapper for the [datamover tools](https://doc.zih.tu-dresden.de/data_transfer/datamover/) that enable moving data between the [ZIH fileserver](https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/datenspeicher/details) and the [taurus cluster](https://tu-dresden.de/zih/hochleistungsrechnen/hpc?set_language=en) at TU Dresden.

To facilitate temporary storage across computing nodes, also provides the `Workspace` wrapper for the [workspace tools](https://doc.zih.tu-dresden.de/data_lifecycle/workspaces/)

Before you can start working on the taurus cluster, you need to file a [project request](https://tu-dresden.de/zih/hochleistungsrechnen/hpc?set_language=en#section-1). You also need a [group share](https://tu-dresden.de/zih/dienste/service-katalog/arbeitsumgebung/datenspeicher/details#section-2) on the ZIH fileserver.

## Getting started

If you own a project space on taurus and want to transfer files to it, you can ask [HPC support](https://tu-dresden.de/zih/hochleistungsrechnen/support) to enable a connection to your fileserver.

Afterwards, you can use [TUD ZIH datamover](https://doc.zih.tu-dresden.de/data_transfer/datamover/) to transfer files from the fileserver to the cluster.

This python package provides a python wrapper for the datamover tools.

## Usage

### Datamover

First import `taurus_datamover` and create a `Datamover` object

```python
from taurus_datamover import Datamover, waitfor
dm = Datamover()
```
The object will have all datamover commands as methods. The most commonly used methods are: 
* `dtls` list directory contents. Equivalent of the the linux command `ls`.
* `dtcp` copy files like `cp`
* `dtmv` move files like `mv`
* `dtrm` delete files like `rm`

All commands take the same arguments like the linux equivalents. Arguments are passed as arguments to the method. For example, the `--help` option tells you how to use them:
```python
out, _ = dm.dtls('--help').communicate()
print(out.decode('utf-8'))
```
returns (truncated):
```
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
Sort entries alphabetically if none of -cftuvSUX nor --sort is specified.

Mandatory arguments to long options are mandatory for short options too.
  -a, --all                  do not ignore entries starting with .
  -A, --almost-all           do not list implied . and ..
      --author               with -l, print the author of each file
[...]
```

The `--help` argument is a little special, because it returns immediately. Normally, the commands run on a separate node in the background.

For example, listing the contents of the directory `/grp/g_biapol`
```python
proc = dm.dtls('-lh','/grp/g_biapol')
```
initially just prints some messages from the clusters queuing system:
```
srun: job 27549105 queued and waiting for resources
```
(some time passing here, until the job gets assigned to a node...)
```
srun: job 27549105 has been allocated resources
srun: error: ioctl(TIOCGWINSZ): Inappropriate ioctl for device
srun: error: Not using a pseudo-terminal, disregarding --pty option
```
the error messages are normal. they are caused by the fact that we did not run the command from an interactive terminal.

The whole process takes a while. therefore `Datamover` executes the commands in the background and returns immediately, so that you can do other stuff in the background. You can check the status with `poll()`. As long as that returns `None`, the process is still in progress:
```python
proc.poll()
```
```
None
```
And if the process finished it will return the exit code (0 in case of success, an integer larger than 0 in case of an error):
```python
proc.poll()
```
```
0
```

If your code needs to wait for the result, use the `waitfor` helper function, which waits for the result and returns the exit code of the command:

```python
proc = dm.dtls('-lh','/grp/g_biapol')
waitfor(proc)
```
```
Waiting ..
srun: job 27549647 queued and waiting for resources
......................................................................................................................
srun: job 27549647 has been allocated resources
.
srun: error: ioctl(TIOCGWINSZ): Inappropriate ioctl for device
srun: error: Not using a pseudo-terminal, disregarding --pty option
.
0
```
Only error messages are printed immediately, the normal output of the function is captured and can be retrieved like this:
```python
out, _ = proc.communicate()
print(out.decode('utf-8'))
```
```
total 12K
drwx------ 20 roha044c 1111111 4.0K Jul  8 13:59 data
drwx------  3 mazo260d 1111111 4.0K Jun 20 11:49 presentations
drwx------  3 johamuel 1111111 4.0K Mar 10 14:53 projects
```

### Examples

Recursively (`-r`) copy the directory `data/test` from the fileserver to the project space:
```python
waitfor(dm.dtcp('-r','/grp/g_biapol/data/test', '/projects/p_bioimage/'))
```

once it is done, we can see (and read) the files on the project space:
```python
!ls -la /projects/p_bioimage/test/
```
```
total 12
drwxrwsr-x 3 tkorten p_bioimage 4096 Aug  3 16:31 .
drwxrws--T 6 root    p_bioimage 4096 Aug  1 13:52 ..
drwx--S--- 2 tkorten p_bioimage 4096 Aug  3 16:31 test
```
However, from a normal node, we don't have write access:
```python
!rm -r /projects/p_bioimage/test/test
```
```
rm: cannot remove '/projects/p_bioimage/test/test': Read-only file system
```
But using the datamover, we can write to the project space:
```python
waitfor(dm.dtrm('-r', '/projects/p_bioimage/test'))
```
```
!ls -la /projects/p_bioimage/test/
```
```
ls: cannot access '/projects/p_bioimage/test/': No such file or directory
```


### Workspace

First import the workspace-related classes

```python
from taurus_datamover import Workspace, CacheWorkspace
ws = Workspace()
```

`Workspace` works very similar to Datamover, except that it provides access to the [workspace command line tools](https://doc.zih.tu-dresden.de/data_lifecycle/workspaces/):
* `ws_allocate` allocate a new workspace
* `ws_list` list existing workspaces for your user
* `ws_release` release an existing workspace (note all data on that workspace will be deleted within 1 day after releasing the workspace)

Let's create a workspace called `my-workspace` that expires automatically in 30 days:
```python
out, _ = ws.ws_allocate('my-workspace', '30').communicate()
workspace_path = out.strip().decode('utf-8')
```
`workspace_path` will look something like `/scratch/ws/0/username-my-workspace`

List existing workspaces with `ws_list`:
```python
out, _ = ws.ws_list().communicate()
print(out.strip().decode('utf-8'))
```
will return something like:
```
id: my-workspace
     workspace directory  : /scratch/ws/0/username-my-workspace
     remaining time       : 0 days 23 hours
     creation time        : Wed Aug 10 13:16:25 2022
     expiration date      : Thu Aug 11 13:16:25 2022
     filesystem name      : scratch
     available extensions : 10
```
And once we are done, we can release the workspace:
```python
ws.ws_release('my-workspace').wait()
```
This hides the workspace and all data will be deleted within 1d after you released the workspace.


`CacheWorkspace` is a convenience class for creating short-lived temporary workspaces. Instantiating it automatically creates a workspace with the id `cache`
```python
cws = CacheWorkspace()
```
Now you can work with the cache workspace, for example, you can create a temporary folder within:
```python
from tempfile import TemporaryDirectory
tmp = TemporaryDirectory(prefix=cws.name + '/')
tmp.name
```
```
/scratch/ws/0/username-cache/fgixyd8
```
cleaning up the cache (i.e. releasing the cache workspace) is simple:
```python
cws.cleanup()
```

If you only need the cache for a single piece of code, you can also use it as a context manager:
```python
with CacheWorkspace() as cws:
  temp_file = cws.name + '/temp.tiff'
  imsave(temp_file)
  target_file='/projects/my_project/data.tiff'
  dm.dtcp(temp_file, target_file)
```
That way, the cache workspace will be created and cleaned up automatically.

## Contributing
Contributions are very welcome. Tests can be run with tox, please ensure the coverage at least stays the same before you submit a pull request.

## License
Distributed under the terms of the BSD-3 license, "biapol-taurus" is free and open source software.

## Support
If you need support with the tools listed here, please [open an issue](https://gitlab.mn.tu-dresden.de/bia-pol/taurus-datamover/issues).
