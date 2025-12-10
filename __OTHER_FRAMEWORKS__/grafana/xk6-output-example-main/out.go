// Package example contains the xk6-output-example extension.
package example

import (
	"encoding/csv"
	"fmt"
	"time"

	"go.k6.io/k6/metrics"
	"go.k6.io/k6/output"
)

const defaultInterval = 10 * time.Second

var fields = []string{"time", "metric", "avg", "min", "med", "max", "p(90)", "p(95)"} //nolint:gochecknoglobals

type out struct {
	buffer  *output.SampleBuffer
	flusher *output.PeriodicFlusher

	writer *csv.Writer
	closer func() error

	params output.Params

	filename string
	interval time.Duration
}

var _ output.WithStopWithTestError = new(out)

func newOutput(params output.Params) (output.Output, error) {
	o := new(out)

	o.params = params
	o.filename = params.ConfigArgument

	if v, has := params.Environment["XK6_EXAMPLE_INTERVAL"]; has && len(v) > 0 {
		var err error

		o.interval, err = time.ParseDuration(v)
		if err != nil {
			return nil, err
		}
	} else {
		o.interval = defaultInterval
	}

	return o, nil
}

// Description returns a human-readable description of the output that will be shown in `k6 run`.
func (o *out) Description() string {
	return fmt.Sprintf("%s file=%s interval=%s", o.params.OutputType, o.filename, o.interval.String())
}

// Start is called before the Engine tries to use the output and should be
// used for any long initialization tasks.
func (o *out) Start() error {
	if len(o.filename) != 0 && o.filename != "-" {
		file, err := o.params.FS.Create(o.filename)
		if err != nil {
			return err
		}

		o.writer = csv.NewWriter(file)
		o.closer = func() error { return file.Close() }
	} else {
		o.writer = csv.NewWriter(o.params.StdOut)
		o.closer = func() error { return nil }
	}

	if err := o.writer.Write(fields); err != nil {
		return err
	}

	o.buffer = new(output.SampleBuffer)

	var err error

	o.flusher, err = output.NewPeriodicFlusher(o.interval, o.flushSamples)

	return err
}

// AddMetricSamples receive the latest metric samples from the Engine.
func (o *out) AddMetricSamples(samples []metrics.SampleContainer) {
	o.buffer.AddMetricSamples(samples)
}

// StopWithTestError flush all remaining metrics and finalize the test run.
func (o *out) StopWithTestError(error) error {
	o.flusher.Stop()

	return o.closer()
}

// Stop to satisfy old deprecated output.Output interface.
func (o *out) Stop() error {
	return o.StopWithTestError(nil)
}

func (o *out) flushSamples() {
	now := time.Now()

	reg := o.makeAggregates()

	if err := o.writeAggregates(now, reg); err != nil {
		o.params.Logger.WithError(err).Error("write failed")
	}
}

func (o *out) makeAggregates() *metrics.Registry {
	reg := metrics.NewRegistry()

	for _, sc := range o.buffer.GetBufferedSamples() {
		for _, sample := range sc.GetSamples() {
			if sample.Metric.Type != metrics.Trend {
				continue
			}

			metric := reg.Get(sample.Metric.Name)
			if metric == nil {
				metric = reg.MustNewMetric(sample.Metric.Name, sample.Metric.Type, sample.Metric.Contains)
			}

			metric.Sink.Add(sample)
		}
	}

	return reg
}

func (o *out) writeAggregates(now time.Time, reg *metrics.Registry) error {
	for _, metric := range reg.All() {
		sink, _ := metric.Sink.(*metrics.TrendSink)
		s := fmt.Sprint

		record := make([]string, 0, len(fields))

		record = append(record, s(now.Unix()), metric.Name)

		data := sink.Format(o.interval)

		for _, name := range fields[len(record):] {
			record = append(record, s(data[name]))
		}

		if err := o.writer.Write(record); err != nil {
			return err
		}
	}

	o.writer.Flush()

	return nil
}
