package tests

import (
	"bytes"
	"crypto/tls"
	"net/http"
	"testing"
	"time"

	"github.com/mariomac/guara/pkg/test"
	"github.com/stretchr/testify/require"

	"github.com/grafana/otel-test-infra/pkg/infra/prom"
)

var tr = &http.Transport{
	TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
}
var testHTTPClient = &http.Client{Transport: tr}

func DisableKeepAlives(disableKeepAlives bool) {
	testHTTPClient.Transport.(*http.Transport).DisableKeepAlives = disableKeepAlives
}

func DoHTTPPost(t *testing.T, path string, status int, jsonBody []byte) {
	req, err := http.NewRequest(http.MethodPost, path, bytes.NewReader(jsonBody))
	require.NoError(t, err)
	req.Header.Set("Content-Type", "application/json")

	r, err := testHTTPClient.Do(req)
	require.NoError(t, err)
	require.Equal(t, status, r.StatusCode)
	time.Sleep(300 * time.Millisecond)
}

func DoHTTPGet(t *testing.T, path string, status int, jsonBody []byte) {
	req, err := http.NewRequest(http.MethodGet, path, bytes.NewReader(jsonBody))
	require.NoError(t, err)
	req.Header.Set("Content-Type", "application/json")

	r, err := testHTTPClient.Do(req)
	require.NoError(t, err)
	require.Equal(t, status, r.StatusCode)
	time.Sleep(300 * time.Millisecond)
}

// does a smoke test to verify that all the components that started
// asynchronously are up and communicating properly
func EnsureReadyWithPrometheus(t *testing.T, url, subpath, promHostPort string) {
	pq := prom.Client{HostPort: promHostPort}
	test.Eventually(t, time.Minute, func(t require.TestingT) {
		// first, verify that the test service endpoint is healthy
		req, err := http.NewRequest("GET", url+subpath, nil)
		require.NoError(t, err)
		r, err := testHTTPClient.Do(req)
		require.NoError(t, err)
		require.Equal(t, http.StatusOK, r.StatusCode)

		// now, verify that the metric has been reported.
		// we don't really care that this metric could be from a previous
		// test. Once one it is visible, it means that Otel and Prometheus are healthy
		results, err := pq.Query(`http_server_duration_seconds_count{http_target="` + subpath + `"}`)
		require.NoError(t, err)
		require.NotZero(t, len(results))
	}, test.Interval(time.Second))
}
