"""
    fio-wrapper
    ===========

    The intent is to be able to do tie fio into testing infra and to have a means of
    ensuring that "benchmark" can be performed in a reproducible manner.

    It does so by constructing an transforming a dictionary of parameters and
    environment variables. This is done via:

    * fio(cijoe, parameters="", env={}): invoke fio as defined in cijoe.config.options

    * setup_job(param, env, job_name): add parameters JOBS accoring to name

    * setup_ioengine(param, env, ...): add parameters and env. according to ioengine

    * setup_output(param, env, ...): add parameters for output format and file

    * fio_fancy(cijoe, ...): construct parameters using setup_* helpers, then call fio()

    Then **chaining** of the parameter construction is done, such that it is possible to
    control certain job-parameters depending on the device, I/O engine, and I/O engine
    options.
    For example, we might wish to run fio with ``--direct=1``, however, when sending
    that same job to e.g. ``/dev/ng0n1`` (the char-device encapsulating an NVMe
    namespace), then ``--direct=1`` is invalid.
    Such a transformation is then done when seeing that the device is an NVMe chardev.

    config
    ------

    fio.bin

    fio.engines

    retargtable: true
    -----------------
"""
import errno
import json
import logging as log
import os
from pathlib import Path

JOBS = {
    "compare": {
        "name": "compare",
        "rw": "randread",
        "size": "12G",
        "iodepth": "1",
        "bs": "4K",
        "direct": "1",
        "thread": "1",
        "time_based": "1",
        "runtime": "7",
        "ramp_time": "3",
        "norandommap": "1",
        "allow_file_create": "0",
    },
    "verify": {
        "name": "verify",
        "rw": "randwrite",
        "size": "1G",
        "iodepth": "16",
        "bs": "4K",
        "direct": "1",
        "thread": "1",
        "verify": "crc32c",
        "allow_file_create": "0",
    },
    "zoned": {
        "name": "zoned",
        "zonemode": "zbd",
        "rw": "write",
        "size": "1G",
        "iodepth": "1",
        "bs": "4K",
        "direct": "1",
        "thread": "1",
        "ramp_time": "1",
        "norandommap": "1",
        "verify": "crc32c",
        "allow_file_create": "0",
    },
}


def setup_job(param, env, job_name):
    """Setup parameters for the fio-job based on the templates in JOBS"""

    param.update(JOBS[job_name])


def setup_ioengine(param, env, engine_name, cijoe, device, xnvme_opts, spdk_opts):
    """
    Setup dictionaries of environment variables and parameters for the given I/O engine

    env: environments variables needed by the ioengine
    param: parameters for the ioengine (param)

    @returns env, param
    """

    engine = (
        cijoe.config.options.get("fio", {}).get("engines", {}).get(engine_name, None)
    )
    if engine is None:
        log.error(f"fio.engine({engine_name}) not in configuration")
        return False

    # disable '--direct' for char-devices
    if "cdev" in device["labels"]:
        param["direct"] = "0"

    # setup the --ioengine flag and possibly the LD_PRELOAD environment variable
    if engine["type"] == "builtin":
        param["ioengine"] = engine_name
    elif engine["type"] == "external_dynamic":
        param["ioengine"] = f"external:{ engine['path'] }"
    elif engine["type"] == "external_preload":
        param["ioengine"] = engine_name
        env["LD_PRELOAD"] = {engine["path"]}
    else:
        log.error(f"Configuration has invalid engine.type({ engine['type'] })")
        return False

    # setup 'xnvme' specific options
    if engine_name == "xnvme":
        param["xnvme_async"] = xnvme_opts["async"]
        param["xnvme_sync"] = xnvme_opts["sync"]
        param["xnvme_admin"] = xnvme_opts["admin"]
        param["xnvme_dev_nsid"] = device["nsid"]

        if any(label in ["pcie", "fabrics"] for label in device["labels"]):
            param["filename"] = device["uri"].replace(":", r"\:")
        else:
            param["filename"] = device["uri"]
    elif engine_name == "spdk":
        param["filename"] = " ".join(
            [
                "trtype=PCIe",
                f"traddr={device['uri']}",
                f"ns={device['nsid']}",
            ]
        )
    elif engine_name == "spdk_bdev":
        # TODO: need to generate a spdk.bdev.conf for the device and be-options
        # generate spdk-conf
        # spdk_conf = []
        # spdk_conf.append("[Nvme]")
        # spdk_conf.append("  TransportID \"trtype:PCIe traddr:{device['uri']\" Nvme0")

        param["spdk_conf"] = "/tmp/spdk.bdev.conf"
        param["filename"] = "Nvme0n1"
    else:
        param["filename"] = device["uri"]


def setup_output(param, env, output_fpath):
    """
    Sets up fio to store output in 'output_fpath' in formated in JSON as well as normal
    output. For postprocessing the json-document needs to be extracted as it is
    intermixed without non-JSON content.
    """

    param["output-format"] = "normal,json"
    param["output"] = f"{output_fpath}"


def fio(cijoe, parameters="", env={}):
    """
    Invoke 'fio' using binary at `'cijoe.config.options.fio.bin`', with the given
    parameters and environment variables (``env``)

    @returns err, state
    """

    return cijoe.run(f"{cijoe.config.options['fio']['bin']} {parameters}", env=env)


def fio_fancy(cijoe, output_fpath, jobname, engine_name, device, xnvme_opts):
    """
    Run fio using helpers for parameter setup for io-engines, store fio output with
    json, collect the output as artifact

    @returns err, state
    """

    param, env = {}, {}  # Setup parameters and env.
    setup_job(param, env, jobname)
    setup_ioengine(param, env, engine_name, cijoe, device, xnvme_opts, {})
    setup_output(param, env, output_fpath)

    environment = env
    parameters = " ".join([f'--{key}="{val}"' for key, val in param.items()])

    err, _ = cijoe.run(f"rm {output_fpath}")  # Avoid getting old data...
    if err:
        log.info(f"failed removing '{output_fpath}'")

    err, state = fio(cijoe, parameters, env=environment)

    cijoe.run(f"cat {output_fpath}")  # Get the output in runlog

    artifacts = state.output_dpath / "artifacts"  # Collect output as artifact
    os.makedirs(artifacts, exist_ok=True)
    cijoe.get(str(output_fpath), str(artifacts / output_fpath.name))

    return err, state


def dict_from_fio_output_file(fpath: Path) -> dict:
    """
    The JSON output produced by fio comes mixed with non-JSON output, this function
    attempts to extract the JSON part, parse it and return the JSON-document as a dict.

    On error, an empty dict is returned.
    """

    lines = []

    with fpath.open() as fio_output:
        do_append = False
        for line in fio_output:
            if line.startswith("{"):
                do_append = True

            if do_append:
                lines.append(line)

            if line.startswith("}"):
                break
    try:
        return json.loads("".join(lines))
    except json.decoder.JSONDecodeError:
        return {}
