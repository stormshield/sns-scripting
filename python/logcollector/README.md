# Log Collector

This script connects to a SNS appliance and archive the logs.

Note: this tool can only archive the logs from a product with a log partition (hard drive of flash card).

# Configuration

Edit the `logcollector.ini` file and fill with your appliance settings:
```
[Config]
host=10.0.0.254
user=admin
password=secret
limit=5000
log_dir=./log
```

`log_dir` is the local folder which will contain the log archive.

Edit the `last.ini` file and create a section for each log type you want to archive with the date of the first log.

For example, to archive the 'connection' log since the beginning of the year 2020, add this section: 

```
[connection]
time = 2020-01-01 00:00:00
tz = +0100
```

# Usage

Run `logcollector.py` regularly (put an entry in the crontab), the script will download the logs since the last execution and keep track of the last downloaded log dates.
