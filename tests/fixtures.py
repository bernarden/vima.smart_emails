SMARTCTL_SEAGATE_IRONWOLF_HDD = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.5.11-7-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Family:     Seagate IronWolf
Device Model:     ST1000VN123-0A1234
Serial Number:    ABC01D2E
LU WWN Device Id: 0 123a45 6b7890123
Firmware Version: AB01
User Capacity:    1,000,195,402,752 bytes [1.00 TB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    7200 rpm
Form Factor:      3.5 inches
Device is:        In smartctl database 7.3/0123
ATA Version is:   ACS-4 (minor revision not indicated)
SATA Version is:  SATA 3.3, 6.0 Gb/s (current: 6.0 Gb/s)
Local Time is:    Sat Jan 01 00:00:00 2000 NZDT
SMART support is: Available - device has SMART capability.
SMART support is: Enabled



"""

SMARTCTL_TOSHIBA_HDD = b"""smartctl 7.1 2019-12-30 r5022 [x86_64-linux-5.4.44-1-pve] (local build)
Copyright (C) 2002-19, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===

Device Model:     TOSHIBA AB0123CDEF
Serial Number:    A0BCD1E2F
LU WWN Device Id: 0 123a45 6b7890123
Firmware Version: AB012C
User Capacity:    1,000,204,886,016 bytes [1.00 TB]
Sector Sizes:     512 bytes logical, 4096 bytes physical
Rotation Rate:    5400 rpm
Form Factor:      2.5 inches
Device is:        Not in smartctl database [for details use: -P showall]
ATA Version is:   ATA8-ACS (minor revision not indicated)
SATA Version is:  SATA 2.6, 3.0 Gb/s (current: 3.0 Gb/s)
Local Time is:    Mon Jun 01 00:00:00 2020 NZST
SMART support is: Available - device has SMART capability.
SMART support is: Enabled



"""

SMARTCTL_SAMSUNG_NVME = b"""smartctl 7.4 2023-08-01 r5530 [x86_64-w64-mingw32-w11-b26100] (sf-7.4-1)
Copyright (C) 2002-23, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF INFORMATION SECTION ===
Model Number:                       Samsung SSD 990 PRO 2TB
Serial Number:                      A0B1CD2E345678F
Firmware Version:                   0A1BCDE2
PCI Vendor/Subsystem ID:            0x123a
IEEE OUI Identifier:                0x012345
Total NVM Capacity:                 2,000,398,934,016 [2.00 TB]
Unallocated NVM Capacity:           0
Controller ID:                      1
NVMe Version:                       2.0
Number of Namespaces:               1
Namespace 1 Size/Capacity:          2,000,398,934,016 [2.00 TB]
Namespace 1 Utilization:            294,600,142,848 [294 GB]
Namespace 1 Formatted LBA Size:     512
Namespace 1 IEEE EUI-64:            002538 433142ed9e
Local Time is:                      Thu May 08 00:00:00 2025 NZST

"""
