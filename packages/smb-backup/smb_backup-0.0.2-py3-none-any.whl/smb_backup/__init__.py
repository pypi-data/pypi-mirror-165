import smbclient
import tarfile
import logging
import os
from datetime import datetime
import shutil

class SMB_Backup(object):
    def __init__(self,server:str,share:str,username:str,password:str,temp_dir:str="temp",retention:int=10) -> None:
        self._server = server
        self._share = share
        self._username = username
        self._password = password
        self._temp_dir = os.path.abspath(temp_dir) 
        self._retention = retention
        smbclient.ClientConfig(username=self._username, password=self._password)
    
    @property
    def _connection_url(self)->str:
        return f"\\\\{self._server}\{self._share}"
        
    def _create_tar_file(self,output_filename:str, source_dir:str)->tuple[str,str]:
        archive = f"{output_filename}.tar.gz"
        path = os.path.join(self._temp_dir,archive)
        with tarfile.open(path, "w:gz") as tar:
            tar.add(source_dir, arcname=os.path.basename(source_dir))
        return archive,path
      
    def backup(self,source_dir:str,dest_dir:str)->bool:
        
        if not os.path.isdir(source_dir):
            return False
        
        #clear the tempdir 
        if os.path.isdir(self._temp_dir):
            shutil.rmtree(self._temp_dir)
        os.makedirs(self._temp_dir)
         
        #create the tar file     
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        try:
            archive,path = self._create_tar_file(now,source_dir)
        except Exception:
            logging.exception("Failed to create archive!")
            return False
        
        #upload to the smb drive
        try:
            smbclient.makedirs(f'{self._connection_url}\\{dest_dir}',exist_ok=True)
            with smbclient.open_file(f'{self._connection_url}\\{dest_dir}\\{archive}', mode="xb") as target:
                with open(path,"rb") as source:
                    target.write(source.read())
                    target.flush()
                    
            os.remove(path)
            
        except Exception:
            logging.exception("Failed to upload archive to SMB!")
            return False
        
        #delete old  backups if necessary
        if self._retention and self._retention > 0:
            try:
                existing_backups = smbclient.listdir(f'{self._connection_url}\\{dest_dir}')
                if len(existing_backups) > self._retention:
                    times = sorted([datetime.strptime(backup.split(".")[0],"%Y-%m-%d_%H-%M-%S") for backup in existing_backups],reverse=True)
                    for time_to_delete in times[self._retention:]:
                        formated_time = time_to_delete.strftime("%Y-%m-%d_%H-%M-%S")
                        file_to_delete = f"{formated_time}.tar.gz"
                        smbclient.remove(f'{self._connection_url}\\{dest_dir}\\{file_to_delete}')  	
            except Exception:
                logging.exception("Failed to create archive!")
                return False
            
        return True