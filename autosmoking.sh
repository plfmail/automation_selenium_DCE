dceaddr=$(env | grep DCEADDR | awk -F '=' '{print $2}')
resultdir=/root/self_3/result
docker run -it -v $resultdir:/result -e DCEADDR=$dceaddr base-from-centos7.4:8.0