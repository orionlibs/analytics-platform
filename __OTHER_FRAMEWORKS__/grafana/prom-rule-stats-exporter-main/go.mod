module github.com/gouthamve/prom-rule-stats-exporter

go 1.16

require (
	github.com/alecthomas/template v0.0.0-20190718012654-fb15b899a751 // indirect
	github.com/alecthomas/units v0.0.0-20210208195552-ff826a37aa15 // indirect
	github.com/go-kit/kit v0.10.0
	github.com/prometheus/client_golang v1.7.1
	github.com/prometheus/common v0.18.0
	github.com/stretchr/testify v1.7.0 // indirect
	gopkg.in/alecthomas/kingpin.v2 v2.2.6
	gopkg.in/yaml.v2 v2.4.0 // indirect
)

// Temporary replace until https://github.com/prometheus/client_golang/pull/855 is merged.
replace github.com/prometheus/client_golang => github.com/gouthamve/client_golang v1.10.1-0.20210411101726-629f64ab3f57
