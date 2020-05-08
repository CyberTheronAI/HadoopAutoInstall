This package is to install and config the hadoop

PreRequisite:
  1.java 1.8 to be downloaded from Oracle website
  2. hadoop to be downloaded from apache hadoop
  
Procedure to Install:
  1.Navigate to the respective download folder
  2.Edit the data.json file for file names and folder path
  3.Make sure the folder contains java and hadoop file downloaded
  4.Then execute sshConfig.py file with command "```python sshConfig.py```" and when prompted for ssh key name press "enter" and proceed
  5.Then execute javaHadoopConfig.py with command "```sudo python javaHadoopConfig.py data.json```"
  Sit back and Relax till your Hadoop gets Configured..
  
  Web Interfaces:
    1.Resource Manager:http://localhost:8088
    2.Web UI of the namenode daemon: http://localhost:50070
    3.HDFS Namenode web interface: http://localhost:8042
    
Note:
  This procedure successfully tested with hadoop 2.7.7 and 3.2.2 and should work fine with all later releases too..
