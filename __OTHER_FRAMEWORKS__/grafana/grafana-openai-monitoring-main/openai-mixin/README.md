# OpenAI Monitoring Mixin

The OpenAI mixin is a set of configurable Grafana dashboards and alerts.

The OpenAI mixin contains the following dashboards:

- OpenAI

and the following alerts:

- HighCompletionTokensUsage
- HighPromptTokensUsage
- HighTotalTokensUsage
- LongRequestDuration
- HighUsageCost

## OpenAI Monitoring Dashboard Overview
OpenAI Monitoring dashbaord provides details on the overall status of the OpenAI Usage including the average cost and model usage. The dashboard includes visualizations to track average requests duration along with token usage.

![Dashboard_1](https://storage.googleapis.com/grafanalabs-integration-assets/openai/screenshots/openai_monitoring_1.png)
![Dashboard_2](https://storage.googleapis.com/grafanalabs-integration-assets/openai/screenshots/openai_monitoring_2.png)

## Alerts Overview
1. HighCompletionTokensUsage:

- Threshold: sum by (model) (openai_completionTokens) > 10000
- Description: This alert will trigger if the sum of openai_completionTokens exceeds 10,000 over a 5-minute window.
- Severity: Critical
- Use Case: This alert is for a critical condition where excessive completion token usage is detected. 

2. HighPromptTokensUsage:

- Threshold: sum by (model) (openai_promptTokens) > 5000
- Description: This alert will trigger if the sum of openai_promptTokens exceeds 5,000 over a 5-minute window.
- Severity: Warning
- Use Case: This alert is for a warning condition indicating elevated prompt token usage.

3. HighTotalTokensUsage:

- Threshold: sum by (model) (openai_totalTokens) > 15000
- Description: This alert will trigger if the sum of openai_totalTokens exceeds 15,000 over a 5-minute window.
- Severity: Critical
- Use Case: This alert is for critical situations when the total token usage is deemed too high. 

4. LongRequestDuration:

- Threshold: max by (model) (openai_requestDuration) > 2
- Description: This alert will trigger if the maximum request duration for any model exceeds 2 seconds over a 2-minute window.
- Severity: Warning
- Use Case: This alert is for warning about unusually long request durations. 

5. HighUsageCost:

- Threshold: sum by (model) (openai_usageCost) > 100
- Description: This alert will trigger if the sum of openai_usageCost exceeds 100 over a 5-minute window.
- Severity: Critical
- Use Case: This alert is for critical cost-related issues.

## Tools
To use them, you need to have `mixtool` and `jsonnetfmt` installed. If you have a working Go development environment, it's easiest to run the following:

```bash
$ go get github.com/monitoring-mixins/mixtool/cmd/mixtool
$ go get github.com/google/go-jsonnet/cmd/jsonnetfmt
```

You can then build a directory `dashboard_out` with the JSON dashboard files for Grafana:

```bash
$ make build
```

For more advanced uses of mixins, see [Prometheus Monitoring Mixins docs](https://github.com/monitoring-mixins/docs).
