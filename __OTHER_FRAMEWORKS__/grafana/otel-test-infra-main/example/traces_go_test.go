package inttests

import (
	"encoding/json"
	"net/http"
	"path"
	"testing"
	"time"

	"github.com/grafana/otel-test-infra/pkg/infra/docker"
	"github.com/grafana/otel-test-infra/pkg/infra/tempo"
	"github.com/grafana/otel-test-infra/pkg/tests"
	"github.com/mariomac/guara/pkg/test"
	"github.com/stretchr/testify/require"
)

const (
	tempoQueryURL    = "http://localhost:3200"
	traceTestTimeout = 20 * time.Second
)

func TestSuite_Traces(t *testing.T) {
	compose, err := docker.ComposeSuite("docker-compose-traces.yml", path.Join(pathOutput, "test-suite-traces.log"))
	require.NoError(t, err)
	require.NoError(t, compose.Up())
	t.Run("Go traces", testGoTraces)
	require.NoError(t, compose.Close())
}

func testGoTraces(t *testing.T) {
	for _, testCaseURL := range []string{
		"http://localhost:8080",
	} {
		t.Run(testCaseURL, func(t *testing.T) {
			tests.EnsureReadyWithTempo(t, testCaseURL, "/smoke", tempoQueryURL)
			testTracesGoHTTP(t, testCaseURL)
		})
	}
}

func testTracesGoHTTP(t *testing.T, url string) {
	tests.DoHTTPGet(t, url+"/create-trace?delay=30&response=200", 200, nil)

	var tr tempo.Trace
	test.Eventually(t, traceTestTimeout, func(t require.TestingT) {
		resp, err := http.Get(tempoQueryURL + "/api/search?tags=http.target%3D%2Fcreate-trace")
		require.NoError(t, err)
		require.Equal(t, http.StatusOK, resp.StatusCode)

		var sr tempo.SearchTagsResult
		require.NoError(t, json.NewDecoder(resp.Body).Decode(&sr))
		require.GreaterOrEqual(t, len(sr.Traces), 1)
		tr = sr.Traces[0]
	}, test.Interval(time.Second))

	require.NotNil(t, tr)
	resp, err := http.Get(tempoQueryURL + "/api/traces/" + tr.TraceID)
	require.NoError(t, err)
	require.Equal(t, http.StatusOK, resp.StatusCode)

	var td tempo.TraceDetails
	require.NoError(t, json.NewDecoder(resp.Body).Decode(&td))
	require.Len(t, td.Batches, 1)

	batch := td.Batches[0]
	require.NotNil(t, batch.Resource)
	tests.AttributesMatch(
		t,
		batch.Resource.Attributes,
		[]tests.AttributeMatch{
			{Type: "string", Key: "service.namespace", Value: "integration-test"},
			{Type: "string", Key: "service.name", Value: "testserver"},
			{Type: "string", Key: "telemetry.sdk.language", Value: "go"},
		},
	)

	parents := batch.FindSpansByName("GET /create-trace")
	require.NotNil(t, parents)
	require.Len(t, parents, 1)
	parent := parents[0]
	require.Equal(t, "SPAN_KIND_SERVER", parent.Kind)
	tests.TimeIsIncreasing(t, parent)

	tests.AttributesMatch(
		t,
		parent.Attributes,
		[]tests.AttributeMatch{
			{Type: "string", Key: "http.target", Value: "/create-trace"},
			{Type: "string", Key: "http.route", Value: "/create-trace"},
			{Type: "string", Key: "http.method", Value: "GET"},
			{Type: "int", Key: "net.host.port", Value: "8080"},
			{Type: "int", Key: "http.status_code", Value: "200"},
			{Type: "int", Key: "http.request_content_length", Value: "0"},
		},
	)

	tests.AttributesExist(
		t,
		parent.Attributes,
		[]tests.AttributeMatch{
			{Type: "string", Key: "net.host.name"},
			{Type: "string", Key: "net.sock.peer.addr"},
		},
	)

	children := batch.ChildrenOf(parent.SpanId)
	require.NotNil(t, children)
	require.GreaterOrEqual(t, 2, len(children))

	inqueue := false
	processing := false
	for _, c := range children {
		require.Equal(t, "SPAN_KIND_INTERNAL", c.Kind)
		require.Equal(t, parent.SpanId, c.ParentSpanId)
		tests.TimeIsIncreasing(t, c)
		require.NotEqual(t, c.ParentSpanId, c.SpanId)
		require.Equal(t, parent.TraceId, c.TraceId)
		require.Nil(t, c.Attributes)

		if c.Name == "in queue" {
			inqueue = true
		}

		if c.Name == "processing" {
			processing = true
		}
	}

	require.True(t, inqueue)
	require.True(t, processing)
}
