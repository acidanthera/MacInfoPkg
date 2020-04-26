MacInfoPkg
==========

[![Build Status](https://travis-ci.com/acidanthera/MacInfoPkg.svg?branch=master)](https://travis-ci.com/acidanthera/MacInfoPkg)

Various information about Mac hardware used by multiple projects,
including [OpenCore](https://github.com/acidanthera/OpenCorePkg).

[Current database status](https://github.com/acidanthera/MacInfoPkg/blob/master/DataBase.md)

## macserial

macserial is a tool that obtains and decodes Mac serial number and board identifier to provide more information about the production of your hardware. Works as a decent companion to [Apple Check Coverage](https://checkcoverage.apple.com) and [Apple Specs](http://support-sp.apple.com/sp/index?page=cpuspec&cc=HTD5) portal. Check the [format description](https://github.com/acidanthera/MacInfoPkg/blob/master/macserial/FORMAT.md) for more details.

Should be built with a compiler supporting C99. Prebuilt binaries are available for macOS 10.4 and higher.

Run with `-h` argument to see all available arguments.

## macrecovery

macrecovery is a tool that helps to automate recovery interaction. It can be used to download diagnostics and recovery as well as analyse MLB.

Requires python to run. Run with `-h` argument to see all available arguments.

## Improving database

To add a new hardware board, please create a file in DataBase
directory, and then run `./update_generated.py`. It should not
output anything and return zero code.

To install PyYAML on macOS use the following commands:

```
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
sudo -H python get-pip.py
sudo -H pip install pyyaml
```

## Unpacking firmwares

To update the database you can either get the information from firmware images or from
running hardware. There currently are two places for firmware images: `FirmwareUpdate.pkg`
for generic models and `BridgeOSUpdateCustomer.pkg` for T2 models (the entire restore list
is available at [mesu.apple.com](https://mesu.apple.com/assets/bridgeos/com_apple_bridgeOSIPSW/com_apple_bridgeOSIPSW.xml)) 
To use them do as follows:

1. Visit suitable update catalogue by filling the OS versions (e.g. [this](https://swscan.apple.com/content/catalogs/others/index-10.15seed-10.15-10.14-10.13-10.12-10.11-10.10-10.9-mountainlion-lion-snowleopard-leopard.merged-1.sucatalog.gz) one for 10.15 beta).
2. Download most recent `FirmwareUpdate.pkg` and `BridgeOSUpdateCustomer.pkg`.
3. Extract `scap` files from `FirmwareUpdate.pkg` files and use them as is.
4. Extract `/usr/standalone/firmware/bridgeOSCustomer.bundle/Contents/Resources/UpdateBundle.zip`
   file from `BridgeOSUpdateCustomer.pkg` and unpack it.
5. After unpacking `UpdateBundle.zip` go to `boot/Firmware/MacEFI` directory and unpack im4p files.
   You can use [img4](https://github.com/xerub/img4lib), [img4tool](https://github.com/tihmstar/img4tool), or our dedicated [MacEfiUnpack](https://github.com/acidanthera/OpenCorePkg/blob/master/Utilities/MacEfiUnpack/MacEfiUnpack.py). For example, `for i in *.im4p ; do ./MacEfiUnpack.py "$i" ; done`

## Credits

* All database maintainers, who continue to actualise data
* [AppleLife](https://applelife.ru/threads/dampy-originalnyx-makov.2943712) and [VirtualSMC](https://github.com/acidanthera/VirtualSMC/tree/master/Docs) hardware dump databases
* Chameleon and Clover teams for legacy Apple SMBIOS database
* [al3xjames](https://github.com/al3xtjames) for several hints and another [database](https://github.com/al3xtjames/MacGen)
* CCC and ...numberinfo.com for hiding their work and inspiring others to reverse it
* Several guys from AppleLife for conducting relevant parts of the research, thanks a lot!
* [vit9696](https://github.com/vit9696)
