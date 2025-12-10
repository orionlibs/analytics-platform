package inttests

import (
	"net"
	"path"
	"testing"
	"time"

	"github.com/mariomac/guara/pkg/test"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/grafana/otel-test-infra/pkg/infra/docker"
	"github.com/grafana/otel-test-infra/pkg/infra/prom"
	"github.com/grafana/otel-test-infra/pkg/tests"
)

const (
	prometheusHostPort = "localhost:9090"

	testTimeout = 20 * time.Second
)

var (
	pathRoot   = path.Join(".")
	pathOutput = path.Join(pathRoot, "testoutput")
)

func TestSuite_Java(t *testing.T) {
	compose, err := docker.ComposeSuite("docker-compose-java.yml", path.Join(pathOutput, "test-suite-java.log"))
	require.NoError(t, err)
	compose.Env = append(compose.Env, `JAVA_OPEN_PORT=8085`, `JAVA_EXECUTABLE_NAME=""`, `JAVA_TEST_MODE=-jar`, `OTEL_SERVICE_NAME=greeting`)
	require.NoError(t, err)
	require.NoError(t, compose.Up())
	t.Run("Java RED metrics", testREDMetricsJavaHTTP)
	require.NoError(t, compose.Close())
}

// does a smoke test to verify that all the components that started
// asynchronously for the Java test are up and communicating properly
func waitForJavaTestComponents(t *testing.T, url string) {
	tests.EnsureReadyWithPrometheus(t, url, "/greeting", prometheusHostPort)
}

func testREDMetricsForJavaHTTPLibrary(t *testing.T, url string, comm string) {
	path := "/greeting"

	// Call the instrumented service 4 times asking to respond with HTTP code 204
	for i := 0; i < 4; i++ {
		tests.DoHTTPGet(t, url+path+"?delay=30&response=204", 204, nil)
	}

	// Eventually, Prometheus would make this query visible
	pq := prom.Client{HostPort: prometheusHostPort}
	var results []prom.Result
	test.Eventually(t, testTimeout, func(t require.TestingT) {
		var err error
		results, err = pq.Query(`http_server_duration_seconds_count{` +
			`http_method="GET",` +
			`http_status_code="204",` +
			`service_namespace="integration-test",` +
			`service_name="` + comm + `",` +
			`http_target="` + path + `"}`)
		require.NoError(t, err)
		// check duration_count has 3 calls and all the arguments
		require.Len(t, results, 1)
		if len(results) > 0 {
			res := results[0]
			require.Len(t, res.Value, 2)
			assert.LessOrEqual(t, "3", res.Value[1])
			addr := net.ParseIP(res.Metric["net_sock_peer_addr"])
			assert.NotNil(t, addr)
		}
	})
}

func testREDMetricsJavaHTTP(t *testing.T) {
	for _, testCaseURL := range []string{
		"http://localhost:8086",
	} {
		t.Run(testCaseURL, func(t *testing.T) {
			waitForJavaTestComponents(t, testCaseURL)
			testREDMetricsForJavaHTTPLibrary(t, testCaseURL, "greeting")
		})
	}
}
