"""
Linux Custom Kernel as Debian Package
=====================================

There are a myriad of ways to build and install a custom Linux kernel. This worklet
builds it as a Debian package. The generated .deb packages are stored in
cijoe.output_path.

Retagetable: true
-----------------

Worklet arguments
-----------------

with.localversion
"""
from pathlib import Path


def worklet_entry(args, cijoe, step):
    """Configure, build and collect the build-artifacts"""

    repos = Path(cijoe.config.options["repository"]["path"]).resolve()
    err, _ = cijoe.run(f"[ -d {repos} ]")
    if err:
        return err

    localversion = step.get("with", {"localversion": "custom"}).get("localversion")

    commands = [
        "[ -f .config ] && rm .config || true",
        "yes " " | make olddefconfig",
        "./scripts/config --disable CONFIG_DEBUG_INFO",
        "./scripts/config --disable SYSTEM_TRUSTED_KEYS",
        "./scripts/config --disable SYSTEM_REVOCATION_KEYS",
        f"yes '' | make -j$(nproc) bindeb-pkg LOCALVERSION={localversion}",
        f"mkdir -p {cijoe.output_path}/artifacts/linux",
        f"mv ../*.deb {cijoe.output_path}/artifacts/linux",
        f"mv ../*.changes {cijoe.output_path}/artifacts/linux",
        f"mv ../*.buildinfo {cijoe.output_path}/artifacts/linux",
    ]
    for cmd in commands:
        err, _ = cijoe.run(cmd, cwd=str(repos))
        if err:
            return err

    return 0
