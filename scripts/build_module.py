#!/usr/bin/env python3
"""Build one recovered NVMeVirt mode in a disposable build directory; never load it."""
import argparse
import os
import pathlib
import re
import shutil
import subprocess

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('mode',choices=['ftl','zns'])
parser.add_argument('--kernel-dir',default='/lib/modules/'+os.uname().release+'/build')
parser.add_argument('--apply-build-fix',action='store_true',help='Explicitly apply the archived #printk syntax repair to the build copy')
args=parser.parse_args()
root=pathlib.Path(__file__).resolve().parents[1]
destination=root/'build'/args.mode
if not pathlib.Path(args.kernel_dir,'Makefile').is_file():parser.error('Kernel header tree not found: '+args.kernel_dir)
if args.mode=='zns' and not args.apply_build_fix:parser.error('The recovered ZNS worktree contains invalid #printk directives. Review patches/build-syntax-fix.patch and opt in with --apply-build-fix.')
if destination.exists():shutil.rmtree(destination)
shutil.copytree(root/'vendor/nvmevirt',destination)
kbuild=destination/'Kbuild'
text=kbuild.read_text()
selected='SSD' if args.mode=='ftl' else 'ZNS'
for mode in ['NVM','SSD','ZNS','KV']:
    text=re.sub(r'(?m)^#?[ \t]*CONFIG_NVMEVIRT_'+mode+r'[ \t]*:=[ \t]*y[ \t]*$',('' if mode==selected else '#')+'CONFIG_NVMEVIRT_'+mode+' := y',text)
kbuild.write_text(text)
if args.apply_build_fix:
    subprocess.run(['patch','-p1','--batch','--forward','-i',str(root/'patches/build-syntax-fix.patch')],cwd=destination,check=True)
subprocess.run(['make','-C',str(destination),'KERNELDIR='+str(pathlib.Path(args.kernel_dir).resolve()),'-j'+str(min(os.cpu_count() or 1,4))],check=True)
print('Built '+str(destination/'nvmev.ko')+'; module was not loaded.')
