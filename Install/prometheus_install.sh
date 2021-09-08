#!/bin/bash
#Assumes the required files are in the directory it was launched from
#prometheus.yml, prometheus.conf, node_exporter.service, prometheus.service
FILES=$(pwd)
mkdir Prometheus
cd Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.26.0/prometheus-2.26.0.linux-amd64.tar.gz
tar xvzf prometheus-2.26.0.linux-amd64.tar.gz
useradd -rs /bin/false prometheus
cd prometheus-2.26.0.linux-amd64
rm prometheus.yml
cp prometheus promtool /usr/local/bin

chown prometheus:prometheus /usr/local/bin/prometheus
mkdir /etc/prometheus
cd $FILES
cp prometheus.yml Prometheus/prometheus-2.26.0.linux-amd64
cd Prometheus/prometheus-2.26.0.linux-amd64
cp -R consoles/ console_libraries/ prometheus.yml /etc/prometheus
cd /
mkdir -p data/prometheus
chown -R prometheus:prometheus data/prometheus /etc/prometheus/*
cd $FILES
cp prometheus.service /lib/systemd/system
#Add test to see if nginx installed possibly, also probably not needed
apt-get install nginx
cp prometheus.conf /etc/nginx/conf.d
apt-get install apache2-utils
cd /etc/prometheus
htpasswd -c .credentials admin
#will get input from user
apt-get install gnutls-bin
cd /etc/ssl
mkdir prometheus
certtool --generate-privkey --outfile prometheus-private-key.pem
certtool --generate-self-signed --load-privkey prometheus-private-key.pem --outfile prometheus-cert.pem

cd $FILES/Prometheus
wget https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz
tar xvzf node_exporter-1.1.2.linux-amd64.tar.gz
cd node_exporter-1.1.2.linux-amd64
cp node_exporter /usr/local/bin
useradd -rs /bin/false node_exporter
chown node_exporter:node_exporter /usr/local/bin/node_exporter
cd $FILES
cp node_exporter.service /lib/systemd/system

systemctl daemon-reload
systemctl restart nginx
systemctl restart prometheus
systemctl start node_exporter

#Grafana
wget -q -O - https://packages.grafana.com/gpg.key | sudo apt-key add -
echo "deb https://packages.grafana.com/oss/deb stable main" | tee -a /etc/apt/sources.list.d/grafana.list

apt-get update
apt-get install grafana
systemctl start grafana-server
#NOTE: This will not disable anon access by default
#localhost:3000 for Grafana, localhost:9090 for Prometheus

