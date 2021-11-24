
from .bus import Bus
from configparser import ConfigParser
from jacdac.logger.constants import JD_LOGGER_PRIORITY_SILENT


def create_bus_from_config() -> Bus:
    """Creates a bus from configuration files

    Raises:
        RuntimeError: no jacdac section was found

    Returns:
        Bus: A Jacdac bus
    """

    config = ConfigParser()
    config.read(["./jacdac.ini", "./.jacdac/config.ini", "./setup.cfg"])
    if not "jacdac" in config:
        raise RuntimeError("no jacdac session found in configuration files")

    cfg = config["jacdac"]
    return Bus(device_id=cfg.get("device_id", None),
               product_identifier=cfg.getint(
        "product_identifier", None),
        firmware_version=cfg.get(
        "firmware_version", None),
        device_description=cfg.get(
        "device_description", None),
        disable_logger=cfg.getboolean(
        "disable_logger", False),
        disable_role_manager=cfg.getboolean(
        "disable_role_manager", False),
        disable_brain=cfg.getboolean(
        "disable_brain", False),
        disable_dev_tools=cfg.getboolean(
        "disable_dev_tools", False),
        hf2_portname=cfg.get("hf2_portname", None),
        default_logger_min_priority=cfg.getint(
        "default_logger_min_priority", JD_LOGGER_PRIORITY_SILENT),
        role_manager_file_name=cfg.get(
        "role_manager_file_name", None),
        settings_file_name=cfg.get(
        "settings_file_name", None)
    )
