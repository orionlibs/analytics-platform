package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
	"net/http/httputil"
	"strings"

	"github.com/guillaumeblaquiere/jsonFilter"
	"github.com/prometheus/common/log"
)

type client struct {
	httpClient    *http.Client
	token         string
	baseLegacyUrl string
	baseURL       string
	apiVersion    string
}

func (c *client) getOrganizations() (orgsResponse, error) {
	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("%s/orgs", c.baseLegacyUrl), nil)
	if err != nil {
		return orgsResponse{}, err
	}
	response, err := c.do(req)
	if err != nil {
		return orgsResponse{}, err
	}
	var orgs orgsResponse
	err = json.NewDecoder(response.Body).Decode(&orgs)
	if err != nil {
		return orgsResponse{}, err
	}
	return orgs, nil
}

func (c *client) getProjects(organizationID string, target string, origins []string, projectFilter string) (projectsResponse, error) {
	var reader bytes.Buffer

	req, err := http.NewRequest(http.MethodGet, fmt.Sprintf("%s/orgs/%s/projects", c.baseURL, organizationID), &reader)
	if err != nil {
		return projectsResponse{}, err
	}

	q := req.URL.Query()
	q.Add("version", c.apiVersion)
	q.Add("limit", "50")
	if len(target) != 0 {
		q.Add("names", target)
	}
	if len(origins) != 0 {
		q.Add("origins", strings.Join(origins, ","))
	}
	req.URL.RawQuery = q.Encode()

	log.Debugf("Fetching Projects...")
	response, err := c.do(req)
	if err != nil {
		return projectsResponse{}, err
	}

	var allProjects projectsResponse
	err = json.NewDecoder(response.Body).Decode(&allProjects)
	if err != nil {
		return projectsResponse{}, err
	}

	filter := jsonFilter.Filter{}
	if projectFilter != "" {
		err = filter.Init(projectFilter, project{})
		if err != nil {
			return projectsResponse{}, err
		}
	}

	for {
		if len(allProjects.Links.Next) == 0 {
			break
		}

		var paginatedReader bytes.Buffer
		req, err := http.NewRequest(http.MethodGet, c.baseURL+allProjects.Links.Next, &paginatedReader)
		if err != nil {
			return projectsResponse{}, err
		}

		log.Debugf("Fetching Projects... (cursor: %s)", req.URL.Query().Get("starting_after"))

		response, err := c.do(req)
		if err != nil {
			return projectsResponse{}, err
		}

		var projects projectsResponse
		err = json.NewDecoder(response.Body).Decode(&projects)
		if err != nil {
			return projectsResponse{}, err
		}

		if projectFilter != "" {
			ret, err := filter.ApplyFilter(projects.Data)
			if err != nil {
				return projectsResponse{}, err
			}
			projects.Data = ret.([]project)
		}

		allProjects.Data = append(allProjects.Data, projects.Data...)
		allProjects.Links = projects.Links
	}

	log.Debugf("Found %d Projects.", len(allProjects.Data))
	return allProjects, nil
}

func (c *client) getIssues(organizationID string, projectID string) (issuesResponse, error) {
	postData := issuesPostData{
		Filters: issueFilters{
			Severities: []string{
				"critical", "high", "medium", "low",
			},
		},
	}
	var reader bytes.Buffer
	err := json.NewEncoder(&reader).Encode(&postData)
	if err != nil {
		return issuesResponse{}, err
	}
	req, err := http.NewRequest(http.MethodPost, fmt.Sprintf("%s/org/%s/project/%s/aggregated-issues", c.baseLegacyUrl, organizationID, projectID), &reader)
	if err != nil {
		return issuesResponse{}, err
	}
	response, err := c.do(req)
	if err != nil {
		return issuesResponse{}, err
	}
	var issues issuesResponse
	err = json.NewDecoder(response.Body).Decode(&issues)
	if err != nil {
		return issuesResponse{}, err
	}
	return issues, nil
}

func (c *client) do(req *http.Request) (*http.Response, error) {
	req.Header.Add("Authorization", fmt.Sprintf("token %s", c.token))
	req.Header.Add("Content-Type", "application/vnd.api+json")
	response, err := c.httpClient.Do(req)
	if err != nil {
		return nil, err
	}
	if response.StatusCode != http.StatusOK {
		body, err := ioutil.ReadAll(response.Body)
		if err != nil {
			log.Errorf("read body failed: %v", err)
			body = []byte("failed to read body")
		}
		requestDump, err := httputil.DumpRequestOut(req, true)
		if err != nil {
			log.Debugf("Failed to dump request for logging")
		} else {
			log.Debugf("Failed request dump: %s", requestDump)
		}
		return nil, fmt.Errorf("request not OK: %s: body: %s", response.Status, body)
	}
	return response, nil
}

type orgsResponse struct {
	Orgs []org `json:"orgs,omitempty"`
}

type org struct {
	ID    string `json:"id,omitempty"`
	Name  string `json:"name,omitempty"`
	Group *struct {
		Name string `json:"name,omitempty"`
		ID   string `json:"id,omitempty"`
	} `json:"group,omitempty"`
}

type projectsResponse struct {
	JsonApi jsonApi      `json:"jsonapi,omitempty"`
	Data    []project    `json:"data,omitempty"`
	Links   projectLinks `json:"links,omitEmpty"`
}

type jsonApi struct {
	Version string `json:"version,omitempty"`
}

type project struct {
	Type          string               `json:"type,omitempty"`
	ID            string               `json:"id,omitempty"`
	Meta          projectMeta          `json:"meta,omitempty"`
	Attributes    projectAttributes    `json:"attributes,omitempty"`
	Relationships projectRelationships `json:"relationships,omitempty"`
}

type projectMeta struct {
	MonitoredAt string `json:"cli_monitored_at,omitempty"`
}

type projectAttributes struct {
	Name                string          `json:"name,omitempty"`
	Type                string          `json:"type,omitempty"`
	TargetFile          string          `json:"target_file,omitempty"`
	TargetReference     string          `json:"target_reference,omitempty"`
	Origin              string          `json:"origin,omitempty"`
	Created             string          `json:"created,omitempty"`
	Status              string          `json:"status,omitempty"`
	BusinessCriticality []string        `json:"business_criticality,omitempty"`
	Environment         []string        `json:"environment,omitempty"`
	Lifecycle           []string        `json:"lifecycle,omitempty"`
	Tags                []projectTag    `json:"tags,omitempty"`
	Settings            projectSettings `json:"settings,omitempty"`
	ImageCluster        string          `json:"imageCluster,omitempty"`
}

type projectTag struct {
	Key   string `json:"key,omitempty"`
	Value string `json:"value,omitempty"`
}

type projectSettings struct {
	RecurringTests projectSettingsRecurringTests `json:"recurring_tests,omitempty"`
	PullRequests   projectSettingsPullRequests   `json:"pull_requests,omitempty"`
}

type projectSettingsRecurringTests struct {
	Frequency string `json:"frequency,omitempty"`
}

type projectSettingsPullRequests struct {
	FailOnlyForIssuesWithFix bool `json:"fail_only_for_issues_with_fix,omitempty"`
}

type projectRelationships struct {
	Organization projectRelationship `json:"organization,omitempty"`
	Target       projectRelationship `json:"target,omitempty"`
	Importer     projectRelationship `json:"importer,omitempty"`
}

type projectRelationship struct {
	Data  projectRelationshipData  `json:"data,omitempty"`
	Links projectRelationshipLinks `json:"links,omitempty"`
}

type projectRelationshipData struct {
	Type string `json:"type,omitempty"`
	ID   string `json:"id,omitempty"`
}

type projectRelationshipLinks struct {
	Related string `json:"related,omitempty"`
}

type projectLinks struct {
	Next string `json:"next,omitempty"`
	Prev string `json:"prev,omitempty"`
}

type issuesResponse struct {
	Issues []issue `json:"issues,omitempty"`
}

type issue struct {
	ID        string    `json:"id,omitempty"`
	IssueType string    `json:"issueType"`
	IssueData issueData `json:"issueData,omitempty"`
	Ignored   bool      `json:"isIgnored"`
	FixInfo   fixInfo   `json:"fixInfo,omitempty"`
	Links     Links     `json:"links"`
}

type issueData struct {
	ID          string      `json:"id,omitempty"`
	Title       string      `json:"title,omitempty"`
	Severity    string      `json:"severity,omitempty"`
	Identifiers Identifiers `json:"identifiers,omitempty"`
}

type Links struct {
	Paths string `json:"paths"`
}

type Identifiers struct {
	CVE []string `json:"CVE"`
}

type fixInfo struct {
	Upgradeable bool `json:"isUpgradable"`
	Patchable   bool `json:"isPatchable"`
}

type license struct{}

type issuesPostData struct {
	Filters issueFilters `json:"filters,omitempty"`
}
type issueFilters struct {
	Severities []string `json:"severities,omitempty"`
	Types      []string `json:"types,omitempty"`
	Ignored    bool     `json:"ignored,omitempty"`
	Patched    bool     `json:"patched,omitempty"`
}

type projectPostData struct {
	Filters projectFilters `json:"filters,omitempty"`
}
type projectFilters struct {
	Name string `json:"name,omitempty"`
}
