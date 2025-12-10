# Monitor OpenAI API Usage with Grafana Cloud

[![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?&logo=grafana&logoColor=white)](https://grafana.com)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/grafana/grafana-openai-monitoring)](https://github.com/grafana/grafana-openai-monitoring/tags)
[![GitHub Contributors](https://img.shields.io/github/contributors/grafana/grafana-openai-monitoring)](https://github.com/grafana/grafana-openai-monitoring/tags)

[![Python Tests](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/python-tests.yml)
[![Pylint](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/pylint.yml/badge.svg?branch=main)](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/pylint.yml)
[![Node.js Tests](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/nodejs-tests.yml/badge.svg?branch=main)](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/nodejs-tests.yml)


`grafana-openai-monitoring` is a set of libraries for both Python and JavaScript that provides decorators and functions to monitor chat completions and Completions endpoints of the OpenAI API. It facilitates sending metrics and logs to **Grafana Cloud**, allowing you to track and analyze OpenAI API usage and responses.

## Installation

### Python Library
You can install the [Python library](https://pypi.org/project/grafana-openai-monitoring/) using pip:

```bash
pip install grafana-openai-monitoring
```

### NPM Package
You can install the [NPM Package](https://www.npmjs.com/package/grafana-openai-monitoring) using npm:

```bash
npm install grafana-openai-monitoring
```

## Usage

### Python
The [Python library](https://pypi.org/project/grafana-openai-monitoring/) provides decorators to monitor chat completions and Completions endpoints of the OpenAI API. It automatically tracks API calls and sends metrics and logs to the specified Grafana Cloud endpoints.

Here's how to set it up:

```python
from openai import OpenAI
from grafana_openai_monitoring import chat_v2

client = OpenAI(
    api_key="YOUR_OPENAI_API_KEY",
)

# Apply the custom decorator to the OpenAI API function. To use with AsyncOpenAI, Pass use_async = True in this function.
client.chat.completions.create = chat_v2.monitor(
    client.chat.completions.create,
    metrics_url="YOUR_PROMETHEUS_METRICS_URL",
    logs_url="YOUR_LOKI_LOGS_URL",
    metrics_username="YOUR_METRICS_USERNAME",
    logs_username="YOUR_LOGS_USERNAME",
    access_token="YOUR_ACCESS_TOKEN"
)

# Now any call to client.chat.completions.create will be automatically tracked
response = client.chat.completions.create(model="gpt-4", max_tokens=100, messages=[{"role": "user", "content": "What is Grafana?"}])
print(response)
```

## JavaScript
The [NPM Package](https://www.npmjs.com/package/grafana-openai-monitoring) provides functions to monitor chat completions and Completions endpoints of the OpenAI API. It facilitates sending metrics and logs to the specified Grafana Cloud endpoints.

Here's how to set it up:

```javascript
import OpenAI from 'openai';
import { chat_v2 } from 'grafana-openai-monitoring';

const openai = new OpenAI({
  apiKey: 'YOUR_OPENAI_API_KEY',
});

const monitoringOptions = {
  metrics_url: 'YOUR_PROMETHEUS_METRICS_URL',
  logs_url: 'YOUR_LOKI_LOGS_URL',
  metrics_username: 'YOUR_METRICS_USERNAME',
  logs_username: 'YOUR_LOGS_USERNAME',
  access_token: 'YOUR_ACCESS_TOKEN',
};

chat_v2.monitor(openai, monitoringOptions);

// Now any call to openai.chat.completions.create will be automatically tracked
async function main() {
  const completion = await openai.completions.create({
    model: 'gpt-4',
    max_tokens: 100,
    messages: [{ role: 'user', content: 'What is Grafana?' }],
  });
  console.log(completion);
}

main();
```

## Configuration
To use the grafana-openai-monitoring library effectively, you need to provide the following information:

- **YOUR_OPENAI_API_KEY**: Replace this with your actual OpenAI API key.
- **YOUR_PROMETHEUS_METRICS_URL**: Replace the URL with your Prometheus URL.
- **YOUR_LOKI_LOGS_URL**: Replace with the URL where you want to send Loki logs.
- **YOUR_METRICS_USERNAME**: Replace with the username for Prometheus.
- **YOUR_LOGS_USERNAME**: Replace with the username for Loki.
- **YOUR_ACCESS_TOKEN**: Replace with the [Cloud Access Policy token](https://grafana.com/docs/grafana-cloud/account-management/authentication-and-permissions/access-policies/) required for authentication.

After configuring the parameters, the monitored API function will automatically log and track the requests and responses to the specified endpoints.

## Compatibility
- Python Library: Python 3.7.1 and above
- NPM Package: Node.js version 16 and above

## License
Both libraries are licensed under the  GPL-3.0 license. See the LICENSE files for details.
