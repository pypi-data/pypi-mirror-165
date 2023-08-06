---
doc: |
  This workflow builds Linux kernel as .deb installable packages

steps:
- name: sysinfo
  uses: linux.sysinfo

- name: build
  uses: linux.build_kdebs
