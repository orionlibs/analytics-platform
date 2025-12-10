// Function to check if all required arguments are provided and modify metrics and logs URLs
export function check(metrics_url, logs_url, metrics_username, logs_username, access_token) {
    const requiredParameters = ['metrics_url', 'logs_url', 'metrics_username', 'logs_username', 'access_token'];
    
    // Check if all required parameters exist
    for (const param of requiredParameters) {
        if (!eval(param)) {
        throw new Error(`The "${param}" parameter is missing.`);
        }
    }
    
    // Check if 'api/prom' is present in the metrics URL
    if (!metrics_url.includes('api/prom')) {
      throw new Error("Invalid metrics URL format. It should contain 'api/prom' in the URL.");
    }

    // Check if 'api/v1/push' is present in the logs URL
    if (!logs_url.includes('api/v1/push')) {
      throw new Error("Invalid logs URL format. It should contain 'loki/api/v1/push' in the URL.");
    }
  
    // Convert metrics_url to use the influx line protocol URL
    if (metrics_url.includes('prometheus')) {
      metrics_url = metrics_url.replace('prometheus', 'influx').replace('api/prom', 'api/v1/push/influx/write');
  
      // Special case exception for prometheus-us-central1
      if (metrics_url.includes('-us-central1')) {
        metrics_url = metrics_url.replace('-us-central1', '-prod-06-prod-us-central-0');
      }
    }

    // Return metrics_url and logs_url without the trailing slash
    return {
      metrics_url: metrics_url.endsWith('/') ? metrics_url.slice(0, -1) : metrics_url,
      logs_url: logs_url.endsWith('/') ? logs_url.slice(0, -1) : logs_url,
    };
}

// Function to calculate the cost based on the model, prompt tokens, and sampled tokens
export function calculateCost(model, promptTokens, sampledTokens) {
    // Define the pricing information for different models
    const prices = {
      "ada": [0.0004, 0.0004],
      "text-ada-001": [0.0004, 0.0004],
      "babbage": [0.0004, 0.0004],
      "babbage-002": [0.0004, 0.0004],
      "text-babbage-001": [0.0004, 0.0004],
      "curie": [0.0020, 0.0020],
      "text-curie-001": [0.0020, 0.0020],
      "davinci": [0.0020, 0.0020],
      "davinci-002": [0.0020, 0.0020],
      "text-davinci-001": [0.0020, 0.0020],
      "text-davinci-002": [0.0020, 0.0020],
      "text-davinci-003": [0.0020, 0.0020],
      "gpt-3.5-turbo": [0.0010, 0.0020],
      "gpt-3.5-turbo-16k": [0.003, 0.004],
      "gpt-3.5-turbo-instruct": [0.0015, 0.0020],
      "gpt-4": [0.03, 0.06],
      "gpt-gpt-4-32k": [0.06, 0.12],
      "gpt-4-32k": [0.06, 0.12],
      "gpt-4-1106-preview": [0.01, 0.03],
      "gpt-4-1106-vision-preview": [0.01, 0.03],
    };
    
    // Use destructuring to get the promptPrice and sampledPrice
    const [promptPrice, sampledPrice] = prices[model] || [0, 0];
  
    // Calculate the total cost based on prompt and sampled tokens
    const cost = (promptTokens / 1000) * promptPrice + (sampledTokens / 1000) * sampledPrice;
  
    return cost;
}
// Function to send logs to the specified logs URL
export async function sendLogs(logs_url, logs_username, access_token, logs) {
  try {
      const response = await fetch(logs_url, {
          method: 'post',
          headers: {
              'Content-Type': 'application/json',
              'Authorization': `Basic ${btoa(`${logs_username}:${access_token}`)}`,
          },
          body: JSON.stringify(logs),
          timeout: 60000, // 60 seconds
      });

      if (!response.ok) {
          throw new Error(`Error sending Logs: HTTP status ${response.status}`);
      }

      return response;
  } catch (err) {
      throw new Error(`Error sending Logs: ${err.message}`);
  }
}


// Function to send metrics to the specified metrics URL
export async function sendMetrics(metrics_url, metrics_username, access_token, metrics) {
    try {
      const body = metrics.join('\n');
      const response = await fetch(metrics_url, {
        method: 'post',
        headers: {
          'Content-Type': 'text/plain',
          'Authorization': `Bearer ${metrics_username}:${access_token}`,
        },
        body: body,
        timeout: 60000, // 60 seconds
      });
  
      if (!response.ok) {
        throw new Error(`Error sending Metrics: HTTP status ${response.status}`);
      }
  
      return response;
    } catch (err) {
      throw new Error(`Error sending Metrics: ${err}`);
    }
  }
