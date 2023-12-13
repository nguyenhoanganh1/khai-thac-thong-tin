hdfs_object = pydoop.hdfs.hdfs(host='url of the file system goes here',
                               port=9864, user=None, groups=None)
hdfs_object.list_directory("/vs_co2_all_2019_v1.csv")
