export JAVA_HOME =/ home / master / jdk1 .8.0 _92
export PATH =$ JAVA_HOME / bin: $ PATH
export HADOOP_HOME =$ HOME / hadoop -3.3.6
export HADOOP_CONF_DIR =$ HADOOP_HOME / etc / hadoop
export HADOOP_MAPRED_HOME =$ HADOOP_HOME
export HADOOP_COMMON_HOME =$ HADOOP_HOME
export HADOOP_HDFS_HOME =$ HADOOP_HOME
export YARN_HOME =$ HADOOP_HOME
export PATH =$ PATH: $ HADOOP_HOME / bin
export PATH =$ PATH: $ HADOOP_HOME / sbin
export HIVE_HOME =/ opt / hive
export HIVE_CONF_DIR =$ HIVE_HOME / conf
export HADOOP_CLASSPATH =$ HADOOP_HOME / lib /* : $ HADOOP_CONF_DIR
export PATH =$ PATH: $ HIVE_HOME / bin
export CLASSPATH =$ CLASSPATH: / opt / hive / lib / mysql - connector -j -8.0.32. jar
export SPARK_HOME =/ opt / spark # Adaptez le chemin selon votre install >
export PATH =$ PATH: $ SPARK_HOME / bin: $ SPARK_HOME / sbin
export PYSPARK_PYTHON =/ home / master / spark_env / bin / python3
export PYSPARK_DRIVER_PYTHON =/ home / master / spark_env / bin / python3
export PYSPARK_DRIVER_PYTHON_OPTS =’notebook ’
export SUPERSET_CONFIG_PATH ="/ home / master / superset / superset_config .py"
export FLASK_APP = superset
export PATH ="$ HOME /. pyenv / bin: $ PATH "
eval "$( pyenv ␣ init ␣ -)"
eval "$( pyenv ␣ virtualenv - init ␣ -)"
export NVM_DIR ="$ HOME /. config /nvm "
[ -s "$ NVM_DIR /nvm.sh" ] && \. "$ NVM_DIR / nvm .sh" # This loads nvm
[ -s "$ NVM_DIR / bash_completion " ] && \. "$ NVM_DIR / bash_completion "