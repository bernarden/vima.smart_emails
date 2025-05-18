SMARTCTL_HHD1_ATTRIBUTES_SCAN1: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-9-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000b   100   100   001    Pre-fail  Always       -       0
  2 Throughput_Performance  0x0004   136   136   054    Old_age   Offline      -       96
  3 Spin_Up_Time            0x0007   083   083   001    Pre-fail  Always       -       339 (Average 341)
  4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       25
  5 Reallocated_Sector_Ct   0x0033   100   100   001    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000a   100   100   001    Old_age   Always       -       0
  8 Seek_Time_Performance   0x0004   140   140   020    Old_age   Offline      -       15
  9 Power_On_Hours          0x0012   098   098   000    Old_age   Always       -       16947
 10 Spin_Retry_Count        0x0012   100   100   001    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       25
 22 Unknown_Attribute       0x0023   100   100   025    Pre-fail  Always       -       100
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       750
193 Load_Cycle_Count        0x0012   100   100   000    Old_age   Always       -       750
194 Temperature_Celsius     0x0002   060   060   000    Old_age   Always       -       34 (Min/Max 20/47)
196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x000a   100   100   000    Old_age   Always       -       0

"""

SMARTCTL_HHD1_ATTRIBUTES_SCAN2: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-9-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000b   100   100   001    Pre-fail  Always       -       0
  2 Throughput_Performance  0x0004   136   136   054    Old_age   Offline      -       96
  3 Spin_Up_Time            0x0007   083   083   001    Pre-fail  Always       -       339 (Average 341)
  4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       25
  5 Reallocated_Sector_Ct   0x0033   100   100   001    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000a   100   100   001    Old_age   Always       -       0
  8 Seek_Time_Performance   0x0004   140   140   020    Old_age   Offline      -       15
  9 Power_On_Hours          0x0012   098   098   000    Old_age   Always       -       17115
 10 Spin_Retry_Count        0x0012   100   100   001    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       25
 22 Unknown_Attribute       0x0023   100   100   025    Pre-fail  Always       -       100
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       757
193 Load_Cycle_Count        0x0012   100   100   000    Old_age   Always       -       757
194 Temperature_Celsius     0x0002   058   058   000    Old_age   Always       -       36 (Min/Max 20/47)
196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x000a   100   100   000    Old_age   Always       -       0

"""

SMARTCTL_HHD1_ATTRIBUTES_SCAN3: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-9-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 16
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000b   100   100   001    Pre-fail  Always       -       0
  2 Throughput_Performance  0x0004   136   136   054    Old_age   Offline      -       96
  3 Spin_Up_Time            0x0007   083   083   001    Pre-fail  Always       -       339 (Average 341)
  4 Start_Stop_Count        0x0012   100   100   000    Old_age   Always       -       26
  5 Reallocated_Sector_Ct   0x0033   100   100   001    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000a   100   100   001    Old_age   Always       -       0
  8 Seek_Time_Performance   0x0004   140   140   020    Old_age   Offline      -       15
  9 Power_On_Hours          0x0012   098   098   000    Old_age   Always       -       17283
 10 Spin_Retry_Count        0x0012   100   100   001    Old_age   Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   000    Old_age   Always       -       26
 22 Unknown_Attribute       0x0023   100   100   025    Pre-fail  Always       -       100
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       765
193 Load_Cycle_Count        0x0012   100   100   000    Old_age   Always       -       765
194 Temperature_Celsius     0x0002   060   060   000    Old_age   Always       -       34 (Min/Max 20/47)
196 Reallocated_Event_Count 0x0032   100   100   000    Old_age   Always       -       0
197 Current_Pending_Sector  0x0022   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0008   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x000a   100   100   000    Old_age   Always       -       0

"""

SMARTCTL_HHD2_ATTRIBUTES_SCAN1: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-9-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 10
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000f   083   064   044    Pre-fail  Always       -       209989296
  3 Spin_Up_Time            0x0003   083   083   000    Pre-fail  Always       -       0
  4 Start_Stop_Count        0x0032   100   100   020    Old_age   Always       -       31
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000f   085   060   045    Pre-fail  Always       -       301861854
  9 Power_On_Hours          0x0032   077   077   000    Old_age   Always       -       20303
 10 Spin_Retry_Count        0x0013   100   100   097    Pre-fail  Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   020    Old_age   Always       -       31
 18 Head_Health             0x000b   100   100   050    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
188 Command_Timeout         0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0022   056   047   040    Old_age   Always       -       44 (Min/Max 22/52)
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       25
193 Load_Cycle_Count        0x0032   079   079   000    Old_age   Always       -       43592
194 Temperature_Celsius     0x0022   044   053   000    Old_age   Always       -       44 (0 15 0 0 0)
195 Hardware_ECC_Recovered  0x001a   083   064   000    Old_age   Always       -       209989296
197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0
240 Head_Flying_Hours       0x0000   100   253   000    Old_age   Offline      -       14013h+51m+56.618s
241 Total_LBAs_Written      0x0000   100   253   000    Old_age   Offline      -       57460727660
242 Total_LBAs_Read         0x0000   100   253   000    Old_age   Offline      -       598694369133

"""

SMARTCTL_HHD2_ATTRIBUTES_SCAN2: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-10-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 10
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000f   068   064   044    Pre-fail  Always       -       6583600
  3 Spin_Up_Time            0x0003   083   083   000    Pre-fail  Always       -       0
  4 Start_Stop_Count        0x0032   100   100   020    Old_age   Always       -       32
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000f   085   060   045    Pre-fail  Always       -       308679715
  9 Power_On_Hours          0x0032   077   077   000    Old_age   Always       -       20639
 10 Spin_Retry_Count        0x0013   100   100   097    Pre-fail  Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   020    Old_age   Always       -       32
 18 Head_Health             0x000b   100   100   050    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
188 Command_Timeout         0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0022   055   047   040    Old_age   Always       -       45 (Min/Max 38/51)
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       26
193 Load_Cycle_Count        0x0032   078   078   000    Old_age   Always       -       44639
194 Temperature_Celsius     0x0022   045   053   000    Old_age   Always       -       45 (0 15 0 0 0)
195 Hardware_ECC_Recovered  0x001a   068   064   000    Old_age   Always       -       6583600
197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0
240 Head_Flying_Hours       0x0000   100   253   000    Old_age   Offline      -       14210h+41m+09.495s
241 Total_LBAs_Written      0x0000   100   253   000    Old_age   Offline      -       57662249124
242 Total_LBAs_Read         0x0000   100   253   000    Old_age   Offline      -       617143440379

"""

SMARTCTL_HHD2_ATTRIBUTES_SCAN3: bytes = b"""smartctl 7.3 2022-02-28 r5338 [x86_64-linux-6.8.12-9-pve] (local build)
Copyright (C) 2002-22, Bruce Allen, Christian Franke, www.smartmontools.org

=== START OF READ SMART DATA SECTION ===
SMART Attributes Data Structure revision number: 10
Vendor Specific SMART Attributes with Thresholds:
ID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE
  1 Raw_Read_Error_Rate     0x000f   082   064   044    Pre-fail  Always       -       167779088
  3 Spin_Up_Time            0x0003   083   083   000    Pre-fail  Always       -       0
  4 Start_Stop_Count        0x0032   100   100   020    Old_age   Always       -       32
  5 Reallocated_Sector_Ct   0x0033   100   100   010    Pre-fail  Always       -       0
  7 Seek_Error_Rate         0x000f   085   060   045    Pre-fail  Always       -       305612118
  9 Power_On_Hours          0x0032   077   077   000    Old_age   Always       -       20471
 10 Spin_Retry_Count        0x0013   100   100   097    Pre-fail  Always       -       0
 12 Power_Cycle_Count       0x0032   100   100   020    Old_age   Always       -       32
 18 Head_Health             0x000b   100   100   050    Pre-fail  Always       -       0
187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0
188 Command_Timeout         0x0032   100   100   000    Old_age   Always       -       0
190 Airflow_Temperature_Cel 0x0022   062   047   040    Old_age   Always       -       38 (Min/Max 38/48)
192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       26
193 Load_Cycle_Count        0x0032   078   078   000    Old_age   Always       -       44129
194 Temperature_Celsius     0x0022   038   053   000    Old_age   Always       -       38 (0 15 0 0 0)
195 Hardware_ECC_Recovered  0x001a   082   064   000    Old_age   Always       -       167779088
197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0
198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0
199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0
240 Head_Flying_Hours       0x0000   100   253   000    Old_age   Offline      -       14118h+48m+47.984s
241 Total_LBAs_Written      0x0000   100   253   000    Old_age   Offline      -       57553430308
242 Total_LBAs_Read         0x0000   100   253   000    Old_age   Offline      -       609342591200

"""
