package example //nolint:testpackage

import (
	"io"
	"strings"
	"testing"
	"time"

	"github.com/stretchr/testify/require"
	"go.k6.io/k6/lib/fsext"
	"go.k6.io/k6/metrics"
	"go.k6.io/k6/output"
)

func newTestOutput(t *testing.T, filename string, interval string) (*out, error) {
	t.Helper()

	params := output.Params{
		OutputType:  "example",
		Environment: map[string]string{},
		FS:          fsext.NewMemMapFs(),
	}

	if len(filename) > 0 {
		params.ConfigArgument = filename
	}

	if len(interval) > 0 {
		params.Environment["XK6_EXAMPLE_INTERVAL"] = interval
	}

	instance, err := newOutput(params)
	if err != nil {
		return nil, err
	}

	o, _ := instance.(*out)

	return o, nil
}

func Test_newOutput(t *testing.T) {
	t.Parallel()

	const filename = "test.csv"

	o, err := newTestOutput(t, filename, "")

	require.NoError(t, err)
	require.Equal(t, defaultInterval, o.interval)

	o, err = newTestOutput(t, filename, "100ms")

	require.NoError(t, err)
	require.Equal(t, 100*time.Millisecond, o.interval)

	_, err = newTestOutput(t, filename, "invalid")

	require.Error(t, err)
}

func Test_out_Description(t *testing.T) {
	t.Parallel()

	o, err := newTestOutput(t, "test.csv", "100ms")

	require.NoError(t, err)

	require.Equal(t, "example file=test.csv interval=100ms", o.Description())
}

func newTestSamples(t *testing.T, values ...float64) []metrics.SampleContainer {
	t.Helper()

	samples := make([]metrics.SampleContainer, 0, len(values))

	now := time.Now()

	for _, value := range values {
		samples = append(samples, metrics.Sample{
			TimeSeries: metrics.TimeSeries{
				Metric: &metrics.Metric{
					Name:     "test_trend",
					Type:     metrics.Trend,
					Contains: metrics.Data,
				},
			},
			Time:  now,
			Value: value,
		})

		samples = append(samples, metrics.Sample{
			TimeSeries: metrics.TimeSeries{
				Metric: &metrics.Metric{
					Name:     "test_counter",
					Type:     metrics.Counter,
					Contains: metrics.Data,
				},
			},
			Time:  now,
			Value: value,
		})
	}

	return samples
}

func Test_out_file(t *testing.T) {
	t.Parallel()

	o, err := newTestOutput(t, "test.csv", "100ms")

	require.NoError(t, err)
	require.NoError(t, o.Start())

	o.AddMetricSamples(newTestSamples(t, 1, 2, 2, 1))

	require.NoError(t, o.Stop())

	file, err := o.params.FS.Open("test.csv")

	require.NoError(t, err)

	data, err := io.ReadAll(file)

	require.NoError(t, err)
	require.NoError(t, file.Close())

	lines := strings.Split(string(data), "\n")

	require.Equal(t, "time,metric,avg,min,med,max,p(90),p(95)", lines[0])
	require.Regexp(t, `\d+,test_trend,1.5,1,1.5,2,2,2`, lines[1])
}

func Test_out_stdout(t *testing.T) {
	t.Parallel()

	o, err := newTestOutput(t, "", "100ms")

	require.NoError(t, err)

	stdout, err := o.params.FS.Create("stdout")

	require.NoError(t, err)

	o.params.StdOut = stdout

	require.NoError(t, o.Start())

	o.AddMetricSamples(newTestSamples(t, 1, 2, 2, 1))

	require.NoError(t, o.Stop())
	require.NoError(t, stdout.Close())

	file, err := o.params.FS.Open("stdout")

	require.NoError(t, err)

	data, err := io.ReadAll(file)

	require.NoError(t, err)
	require.NoError(t, file.Close())

	lines := strings.Split(string(data), "\n")

	require.Equal(t, "time,metric,avg,min,med,max,p(90),p(95)", lines[0])
	require.Regexp(t, `\d+,test_trend,1.5,1,1.5,2,2,2`, lines[1])
}
