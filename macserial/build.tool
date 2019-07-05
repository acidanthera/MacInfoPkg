#!/bin/bash

if [ "$BUILD_32" = "" ]; then
  if [ $(uname -r | cut -f1 -d'.') -gt 17 ]; then
    echo "Warning: Disabling 32-bit compilation by default on 10.14..."
    BUILD_32=false
  else
    BUILD_32=true
  fi
fi

if [ "$MACOS_MIN" = "" ]; then
  if [ $(uname -r | cut -f1 -d'.') -gt 17 ]; then
    echo "Warning: Disabling 10.4 and 10.5 support by default on 10.14..."
    MACOS_MIN="10.6"
  else
    MACOS_MIN="10.4"
  fi
fi

cd "$(dirname "$0")" || exit 1

rm -rf bin
mkdir -p bin || exit 1

VER=$(cat src/macserial.h | grep 'PROGRAM_VERSION' | cut -f2 -d'"')

if [ "$VER" == "" ]; then
  VER=unknown
fi

if [ "$DEBUG" != "" ]; then
  if $BUILD_32; then
    clang -std=c11 -Werror -Wall -Wextra -pedantic -Wl,-framework,IOKit -Wl,-framework,CoreFoundation -m32 -mmacosx-version-min=$MACOS_MIN -O0 -g src/macserial.c -o bin/macserial32 || exit 1
  fi
  clang -std=c11 -Werror -Wall -Wextra -pedantic -Wl,-framework,IOKit -Wl,-framework,CoreFoundation -m64 -mmacosx-version-min=$MACOS_MIN -O0 -g src/macserial.c -o bin/macserial64 || exit 1
else
  if $BUILD_32; then
    clang -std=c11 -Werror -Wall -Wextra -pedantic -Wl,-framework,IOKit -Wl,-framework,CoreFoundation -m32 -flto -mmacosx-version-min=$MACOS_MIN -O3 src/macserial.c -o bin/macserial32 || exit 1
    strip -x bin/macserial32 || exit 1
  fi
  clang -std=c11 -Werror -Wall -Wextra -pedantic -Wl,-framework,IOKit -Wl,-framework,CoreFoundation -m64 -flto -mmacosx-version-min=$MACOS_MIN -O3 src/macserial.c -o bin/macserial64 || exit 1
  strip -x bin/macserial64 || exit 1
fi

if $BUILD_32; then
  lipo -create bin/macserial32 bin/macserial64 -output bin/macserial || exit 1
else
  cp bin/macserial64 bin/macserial
fi

rm -f bin/macserial32 bin/macserial64

if [ "$(which i686-w64-mingw32-gcc)" != "" ]; then
  if [ "$DEBUG" != "" ]; then
    i686-w64-mingw32-gcc -std=c11 -Werror -Wall -Wextra -pedantic -O0 -g src/macserial.c -o bin/macserial32.exe || exit 1
  else
    i686-w64-mingw32-gcc -s -std=c11 -Werror -Wall -Wextra -pedantic -O3 src/macserial.c -o bin/macserial32.exe || exit 1
  fi
fi

cd bin || exit 1

zip -qry -FS "macserial-${VER}-mac.zip" macserial || exit 1
if [ -f macserial32.exe ]; then
  zip -qry -FS "macserial-${VER}-win32.zip" macserial32.exe || exit 1
fi

exit 0
