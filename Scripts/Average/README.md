### Prometheus Floating Average

Average is a simple python script for calculating and providing prometheus a floating average of memory free as reported by [node-exporter](https://github.com/prometheus/node_exporter). The basic idea is for Python to query the Prometheus database for data, run some calculations on the data from the query, and make the result scrapeable by the Prometheus installation. 

    picture here

As pictured, our setup with the script utilized the [Prometheus pushgateway](https://github.com/prometheus/pushgateway). The pushgateway was used for testing purposes. If you intend to create permanant custom metrics, it is recommended to use one of the [prometheus client](https://github.com/prometheus/client_python) libraries instead.
