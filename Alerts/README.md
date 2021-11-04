### Alerting

Both Grafana and Prometheus support some variation of alerts for data. For this project, only the alerting functionality of prometheus is used. When using alerting with prometheus, configurations to the prometheus.yml file must be made. Additionally, a standalone service called "alertmanager" must be used for routing the alerts. 

#### Overview

Prometheus reads the prometheus.yml file on startup. In this file, the alertmanager instance must be set as a target. By default, alertmanager runs on port 9093.

#### Prometheus YAML Configurations for Alerting

To configure prometheus to work with our alertmanager running on port 9093, we must add a few lines to our prometheus.yml file:

    alerting:
      alertmanagers:
    - static_configs:
      - targets: ["localhost:9093"]

This will tell prometheus that our alertmanager server can be found on port 9093. Next, a rule file must be created that will contain the rules for our alerts. For this example, a new file was created called "alert_rules.yml". In this file, we put:

    groups:
      - name: alert_rules
      rules:
      - alert: TEST_ALERT
        expr: go_memstats_alloc_bytes_total{job="prometheus"} > 1
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: TST_MSG

To create a simple test rule. This alert will trigger after go_memstats_alloc_bytes_total > 1 for one minute, set by the "for" clause. For more information on alert rules, the documentation can be found [here](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/).

Next, we must edit the YAML file for the alertmanager. This is our alertmanager.yml file for this simple demonstration:

    route:
    group_by: ['alertname']
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 1h
    receiver: 'email'
    receivers:
    - name: 'email'
    email_configs:
        - to: 'target_email@example.com'
        from: 'your_email@gmail.com'
        smarthost: smtp.gmail.com:587
        auth_username: 'your_email@gmail.com'
        auth_identity: 'your_email@gmail.com'
        auth_password: 'your_password'
    inhibit_rules:
    - source_match:
        severity: 'critical'
        target_match:
        severity: 'warning'
        equal: ['alertname', 'dev', 'instance']

Depending on your email provider, you may have to adjust these settings. More documentation for alertmanager configuration can be found [here](https://prometheus.io/docs/alerting/latest/configuration/). 

Finally, we must also specify the rule file in the prometheus.yml file. To do this, we add:

    rule_files:
    - "alert_rules.yml"

To the file. "alert_rules.yml" should be set to whatever you named your alert rules file. After this, start/restart both prometheus and alertmanager after saving the configuration files. 

For debugging purposes, prometheus comes with a command line tool called promtool and alertmanager comes with amtool. These tools can be used to check configuration files for errors. To check if a rules file is valid, run:

    promtool check rules your_alert_file.yml

To check the alert manager configuration file run:

    amtool check-config your_am_config.yml

