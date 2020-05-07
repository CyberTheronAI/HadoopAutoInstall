This package is to install and config the hadoop

PreRequisite:
  java 1.8 to be downloaded from Oracle website/ can use the one in the directory
  hadoop to be downloaded from apache hadoop / can use the one in the directory
  
Procedure to Install:
  Navigate to the respective download folder
  Edit the data.json file for file names and folder path
  Make sure the folder contains java and hadoop file downloaded
  Then execute sshConfig.py file with command "python sshConfig.py" and new prompted or ssh key name press enter and proceed
  Then execute javaHadoopConfig.py with command "sudo python javaHadoopConfig.py data.json"
  Sit back and Relax till your Hadoop gets Configured..
  
  Web Interfaces:
    Resource Manager:http://localhost:8088
    Web UI of the namenode daemon: http://localhost:50070
    HDFS Namenode web interface: http://localhost:8042
    
Note:
  This procedure successfully tested with hadoop 2.7.7 and should work fine with all later releases too..
