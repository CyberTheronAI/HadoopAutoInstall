import ctaiLib

user_home=ctaiLib.userHomeDirPath()
print(user_home)

ctaiLib.executeCmd('yes | sudo apt-get purge openssh-server')
print('ssh purged')

ctaiLib.executeCmd('yes | sudo apt-get install openssh-server')
print('ssh installed')

ctaiLib.executeCmd('ssh-keygen -t rsa -P ""')
ctaiLib.executeCmd('cat {loc}/.ssh/id_rsa.pub >> {loc}/.ssh/authorized_keys'.format(loc=user_home))
ctaiLib.executeCmd('ssh localhost')


