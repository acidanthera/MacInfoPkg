macserial
=========

[![Build Status](https://travis-ci.org/acidanthera/macserial.svg?branch=master)](https://travis-ci.org/acidanthera/macserial)

Obtains and decodes Mac serial number and board identifier to provide more information about the production of your hardware. Works as a decent companion to [Apple Check Coverage](https://checkcoverage.apple.com) and [Apple Specs](http://support-sp.apple.com/sp/index?page=cpuspec&cc=HTD5) portal. Check the [format description](https://github.com/vit9696/MacSerial/blob/master/FORMAT.md) for more details.

Should be built with a compiler supporting C99. Prebuilt binaries are available for macOS 10.4 and higher.

Run with `-h` argument to see all available arguments.

### Credits
* Chameleon and Clover teams for Apple SMBIOS database
* [al3xjames](https://github.com/al3xtjames) for several hints and another [database](https://github.com/al3xtjames/MacGen)
* CCC and ...numberinfo.com for hiding their work and inspiring others to reverse it
* Several guys from AppleLife for conducting relevant parts of the research, thanks a lot!
* [vit9696](https://github.com/vit9696) for the tool
