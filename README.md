MacInfoPkg
==========

[![Build Status](https://travis-ci.org/acidanthera/MacInfoPkg.svg?branch=master)](https://travis-ci.org/acidanthera/MacInfoPkg)

Various information about Mac hardware used by multiple projects,
including [OpenCore](https://github.com/acidanthera/OpenCorePkg).

## macserial

**WARNING**: macserial database is currently in process of being synced with MacInfoPkg database.

macserial is a tool that obtains and decodes Mac serial number and board identifier to provide more information about the production of your hardware. Works as a decent companion to [Apple Check Coverage](https://checkcoverage.apple.com) and [Apple Specs](http://support-sp.apple.com/sp/index?page=cpuspec&cc=HTD5) portal. Check the [format description](https://github.com/acidanthera/MacInfoPkg/blob/master/macserial/FORMAT.md) for more details.

Should be built with a compiler supporting C99. Prebuilt binaries are available for macOS 10.4 and higher.

Run with `-h` argument to see all available arguments.

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

## Credits

* All database maintainers, who continue to actualise data
* Chameleon and Clover teams for legacy Apple SMBIOS database
* [al3xjames](https://github.com/al3xtjames) for several hints and another [database](https://github.com/al3xtjames/MacGen)
* CCC and ...numberinfo.com for hiding their work and inspiring others to reverse it
* Several guys from AppleLife for conducting relevant parts of the research, thanks a lot!
* [vit9696](https://github.com/vit9696)
