import json
import sys
import xml.etree.ElementTree
import ctaiLib


def setupJava():
    javaDownloadFile = ctaiLib.joinPath(data['installationLocation'], data['java_scr'])
    print(javaDownloadFile)
    ctaiLib.executeCmd("yes | sudo apt-get purge openjdk-\*")
    print("existing java removed from system")

    ctaiLib.executeCmd("yes | sudo tar -xvf " + javaDownloadFile)
    print("downloaded java file extracted")

    extractedJavaFolder = ''

    for file in ctaiLib.listDirCont(data['installationLocation']):
        if file.startswith('jdk') and not file.endswith('.gz'):
            extractedJavaFolder = file

    ctaiLib.executeCmd("sudo mv " + extractedJavaFolder + " " + data["javaFolder"])

    print("extracted java folder renamed")

    ctaiLib.executeCmd("sudo chmod +777 " + data["javaFolder"])

    javaSet = """JAVA_HOME={javapath}
    PATH=$PATH:$HOME/bin:$JAVA_HOME/bin
    export JAVA_HOME
    export PATH""".format(javapath=ctaiLib.joinPath(data['installationLocation'], data["javaFolder"]))

    print(javaSet)
    ctaiLib.executeCmd("cd")
    with open("/etc/profile", "a+") as f1:
        f1.write(javaSet + "\n")
        f1.seek(1, 0)
        command = f1.read()
        print(command)
    print('etc/profile set done')

    ctaiLib.executeCmd(". /etc/profile")
    javaDir = ctaiLib.joinPath(data['installationLocation'], data["javaFolder"])

    ctaiLib.executeCmd(
        'sudo update-alternatives --install "/usr/bin/java" "java" "{dirJava}/bin/java" 1'.format(dirJava=javaDir))
    ctaiLib.executeCmd(
        'sudo update-alternatives --install "/usr/bin/javac" "javac" "{dirJava}/bin/javac" 1'.format(dirJava=javaDir))
    ctaiLib.executeCmd('sudo update-alternatives --install "/usr/bin/javaws" "javaws" "{dirJava}/bin/javaws" 1'.format(
        dirJava=javaDir))

    ctaiLib.executeCmd('sudo update-alternatives --set java {dirJava}/bin/java'.format(dirJava=javaDir))
    ctaiLib.executeCmd('sudo update-alternatives --set javac {dirJava}/bin/javac'.format(dirJava=javaDir))
    ctaiLib.executeCmd('sudo update-alternatives --set javaws {dirJava}/bin/javaws'.format(dirJava=javaDir))
    ctaiLib.executeCmd('java -version')
    return ("Java setup Completed")

def setupHadoop():
    user_home = ctaiLib.userHomeDirPath()
    user = user_home.split('/')[2]
    print(user)

    global hadoopDownloadFile
    hadoopDownloadFile = ctaiLib.joinPath(data['installationLocation'], data['hadoop_src'])
    print(hadoopDownloadFile)

    ctaiLib.executeCmd("yes | sudo tar -xvf " + hadoopDownloadFile)
    print("downloaded hadoop file extracted")

    extractedHadoopFolder = ''
    for file in ctaiLib.listDirCont(data['installationLocation']):
        if file.startswith('hadoop') and not file.endswith('.gz'):
            extractedHadoopFolder = file
    print(extractedHadoopFolder)
    ctaiLib.executeCmd("sudo mv " + extractedHadoopFolder + " " + data["hadoop_folder"])

    print("extracted java folder renamed")

    ctaiLib.executeCmd("sudo chmod +777 " + data["hadoop_folder"])
    ctaiLib.executeCmd('cd')
    hadoopBash = """#Set HADOOP_HOME
    export HADOOP_HOME={dir1}
    #Set JAVA_HOME
    export JAVA_HOME={dir2}
    # Add bin/ directory of Hadoop to PATH
    export PATH=$PATH:$HADOOP_HOME/bin""".format(
        dir1=ctaiLib.joinPath(data['installationLocation'], data["hadoop_folder"]),
        dir2=ctaiLib.joinPath(data['installationLocation'], data["javaFolder"]))

    print(hadoopBash)
    ctaiLib.executeCmd("echo '{hdb}' >> ~/.bashrc ".format(hdb=hadoopBash))
    ctaiLib.executeCmd('. ~/.bashrc')
    global javaDir
    javaDir = ctaiLib.joinPath(data['installationLocation'], data["javaFolder"])
    global hadoopHome
    hadoopHome = ctaiLib.joinPath(data['installationLocation'], data["hadoop_folder"])
    global hadoopConfigFilePath
    hadoopConfigFilePath = hadoopHome + "/etc/hadoop/"
    print(hadoopConfigFilePath)

    ctaiLib.executeCmd("cd")
    with open("/etc/profile.d/hadoop.sh", "a+") as f1:
        f1.write("export HADOOP_HOME={dir}".format(dir=hadoopHome) + "\n")
        f1.seek(1, 0)
        command = f1.read()
        print(command)
    print('etc/profile.d/hadoop.sh set done')

    ctaiLib.executeCmd("sudo chmod +x /etc/profile.d/hadoop.sh")

    a = ("\n"
         "    export JAVA_HOME={JAVA_HOME}\n"
         "    \n"
         "    export HADOOP_CONF_DIR=${HADOOP_CONF_DIR:-\"/etc/hadoop\"}\n"
         "    \n"
         "    for f in $HADOOP_HOME/contrib/capacity-scheduler/*.jar; do\n"
         "      if [ \"$HADOOP_CLASSPATH\" ]; then\n"
         "        export HADOOP_CLASSPATH=$HADOOP_CLASSPATH:$f\n"
         "      else\n"
         "        export HADOOP_CLASSPATH=$f\n"
         "      fi\n"
         "    done\n"
         "    \n"
         "    export HADOOP_OPTS=\"$HADOOP_OPTS -Djava.net.preferIPv4Stack=true\"\n"
         "    \n"
         "    export HADOOP_NAMENODE_OPTS=\"-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_NAMENODE_OPTS\"\n"
         "    export HADOOP_DATANODE_OPTS=\"-Dhadoop.security.logger=ERROR,RFAS $HADOOP_DATANODE_OPTS\"\n"
         "    \n"
         "    export HADOOP_SECONDARYNAMENODE_OPTS=\"-Dhadoop.security.logger=${HADOOP_SECURITY_LOGGER:-INFO,RFAS} -Dhdfs.audit.logger=${HDFS_AUDIT_LOGGER:-INFO,NullAppender} $HADOOP_SECONDARYNAMENODE_OPTS\"\n"
         "    \n"
         "    export HADOOP_NFS3_OPTS=\"$HADOOP_NFS3_OPTS\"\n"
         "    export HADOOP_PORTMAP_OPTS=\"-Xmx512m $HADOOP_PORTMAP_OPTS\"\n"
         "    \n"
         "    export HADOOP_CLIENT_OPTS=\"-Xmx512m $HADOOP_CLIENT_OPTS\"\n"
         "    \n"
         "    export HADOOP_SECURE_DN_USER=${HADOOP_SECURE_DN_USER}\n"
         "    \n"
         "    export HADOOP_SECURE_DN_LOG_DIR=${HADOOP_LOG_DIR}/${HADOOP_HDFS_USER}\n"
         "    \n"
         "    export HADOOP_PID_DIR=${HADOOP_PID_DIR}\n"
         "    export HADOOP_SECURE_DN_PID_DIR=${HADOOP_PID_DIR}\n"
         "    \n"
         "    export HADOOP_IDENT_STRING=$USER").format(JAVA_HOME=javaDir)
    print(a)
    with open(hadoopConfigFilePath + 'hadoop-env.sh', "w") as f1:
        f1.write(a)
        f1.close()

def writeXML(filename,conf):
    et = xml.etree.ElementTree.parse(filename)

    for m in conf:
        ptag = xml.etree.ElementTree.SubElement(et.getroot(), 'property')
        for k, v in m.items():
            if k == "name":
                ntag = xml.etree.ElementTree.SubElement(ptag, 'name')
                ntag.text = v
            elif k == "value":
                vtag = xml.etree.ElementTree.SubElement(ptag, 'value')
                vtag.text = v
    return et
def core_file(conf):

    filename = hadoopConfigFilePath + 'core-site.xml'
    et = writeXML(filename,conf)
    et.write(filename)
    ctaiLib.executeCmd("sudo mkdir -p /app/hadoop/tmp")
    ctaiLib.executeCmd("sudo chmod +777 /app/hadoop/tmp")
    ctaiLib.executeCmd("sudo chown -R {usr} /app/hadoop/tmp".format(usr=user))
    ctaiLib.executeCmd('cd')
    print('Core conf finished')


def hdfs_file(conf):
    filename = hadoopConfigFilePath + 'hdfs-site.xml'
    et = writeXML(filename,conf)
    ptag = xml.etree.ElementTree.SubElement(et.getroot(), 'property')
    ntag = xml.etree.ElementTree.SubElement(ptag, 'name')
    ntag.text = 'dfs.datanode.data.dir'
    vtag = xml.etree.ElementTree.SubElement(ptag, 'value')
    vtag.text = user_home + "/hdfs"
    et.write(filename)

    ctaiLib.executeCmd("sudo mkdir -p " + user_home + "/hdfs")
    ctaiLib.executeCmd("sudo chmod +777 " + user_home + "/hdfs")
    ctaiLib.executeCmd("sudo chown -R "+user+" " + user_home + "/hdfs")
    print('HDFS conf finished')


def mapred_file(conf):
    filename = hadoopConfigFilePath + 'mapred-site.xml'
    et = writeXML(filename, conf)
    et.write(filename)
    print('Mapred file finished')

if __name__ == '__main__':

    if sys.argv[1] is None or len(sys.argv) == 1:
        print('Usage: sudo python javaHadoopConfig.py data.json')
        sys.exit(1)

    global data
    global user_home
    global user

    with open(sys.argv[1], 'r') as json_data:
        data = json.load(json_data, strict=False)

    print(data)

    user_home = ctaiLib.userHomeDirPath()
    user = user_home.split('/')[2]

    print(user)

    setupJava()

    setupHadoop()

    core_file(data['core'])

    hdfs_file(data['hdfs'])
    global javaDir
    if "mapred-site.xml" in ctaiLib.listDirCont(hadoopConfigFilePath):
        print('mapred-site.xml is available')
        mapred_file(data['mapred'])
    else:
        print('mapred-site.xml is not available')
        ctaiLib.executeCmd("sudo cp {p}mapred-site.xml.template {p}mapred-site.xml".format(p=hadoopConfigFilePath))
        ctaiLib.executeCmd("sudo chmod +777 " + hadoopConfigFilePath + "mapred-site.xml")
        mapred_file(data['mapred'])

    ctaiLib.executeCmd(hadoopHome + "/bin/hdfs namenode -format")

    ctaiLib.executeCmd(hadoopHome + "/sbin/start-dfs.sh")
    ctaiLib.executeCmd(hadoopHome + "/sbin/start-yarn.sh")
    ctaiLib.executeCmd("alias jps='{r}/bin/jps'".format(r=javaDir))
    ctaiLib.executeCmd("jps")
