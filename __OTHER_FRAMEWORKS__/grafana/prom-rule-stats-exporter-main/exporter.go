package main

import (
	"context"
	"fmt"
	"time"

	"github.com/go-kit/kit/log"
	"github.com/go-kit/kit/log/level"
	"github.com/prometheus/client_golang/api"
	v1 "github.com/prometheus/client_golang/api/prometheus/v1"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/common/config"
)

var (
	promScrapeDurationDesc = prometheus.NewDesc(
		"rulestats_prometheus_scrape_duration_seconds",
		"Time taken to call the Prometheus API.",
		nil, nil,
	)
	promUpDesc = prometheus.NewDesc(
		"rulestats_prometheus_up",
		"If the Prometheus API call succeeded.",
		nil, nil,
	)
	ruleEvalDurationDesc = prometheus.NewDesc(
		"rulestats_prometheus_rule_evaluation_last_duration_seconds",
		"The last evaluation duration for the rule",
		[]string{"group", "file", "rule"}, nil,
	)
	ruleEvalSuccessDesc = prometheus.NewDesc(
		"rulestats_prometheus_rule_evaluation_success",
		"If the last rule evaluation succeeded or not.",
		[]string{"group", "file", "rule"}, nil,
	)
)

type exporter struct {
	v1API   v1.API
	timeout time.Duration

	logger log.Logger
}

func NewExporter(logger log.Logger, addr, user, password string, timeout time.Duration) (*exporter, error) {
	rt := api.DefaultRoundTripper
	if user != "" {
		rt = config.NewBasicAuthRoundTripper(user, config.Secret(password), "", api.DefaultRoundTripper)
	}
	promClient, err := api.NewClient(api.Config{
		Address:      addr,
		RoundTripper: rt,
	})
	if err != nil {
		return nil, err
	}

	v1api := v1.NewAPI(promClient)

	return &exporter{
		v1API:   v1api,
		timeout: timeout,

		logger: logger,
	}, nil
}

func (e *exporter) Describe(ch chan<- *prometheus.Desc) {
	ch <- promScrapeDurationDesc
	ch <- promUpDesc
	ch <- ruleEvalDurationDesc
	ch <- ruleEvalSuccessDesc
}

func (e *exporter) Collect(ch chan<- prometheus.Metric) {
	// Make a request to the rules API.
	ctx, cancel := context.WithTimeout(context.Background(), e.timeout)
	defer cancel()

	now := time.Now()
	rulesResult, err := e.v1API.Rules(ctx)
	ch <- prometheus.MustNewConstMetric(promScrapeDurationDesc, prometheus.GaugeValue, float64(time.Since(now).Seconds()))

	if err != nil {
		level.Error(e.logger).Log("msg", "prometheus rules API", "err", err)
		ch <- prometheus.MustNewConstMetric(promUpDesc, prometheus.GaugeValue, 0)
		return
	}
	ch <- prometheus.MustNewConstMetric(promUpDesc, prometheus.GaugeValue, 1)

	for _, grp := range rulesResult.Groups {
		for idx, rule := range grp.Rules {
			switch v := rule.(type) {
			case v1.RecordingRule:
				ch <- prometheus.MustNewConstMetric(ruleEvalDurationDesc, prometheus.GaugeValue, v.EvaluationTime, grp.Name, grp.File, fmt.Sprintf("%d:%s", idx, v.Name))
				success := 1.0
				if v.Health != v1.RuleHealthGood {
					success = 0
				}
				ch <- prometheus.MustNewConstMetric(ruleEvalSuccessDesc, prometheus.GaugeValue, success, grp.Name, grp.File, fmt.Sprintf("%d:%s", idx, v.Name))
			case v1.AlertingRule:
				ch <- prometheus.MustNewConstMetric(ruleEvalDurationDesc, prometheus.GaugeValue, v.EvaluationTime, grp.Name, grp.File, fmt.Sprintf("%d:%s", idx, v.Name))
				success := 1.0
				if v.Health != v1.RuleHealthGood {
					success = 0
				}
				ch <- prometheus.MustNewConstMetric(ruleEvalSuccessDesc, prometheus.GaugeValue, success, grp.Name, grp.File, fmt.Sprintf("%d:%s", idx, v.Name))
			}
		}
	}
}
