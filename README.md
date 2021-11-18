# Jacdac Python

A client SDK for desktop python for Jacdac.

**Jacdac** is a plug-and-play hardware/software stack
for **microcontrollers** and their peripherals (sensors/actuators),
with applications to rapid prototyping, making, and physical computing.

**Partner Preview: Jacdac is currently in preview. If you would like to join as a pre-release test partner, please email jacdac-tap@microsoft.com.**

This repository contains a command line interface tool for the [Jacdac](https://aka.ms/jacdac) protocol.

-   **[Jacdac Protocol Documentation](https://aka.ms/jacdac/)**
-   **[Python Documentation](https://microsoft.github.io/jacdac-docs/clients/python/)**
-   **[API documentation](https://jacdac-python.readthedocs.io/en/latest/)**
-   Discussions at https://github.com/microsoft/jacdac/discussions
-   Issues are tracked on https://github.com/microsoft/jacdac/issues

The rest of this page is for developers of the `jacdac-python` library.

## Development

This section explains how to develop this library locally.

### WSL setup

```
sudo apt update
sudo apt upgrade
sudo apt install python3 python3-pip ipython3 python3-venv
```

### Build package

Install the build tools

```
pip3 install --upgrade -r requirements.txt
```

Create the library bundle

```
python3 -m build
```

### Devtools

The devtools script allows to run a Jacdac dashboard connected through a websocket. This allows
to pipe packets from the python library into the web developer tools and diagnose issues over there

To install/updates the tools

```
sh scripts/devsetup.sh
```

To launch the developer tools server (once per session)

```
sh scripts/devtools.sh
```

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.opensource.microsoft.com.

When you submit a pull request, a CLA bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., status check, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.

## Trademarks

This project may contain trademarks or logos for projects, products, or services. Authorized use of Microsoft
trademarks or logos is subject to and must follow
[Microsoft's Trademark & Brand Guidelines](https://www.microsoft.com/en-us/legal/intellectualproperty/trademarks/usage/general).
Use of Microsoft trademarks or logos in modified versions of this project must not cause confusion or imply Microsoft sponsorship.
Any use of third-party trademarks or logos are subject to those third-party's policies.
