/** @file
  Copyright (C) 2019, vit9696. All rights reserved.

  All rights reserved.

  This program and the accompanying materials
  are licensed and made available under the terms and conditions of the BSD License
  which accompanies this distribution.  The full text of the license may be found at
  http://opensource.org/licenses/bsd-license.php

  THE PROGRAM IS DISTRIBUTED UNDER THE BSD LICENSE ON AN "AS IS" BASIS,
  WITHOUT WARRANTIES OR REPRESENTATIONS OF ANY KIND, EITHER EXPRESS OR IMPLIED.
**/

#include <Library/BaseMemoryLib.h>
#include <Library/MacInfoLib.h>

STATIC CONST UINT8 mDevicePathsSupported = 1;

VOID
GetMacInfo (
  IN CONST CHAR8     *ProductName,
  OUT MAC_INFO_DATA  *MacInfo
  )
{
  (VOID) ProductName;
  ZeroMem (MacInfo, sizeof (*MacInfo));

  //
  // Fill in DataHub values.
  //
  MacInfo->DataHub.PlatformName = "platform";
  MacInfo->DataHub.DevicePathsSupported = &mDevicePathsSupported;

  //
  // TODO: Implement =)
  //
}
