Distbackup
==========

Distbackup is a tool that can back up a large set of files to a number of offline
disks. Only one backup disk needs to be connected at a time for distbackup to operate on
it. Distbackup will attempt to distribute redundant copies of files across the backup
disks, as long as there is room.

Installation
------------

Distbackup can be installed using PIP:

```
python3 -m pip install distbackup
```

If it fails, make sure you have Python, PIP, and OpenSSL development libraries
installed. On Ubuntu, run

```
sudo apt install python3-pip python3-dev python3-wheel libssl-dev
```

Distbackup uses `argcomplete` to assist with tab completion in your shell. To enable it
(for `bash`), run:

```
mkdir -p ~/.local/share/bash-completion/completions/
register-python-argcomplete --shell bash dsb > ~/.local/share/bash-completion/completions/dsb
```

Argcomplete also supports `tcsh` and `fish`. Run `register-python-argcomplete --help` for
more info.

How it works
------------

Distbackup maintains a database (SQLite) which contains metadata about every file in the
source set, including its name, last modified date, and a SHA256 hash of its
contents. The hash is then used to uniquely identify an "object", which is then copied to
one or more backup disks, along with a copy of the database itself.  The files on this
backup disk are stored only by their hash, so a restore requires reading the database to
reconstruct the original file structure.

The file structure on the backup disk looks like this:

```
├── distbackup-disk.json
├── distbackup,sqlite
├── distbackup-objects
│   ├── 000
│   │   ├── 0005e3d2a9216a465148b424de67297ad5ce65b95289294f3ef53c856ca55088
│   │   └── 000c00bad31d126b054c6ec7f3e02b27c0f9a4d579f987d3c4f879cee1bacb81
│   ├── 004
│   │   ├── 0046066f500854ebc1eb5d679a7164235de42efdf4dfbacff70d9bdb5a2d65db
│   │   └── 004cf775fda2783974afc1599c33b77228f04f7c053760f4a9552927207a064e
│   ├── 007
│   │   ├── 00702164a628a9e65266f4aafec2e1faebc42f0cc2145408a74c3feae39bef6d
│   │   └── 0077c553ae28326ef59c06e3743a6ddf5e046d9482eb9becfa8e06ff5bd37e2e
│   ├── 008
│   │   └── 0083cc2e1d1d989795d02aa47d4dd42b9f90b644d025cece0ab3c953b3a4fa09
.
.
.
```

Since objects are identified by their hash, their contents are immutable. This means that
if a source file changes, it will have a new hash and therefore refer to a new object.

Distbackup works with one backup disk at a time. First, it will delete any orphaned
objects (i.e. files that have been deleted or changed on the source), then it will copy
any new objects to the disk, and then, if it still has room, it will try to make redundant
copies of objects that have already been copied to other disks. It may delete redundant
objects off the disk to make room, as long as the overall redundancy is not reduced. For
example, if there is an object which already has one copy on another disk, it may decide
to delete an object that has two copies on other disks to make room for a second copy of
the first object.

Getting started
---------------

All distbackup commands are accessed via `dsb`. You can run `dsb --help` at any time to
get a list of commands.

Distbackup keeps its data in an SQLite database stored in `~/.config/distbackup/`. If you
want to use a different path, you can set the `DISTBACKUP_PATH` environment variable or
override it with `-d`. The first time you run distbackup, it will create the database
automatically.

First, you need to decide what files you want to back up. You can back up a single folder
or multiple folders spread out across different drives. You can "mount" a folder as a
specific path under the virtual tree with the `dsb source map` command:

```
# Make /media/photos/DCIM appear as /photos in the backup set
dsb source map /photos /media/photos/DCIM

# Another path, from your home folder
dsb source map /videos ~/Videos/recorded/

# You can "mount" directories within other virtual directories.
dsb source map /videos/stream-archive ~/livestream-archive
```

Once you have your source map set up the way you want it, run `dsb update` to scan the
source folders for files and record their metadata in the database. The first time you run
it, it will have to read every file to generate a hash. You can let this process run in
the background while you continue setup. If the hashing process is interrupted, it will
pick up where it left off the next time you run `dsb update` and won't have to rehash any
files unless their contents have changed.

Next, you need to find some disks to use as a backup. Each disk needs to have a unique
name, even if it's just `distbackup-01`, `distbackup-02`, etc.  I highly recommend
physically labelling each disk with its name so it's easy to find. I also recommend
setting the volume label on the disk as well, though distbackup does not require that.

Note: If your disks are formatted as ext4, you should set the "reserved blocks" to
zero. By default, ext4 reserves 5% for the root user, which for a 6TB disk is 300GB, an
insane amount for a data disk. You can use `tune2fs -m 0` to clear it.

Once you have your disk connected, formatted, and mounted, it's time to make distbackup
aware of it:

```
ktpanda@desktop:~$ dsb disk add distbackup-01 /media/distbackup-01/distbackup/
Added disk distbackup-01:
  UUID: db74b831-bd09-434f-ac9b-bc427dfc5628
  Nexus index: 0
  Size: 7,927,384,932,352
  Mount point (current): /media/distbackup-01
  Relative path from mountpoint: distbackup
```

The size, if not specified, defaults to 10GB less than the total size of the disk. If you
want to set a specific size (e.g. to reserve more space for other files), you can specify
`--size` when adding the disk or with the `dsb disk set` command:

```
dsb disk set distbackup-01 --size 7.4T
```

Once you have all your disks set up, and `dsb update` completes, you're ready to start
backing up! Just run `dsb backup distbackup-01`, and it will start copying files until it
hits the size limit of the disk, or it runs out of files to copy.
