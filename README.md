# NVMeVirt with ZNS vs. Traditional FTL

Implementation and original experiment evidence recovered from a powered-off VirtualBox guest. The repository preserves the actual modified driver, its upstream revision, build settings, filesystem tooling, report and screenshots. Large VDI images and reproducible fio filler files are excluded.

## Source and changes

The source comes from [SNU CSL NVMeVirt](https://github.com/snu-csl/nvmevirt), pinned at **c93e88c374917610ba6d8cc474e0376a9911ce0b**. `vendor/nvmevirt/` preserves the final saved guest worktree. Local changes select ZNS in Kbuild, set one die per zone and 256 MiB zones, and add command-handler I/O counters. `patches/recovered-local-changes.patch` separates those changes from upstream.

| Path | Content |
|---|---|
| `vendor/nvmevirt/` | Actual recovered source, retaining upstream license and README |
| `vendor/zonefs-tools/` | Recovered tracked source for the filesystem tool |
| `patches/` | Original local diff and a separate minimal build-syntax repair |
| `environment/` | Original OS and GRUB configuration from both guests |
| `reports/` | Authored report in PDF and DOCX |
| `results/screenshots/` | Original namespace, fio, code and parallelism screenshots |
| `experiments/` | Workload context, provenance and interpretation limits |
| `provenance/` | Revision, hashes and checks actually performed during recovery |

The smaller guest `NVMeVirt` has an empty SCDEMST project directory; the implementation was recovered from `NVMeVirt_`. FTL and ZNS are build modes of the driver, not two separate source projects inferred from the VM names.

## Build

Use a Linux development guest with matching kernel headers, compiler, make and patch:

```sh
python3 scripts/build_module.py ftl
python3 scripts/build_module.py zns --apply-build-fix
```

For compile-only validation against another installed header tree:

```sh
python3 scripts/build_module.py ftl --kernel-dir /usr/src/linux-headers-YOUR-VERSION
python3 scripts/build_module.py zns --kernel-dir /usr/src/linux-headers-YOUR-VERSION --apply-build-fix
```

The output is `build/ftl/nvmev.ko` or `build/zns/nvmev.ko`. The build script never loads the module. Both modes retain the module name `nvmev`; run them separately in a disposable guest. Renaming two `.ko` files does not make them two independent simultaneously loadable module instances.

## Recovered state and minimal repair

The final saved worktree contains two invalid `#printk` directives. The source is preserved unchanged under `vendor/`. The explicit `--apply-build-fix` option applies `patches/build-syntax-fix.patch` only to the disposable build copy. It restores valid C `printk` calls and enables their logging; logging overhead must be recorded in any new performance run. It does not claim to recreate the exact binary that produced the older report.

The recovered error path also decrements the counter and returns true after some failed read/write handlers; this behavior is preserved, not silently changed during archiving. Review it before extending the emulator. See `experiments/README.md` for counter limitations and the evidence behind the original comparison.

## Historical results

The authored report records namespace identification, FTL/F2FS and ZNS/ZoneFS runs and a parallelism table. Original screenshots are preserved. Recovery did not rerun benchmarks or manufacture raw measurements; validation status is in `provenance/validation.json`.

NVMeVirt is upstream work; this repository's contribution is the local modifications and experiment archive. Upstream GPL/BSD notices remain with their code. Reports/screenshots have no newly granted blanket license.
