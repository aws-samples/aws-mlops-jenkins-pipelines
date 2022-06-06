## Build Docker image for Jenkins

```
docker build -t local_jenkins .
```

## Start Jenkins

### Create jenkins folder under `/opt/docker/jenkins/jenkins_home`

```
mkdir -p /opt/docker/jenkins/jenkins_home
```

### Ensure the user has the right permissions to read and write

```
chmod 755 /opt/docker/jenkins/jenkins_home
```

```
chown <USER> /opt/docker/jenkins/jenkins_home
```

### Run the container

```
docker run --name jenkins -i -d -p 8787:8080 -p 50000:50000 -v /opt/docker/jenkins/jenkins_home:/var/jenkins_home:rw --privileged local_jenkins
```