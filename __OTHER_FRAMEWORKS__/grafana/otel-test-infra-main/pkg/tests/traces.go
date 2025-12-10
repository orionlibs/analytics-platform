package tests

import (
	"encoding/json"
	"net/http"
	"strconv"
	"testing"
	"time"

	"github.com/grafana/otel-test-infra/pkg/infra/tempo"
	"github.com/mariomac/guara/pkg/test"
	"github.com/stretchr/testify/require"
)

func EnsureReadyWithTempo(t *testing.T, url, subpath, tempoURL string) {
	test.Eventually(t, time.Minute, func(t require.TestingT) {
		// first, verify that the test service endpoint is healthy
		req, err := http.NewRequest("GET", url+subpath, nil)
		require.NoError(t, err)
		r, err := testHTTPClient.Do(req)
		require.NoError(t, err)
		require.Equal(t, http.StatusOK, r.StatusCode)

		// now, verify that we see traces in Tempo
		// we don't really care that this metric could be from a previous
		// test. Once one it is visible, it means that the Agent and Tempo are healthy and running
		resp, err := http.Get(tempoURL + "/api/search?tags=http.method%3DGET")
		require.NoError(t, err)
		require.Equal(t, http.StatusOK, resp.StatusCode)

		var sr tempo.SearchTagsResult
		require.NoError(t, json.NewDecoder(resp.Body).Decode(&sr))
		require.GreaterOrEqual(t, len(sr.Traces), 1)
	}, test.Interval(time.Second))
}

func MatchTraceAttribute(t *testing.T, attributes []tempo.Attribute, atype, key, value string) {
	require.NotNil(t, attributes)
	found := false
	for _, attr := range attributes {
		if attr.Key == key {
			found = true
			v := attr.Value
			require.NotNil(t, v)
			av, ok := v[atype+"Value"]
			require.True(t, ok)
			if value != "" {
				require.Equal(t, av, value)
			}
		}
	}

	if !found {
		t.Errorf("couldn't find attribute %s", key)
	}
}

type AttributeMatch struct {
	Key   string
	Value string
	Type  string
}

func AttributesMatch(t *testing.T, attributes []tempo.Attribute, match []AttributeMatch) {
	for _, m := range match {
		MatchTraceAttribute(t, attributes, m.Type, m.Key, m.Value)
	}
}

func AttributesExist(t *testing.T, attributes []tempo.Attribute, match []AttributeMatch) {
	for _, m := range match {
		MatchTraceAttribute(t, attributes, m.Type, m.Key, "")
	}
}

func TimeIsIncreasing(t *testing.T, span tempo.Span) {
	require.NotNil(t, span)
	require.NotEmpty(t, span.StartTimeUnixNano)
	require.NotEmpty(t, span.EndTimeUnixNano)

	start, err := strconv.ParseInt(span.StartTimeUnixNano, 10, 64)
	require.NoError(t, err)
	end, err := strconv.ParseInt(span.EndTimeUnixNano, 10, 64)
	require.NoError(t, err)

	require.Greater(t, end, start)
}
