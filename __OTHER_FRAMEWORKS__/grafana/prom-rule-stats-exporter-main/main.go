package main

import (
	"log"
	"net/http"
	"os"

	"github.com/go-kit/kit/log/level"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/prometheus/common/promlog"
	promlogflag "github.com/prometheus/common/promlog/flag"
	"gopkg.in/alecthomas/kingpin.v2"
)

var (
	promlogConfig promlog.Config
)

func main() {
	app := kingpin.New("prom-rule-stats-exporter", "An exporter to export individual rule evaluation duration metrics.")
	// Log level.
	promlogflag.AddFlags(app, &promlogConfig)
	// Server configs.
	serverAddr := app.Flag("http.listen-address", "Address to listen on for scrapes.").Default("0.0.0.0:1234").String()
	// Prometheus configs.
	promAddr := app.Flag("prometheus.address", "Address to query Prometheus server on. Alternatively set $PROMETHEUS_ADDRESS").
		Envar("PROMETHEUS_ADDRESS").
		Required().
		String()
	promUser := app.Flag("prometheus.user", "Basic Auth username for the Prometheus instance. Alternatively set $PROMETHEUS_USER").
		Envar("PROMETHEUS_USER").
		Default("").
		String()
	promPassword := app.Flag("prometheus.password", "Basic Auth password for the Prometheus instance. Alternatively set $PROMETHEUS_PASSWORD").
		Envar("PROMETHEUS_PASSWORD").
		Default("").
		String()
	promTimeout := app.Flag("read-timeout", "Timeout for API calls").
		Default("30s").
		Duration()
	kingpin.MustParse(app.Parse(os.Args[1:]))

	logger := promlog.New(&promlogConfig)
	exporter, err := NewExporter(logger, *promAddr, *promUser, *promPassword, *promTimeout)
	if err != nil {
		level.Error(logger).Log("msg", "error initialising exporter", "err", err)
		os.Exit(-1)
	}
	reg := prometheus.NewPedanticRegistry()
	reg.MustRegister(
		prometheus.NewProcessCollector(prometheus.ProcessCollectorOpts{}),
		prometheus.NewGoCollector(),
		exporter,
	)

	http.Handle("/metrics", promhttp.HandlerFor(reg, promhttp.HandlerOpts{}))
	log.Fatal(http.ListenAndServe(*serverAddr, nil))
}
