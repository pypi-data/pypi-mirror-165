# python-smb-backup
Pytohn library to backup folders to a smb volume

## Installation

```
pip install smb-backup
```
## Usage
```
from smb_backup import SMB_Backup
# create a new backup object
smb_backup = SMB_Backup(SERVER,SHARE,USERNAME,PASSWORD,retention=RETENTION)
# backup a folder
smb_backup.backup(SOURCE_DIR,TARGET_DIR)
```
Depending on the retention-value the oldest backup will be deleted.