Apple Mac Serial Format
=======================

It is reasonably important to get more information about the goods you buy, especially if they are not new, and you do not have absolute confidence in the seller. Serial numbers are the first thing to look at. For Apple products [Apple Check Coverage](https://checkcoverage.apple.com) is your best friend.

However, it does not show all the details encoded in the serial, and in some case it may be important. For example, certain shady dealers may change one valid serial by the other, and it will not be obvious at a glance that the serial does not belong to the actual model. This FAQ attempts to explains the reverse-engineered structure of the serials used in Apple hardware.

You could always receive information about the current serial number of your Mac by running `./getserial`.  
For the other serial use `./getserial -i SERIALNUMBER`, where `SERIALNUMBER` is the serial you check.

There generally are 2 similar formats of serial encoding: the old 11 character format, and the new 12 character format. 

| Type      | Location  | Year | Week | Line | Platform |
| --------- | --------- | ---- | ---- | ---- | -------- |
| Old (11)  | LL        | Y    | WW   | SSS  | PPP      |
| New (12)  | LLL       | Y    | W    | SSS  | PPPP     |

### Location

This value encodes the manufacturing location, which is often more descriptive than `Made in China`, since it may reveal the responsible company and the city. For example, `F5K` means `USA (Flextronics)` and `QT` means `Taiwan (Quanta Computer)`. The list is not standardised or published anywhere, but you can see several known locations by running `./getserial -l`.

One of the important locations for old-style serials (11 characters) is `RM`. It means that the model was refurbished. For new-style serials you have to call [Apple support](https://support.apple.com) to know this.

### Year

Year encodes the actual manufacturing year of each model. For refurbished models it is unknown whether it is replaced by the remanufacturing year.

For old-style serials it always is a digit that encodes the last digit of the year. For example, `8` means 2008 and `1` means 2011. Only `0` to `9` digitis are used for year encoding. Old-style serials are out of use starting with 2013, so `3` means 2003 not 2013.

| Char | Year |
| ---- | ---- |
| `3`  | 2003 |
| `4`  | 2004 |
| `5`  | 2005 |
| `6`  | 2006 |
| `7`  | 2007 |
| `8`  | 2008 |
| `9`  | 2009 |
| `0`  | 2010 |
| `1`  | 2011 |
| `2`  | 2012 |


For new-style serials it is an alphanumeric value, which not only encodes the year, but its half as well. Not all the values are allowed. The table below outlines the pairs of characters which are assumed to encode each supported year. First character in the pair is believed to encode the first half of the year, and the second character — the second half.

| Pair     | Year |
| -------- | ---- |
| `C`, `D` | 2010 |
| `F`, `G` | 2011 |
| `H`, `J` | 2012 |
| `K`, `L` | 2013 |
| `M`, `N` | 2014 |
| `P`, `Q` | 2015 |
| `R`, `S` | 2016 |
| `T`, `V` | 2017 |
| `W`, `X` | 2018 |
| `Y`, `Z` | 2019 |

### Week

Week encodes the actual manufacturing week of each model. This week has nothing in common with [ISO 8601](https://en.wikipedia.org/wiki/ISO_week_date), and appears to be encoded literally as 7-day sequences starting from January, 1st. Since each year has either 365 or 366 days, 53rd week is extremely rare, and you are lucky to have such a serial.

For old-style serials week is encoded in plain numeric digits with leading zeroes. `01`, `02`, ... `53`. For new-style serials an alpha-numeric code is used. Encoded year half also counts and means adds 26 weeks for the second one.

| Char | 1st half | 2nd half |
| ---- | -------- | -------- |
| `1`  | `1`      | `27`     |
| `2`  | `2`      | `28`     |
| `3`  | `3`      | `29`     |
| `4`  | `4`      | `30`     |
| `5`  | `5`      | `31`     |
| `6`  | `6`      | `32`     |
| `7`  | `7`      | `33`     |
| `8`  | `8`      | `34`     |
| `9`  | `9`      | `35`     |
| `C`  | `10`     | `36`     |
| `D`  | `11`     | `37`     |
| `F`  | `12`     | `38`     |
| `G`  | `13`     | `39`     |
| `H`  | `14`     | `40`     |
| `J`  | `15`     | `41`     |
| `K`  | `16`     | `42`     |
| `L`  | `17`     | `43`     |
| `M`  | `18`     | `44`     |
| `N`  | `19`     | `45`     |
| `P`  | `20`     | `46`     |
| `Q`  | `21`     | `47`     |
| `R`  | `22`     | `48`     |
| `T`  | `23`     | `49`     |
| `V`  | `24`     | `50`     |
| `W`  | `25`     | `51`     |
| `X`  | `26`     | `52`     |
| `Y`  | `-`      | `53`     |

For old-style serials it is a pair of two digits, which encode the manufacturing week.

### Production line

Production line is believed to encode the manufacturing line or some identifier used by the assembly engineers. It is calculated as a sum of three alpha-numeric characters, which themselves represent a modified base34 code excluding `O` and `I`. The actual formula is as follows:

```
base34[S1] * 68 + base34[S2] * 34 + base34[S3] = production line
```

That allows to encode a total of `3400` production lines from `0` to `3399`.

| Char | Value | Char | Value |
| ---- | ----- | ---- | ----- |
| `0`  | `0`   | `H`  | `17`  |
| `1`  | `1`   | `J`  | `18`  |
| `2`  | `2`   | `K`  | `19`  |
| `3`  | `3`   | `L`  | `20`  |
| `4`  | `4`   | `M`  | `21`  |
| `5`  | `5`   | `N`  | `22`  |
| `6`  | `6`   | `P`  | `23`  |
| `7`  | `7`   | `Q`  | `24`  |
| `8`  | `8`   | `R`  | `25`  |
| `9`  | `9`   | `S`  | `26`  |
| `A`  | `10`  | `T`  | `27`  |
| `B`  | `11`  | `U`  | `28`  |
| `C`  | `12`  | `V`  | `29`  |
| `D`  | `13`  | `W`  | `30`  |
| `E`  | `14`  | `X`  | `31`  |
| `F`  | `15`  | `Y`  | `32`  |
| `G`  | `16`  | `Z`  | `33`  |

### Production copy

From the nature of the production line code there often exist multiple ways of encoding each value. For example, `680` could be encoded as `0L0`, `1J0`, `2G0`, `3E0`, ..., `920` and `2400` could be encoded as `KYL`, `LWL`, `MUL`, ..., `Z4L`. It was experimentally discovered that the first N encoded values are always valid, and starting with the first invalid value there will be no valid ones. From this data it could be assumed that the encoding type is incremented for each model produced from the same line. So `0L0` and `KYL` are the first copies produced, and `920` with `Z4L` are the last copies.

### Platform model

Last 3 (for legacy serials) or 4 (for new serials) symbols encode the actual platform/model of this exact piece of the hardware. This is probably the most useful part of the serial, since it allows you to get the detailed description of your hardware directly from the dedicated Apple Specs portal. To do so you need to modify the following URI to contain your real platform model value instead of `PPPP` and follow it in your browser:

```
http://support-sp.apple.com/sp/index?page=cpuspec&cc=PPPP
```

For example, for iMacPro1,1 it could be [HX87](http://support-sp.apple.com/sp/index?page=cpuspec&cc=HX87) and for MacBookPro14,3 it could be [HTD5](http://support-sp.apple.com/sp/index?page=cpuspec&cc=HTD5).

### Appendix

This information was obtained experimentally and may not be accurate in certain details. Be warned that it is published at no warranty for educational and introductory purposes only.
