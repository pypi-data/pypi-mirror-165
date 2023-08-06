<div id="logos">
    <p align="center">
        <img src="https://tc.com.br/wp-content/themes/tradersclub/img/tc-out.png" width="150" height="150">
    </p>
</div>   
<br>

<h1 align="center">TCLogger</h1>
<h2 align="center">This lib was created to send logs to splunk easily. This framework uses logstream to receive logs and send to splunk</h2>
<br>
<br>

<h1 align="left">Import</h1>

```py
from TCLogger import error, info, warning, success
```

<br>

<h2 align="left">error, warning, info, success</h2>

<br>

```py
data = {
    'feature': {
        'type': 'cloud_function',
        'name': os.getenv('FUNCTION_NAME'),
        'origin': 'gcp',
        'id': os.getenv('PROJECT_ID'),
        'destination': 'nats'
    },
    'uid': 'psahfj2n4j12b3kh12j',
    'action': 'publish',
    'level': 'warning',
    'timestamp': "2021-11-22T22:22:00.1000Z"
}

tc_logs = TCLogger(logstream_host, logstream_path, logstream_token)

# publishing error message
TCLogger.error(data)

# publishing info message
TCLogger.info(data)

# publishing warning message
TCLogger.warning(data)

# publishing success message
TCLogger.error(data)

```