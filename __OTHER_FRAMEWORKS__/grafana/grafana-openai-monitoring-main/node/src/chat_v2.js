import { check, calculateCost, sendMetrics, sendLogs } from './helpers.js';

export default function monitor_v2(openai, options = {}) {
  const {
    metrics_url,
    logs_url,
    metrics_username,
    logs_username,
    access_token,
  } = options;

  const validatedURL = check(metrics_url, logs_url, metrics_username, logs_username, access_token)

  // Save original method
  const originalMethod = openai.chat.completions.create;

  // Define wrapped method
  openai.chat.completions.create = async function(params) {
    const start = performance.now();
    // Call original method
    const response = await originalMethod.call(this, params);
    const end = performance.now();
    const duration = (end - start) / 1000;

    // Calculate the cost based on the response's usage
    const cost = calculateCost(params.model, response.usage.prompt_tokens, response.usage.completion_tokens);

    // Prepare logs to be sent
    const logs = {
      streams: [
        {
          stream: {
            job: 'integrations/openai',
            prompt: params.messages[0].content,
            model: response.model,
            role: response.choices[0].message.role,
            finish_reason: response.choices[0].finish_reason,
            prompt_tokens: response.usage.prompt_tokens.toString(),
            completion_tokens: response.usage.completion_tokens.toString(),
            total_tokens: response.usage.total_tokens.toString(),
          },
          values: [
            [
              (Math.floor(Date.now() / 1000) * 1000000000).toString(),
              response.choices[0].message.content,
            ],
          ],
        },
      ],
    };

    // Send logs to the specified logs URL
    sendLogs(logs_url, logs_username, access_token, logs);

    // Prepare metrics to be sent
    const metrics = [
      // Metric to track the number of completion tokens used in the response
      `openai,job=integrations/openai,source=node_chatv2,model=${response.model} completionTokens=${response.usage.completion_tokens}`,

      // Metric to track the number of prompt tokens used in the response
      `openai,job=integrations/openai,source=node_chatv2,model=${response.model} promptTokens=${response.usage.prompt_tokens}`,

      // Metric to track the total number of tokens used in the response
      `openai,job=integrations/openai,source=node_chatv2,model=${response.model} totalTokens=${response.usage.total_tokens}`,

      // Metric to track the duration of the API request and response cycle
      `openai,job=integrations/openai,source=node_chatv2,model=${response.model} requestDuration=${duration}`,

      // Metric to track the usage cost based on the model and token usage
      `openai,job=integrations/openai,source=node_chatv2,model=${response.model} usageCost=${cost}`,
    ];

    sendMetrics(validatedURL.metrics_url, metrics_username, access_token, metrics)
    .catch((error) => {
      console.error(error.message);
    });

    // Return original response
    return response;
  };
}
