# OpenAI Monitoring: Monitor OpenAI API Usage with Grafana Cloud
[![Grafana](https://img.shields.io/badge/grafana-%23F46800.svg?&logo=grafana&logoColor=white)](https://grafana.com)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/grafana/grafana-openai-monitoring)](https://github.com/grafana/grafana-openai-monitoring/tags)
[![GitHub Contributors](https://img.shields.io/github/contributors/grafana/grafana-openai-monitoring)](https://github.com/grafana/grafana-openai-monitoring/tags)

[![Node.js Tests](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/nodejs-tests.yml/badge.svg?branch=main)](https://github.com/grafana/grafana-openai-monitoring/actions/workflows/nodejs-tests.yml)

[grafana-openai-monitoring](https://www.npmjs.com/package/grafana-openai-monitoring) is an NPM Package that provides a way to monitor chat completions and Completions endpoints of the OpenAI API. It facilitates sending metrics and logs to **Grafana Cloud**, allowing you to track and analyze OpenAI API usage and responses.

## Installation
You can install grafana-openai-monitoring using npm:

```bash
npm install grafana-openai-monitoring
```

## Usage

The following tables shows which OpenAI function correspons to which monitoing function in this library

| OpenAI Function                 | Monitoring Function |
|---------------------------------|---------------------|
| openai.ChatCompletion.create	  | chat_v2.monitor    |
| openai.Completion.create	      | chat_v1.monitor    |

### ChatCompletions

To monitor ChatCompletions using the OpenAI API, you can use the `chat_v2.monitor` decorator. This decorator automatically tracks API calls and sends metrics and logs to the specified Grafana Cloud endpoints.

Here's how to set it up:

```javascript
import OpenAI from 'openai';
import { chat_v2 } from 'grafana-openai-monitoring';

const openai = new OpenAI({
  apiKey: 'YOUR_OPENAI_API_KEY',
});

// Patch method
chat_v2.monitor(openai, {
  metrics_url: 'YOUR_PROMETHEUS_METRICS_URL',
  logs_url: 'YOUR_LOKI_LOGS_URL',
  metrics_username: 'YOUR_METRICS_USERNAME',
  logs_username: 'YOUR_LOGS_USERNAME',
  access_token: 'YOUR_ACCESS_TOKEN',
});

// Now any call to openai.chat.completions.create will be automatically tracked
async function main() {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    max_tokens: 100,
    messages: [{ role: 'user', content: 'What is Grafana?' }],
  });
  console.log(completion);
}

main();
```

### Completions

To monitor completions using the OpenAI API, you can use the `chat_v1.monitor` decorator. This decorator adds monitoring capabilities to the OpenAI API function and sends metrics and logs to the specified Grafana Cloud endpoints.

Here's how to apply it:

```javascript
import OpenAI from 'openai';
import { chat_v1 } from 'grafana-openai-monitoring';

const openai = a new OpenAI({
  apiKey: 'YOUR_OPENAI_API_KEY',
});

// Patch method
chat_v1.monitor(openai, {
  metrics_url: 'YOUR_PROMETHEUS_METRICS_URL',
  logs_url: 'YOUR_LOKI_LOGS_URL',
  metrics_username: 'YOUR_METRICS_USERNAME',
  logs_username: 'YOUR_LOGS_USERNAME',
  access_token: 'YOUR_ACCESS_TOKEN',
});

// Now any call to openai.completions.create will be automatically tracked
async function main() {
  const completion = await openai.completions.create({
    model: 'davinci',
    max_tokens: 100,
    prompt: 'Isn\'t Grafana the best?',
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
Node.js version 16 and above

## Dependencies
- [OpenAI](https://www.npmjs.com/package/openai)

## License
This project is licensed under the  GPL-3.0 license - see the [LICENSE](LICENSE.txt) for details.
