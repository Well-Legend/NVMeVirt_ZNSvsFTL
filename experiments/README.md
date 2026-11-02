# Recovered experiment context

The original report compares conventional FTL + F2FS with ZNS + ZoneFS. Screenshots are original evidence under `results/screenshots/`; the final guest command history also contains F2FS/ZNS setup attempts that failed. It must not be treated as a tested installation script.

Observed fio parameters include sequential writes, `bs=128k`, four jobs and group reporting; the guest history contains several sizes (100M, 200M, 1G). Report screenshots are the authority for each individual run. Do not combine unlike workloads into a new comparison.

The report's parallelism table states F2FS average/max active I/O of 1/1, versus ZoneFS about 3–4/4. These are the original author's reported values, not rerun results and not independently verified hardware NAND parallelism. The recovered code increments counters around the command handler. Its peak update is not an atomic compare-and-swap maximum, so concurrent updates can lose a peak; the counters are not a direct measurement of physical NAND die occupancy. No new raw fio JSON or dmesg logs were found; screenshots are retained without synthesizing such data.

To rerun, first prepare a disposable Linux guest, reserve memory in GRUB according to `environment/`, build one module mode, and verify the resulting emulated block device. Filesystem formatting destroys target data: explicitly identify the NVMeVirt test device and keep the system disk out of the experiment. The original module parameters include `memmap_start=7G`, `memmap_size=4097M` and `cpus=0,1`; these are historical settings and require a compatible guest memory map. They are not portable defaults.

For new evidence, record kernel/compiler versions, NVMe identify output, full fio command/JSON output, mount/filesystem options and dmesg counters per run. Keep FTL and ZNS runs matched in request size, job count, I/O depth, data size and preconditioning. The recovery process does not load modules, format a device or rerun benchmarks.
