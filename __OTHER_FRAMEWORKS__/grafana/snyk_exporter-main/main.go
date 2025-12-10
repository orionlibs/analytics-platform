package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"strconv"
	"strings"
	"sync"
	"syscall"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/prometheus/common/log"
	kingpin "gopkg.in/alecthomas/kingpin.v2"
)

const (
	issueIdLabel      = "id"
	projectLabel      = "project"
	issueTypeLabel    = "issue_type"
	issueTitleLabel   = "issue_title"
	severityLabel     = "severity"
	organizationLabel = "organization"
	ignoredLabel      = "ignored"
	upgradeableLabel  = "upgradeable"
	patchableLabel    = "patchable"
	monitoredLabel    = "monitored"
	targetLabel       = "target"
	projectTypeLabel  = "project_type"
	cveLabel          = "cve"
)

var (
	vulnerabilityGauge = prometheus.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: "snyk_vulnerabilities_total",
			Help: "Gauge of Snyk vulnerabilities",
		},
		[]string{organizationLabel, targetLabel, projectLabel, projectTypeLabel, issueIdLabel, issueTypeLabel, issueTitleLabel, severityLabel, ignoredLabel, upgradeableLabel, patchableLabel, monitoredLabel, cveLabel},
	)
)

var (
	ready       = false
	readyMutex  = &sync.RWMutex{}
	scrapeMutex = &sync.RWMutex{}
)

var (
	version = ""
)

func main() {
	flags := kingpin.New("snyk_exporter", "Snyk exporter for Prometheus. Provide your Snyk API token and the organization(s) to scrape to expose Prometheus metrics.")
	snykAPIURL := flags.Flag("snyk.api-url", "Snyk API URL (legacy)").Default("https://snyk.io/api/v1").String()
	snykRESTAPIURL := flags.Flag("snyk.rest-api-url", "Snyk REST API URL").Default("https://api.snyk.io/rest").String()
	snykRESTAPIVersion := flags.Flag("snyk.rest-api-version", "Snyk REST API Version").Default("2023-06-22").String()
	snykAPIToken := flags.Flag("snyk.api-token", "Snyk API token").Required().OverrideDefaultFromEnvar("SNYK_API_TOKEN").String()
	snykInterval := flags.Flag("snyk.interval", "Polling interval for requesting data from Snyk API in seconds").Short('i').Default("600").Int()
	snykOrganizations := flags.Flag("snyk.organization", "Snyk organization ID to scrape projects from (can be repeated for multiple organizations)").Strings()
	snykTargets := flags.Flag("snyk.target", "Snyk target/repo name to scrape projects from (can be repeated for multiple targets)").Strings()
	snykOrigins := flags.Flag("snyk.origin", "Snyk project origin (can be repeated for multiple origins)").Strings()
	snykProjectFilter := flags.Flag("snyk.project-filter", "Project filter (e.g. attributes.imageCluster=mycluster).").String()
	requestTimeout := flags.Flag("snyk.timeout", "Timeout for requests against Snyk API").Default("10").Int()
	listenAddress := flags.Flag("web.listen-address", "Address on which to expose metrics.").Default(":9532").String()
	log.AddFlags(flags)
	flags.HelpFlag.Short('h')
	flags.Version(version)
	kingpin.MustParse(flags.Parse(os.Args[1:]))

	if len(*snykOrganizations) != 0 {
		log.Infof("Starting Snyk exporter for organization '%s'", strings.Join(*snykOrganizations, ","))
	} else {
		log.Info("Starting Snyk exporter for all organization for token")
	}

	if len(*snykTargets) != 0 {
		log.Infof("Starting Snyk exporter for targets '%s'", strings.Join(*snykTargets, ","))
	} else {
		log.Info("Starting Snyk exporter for all targets")
	}

	if len(*snykOrigins) != 0 {
		log.Infof("Starting Snyk exporter for origins '%s'", strings.Join(*snykOrigins, ","))
	} else {
		log.Info("Starting Snyk exporter for all origins")
	}

	prometheus.MustRegister(vulnerabilityGauge)
	http.Handle("/metrics", promhttp.InstrumentMetricHandler(
		prometheus.DefaultRegisterer, http.HandlerFunc(func(rw http.ResponseWriter, r *http.Request) {
			scrapeMutex.RLock()
			defer scrapeMutex.RUnlock()
			promhttp.HandlerFor(prometheus.DefaultGatherer, promhttp.HandlerOpts{}).ServeHTTP(rw, r)
		}),
	))

	http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintf(w, "healthy")
	})

	http.HandleFunc("/ready", func(w http.ResponseWriter, r *http.Request) {
		readyMutex.RLock()
		defer readyMutex.RUnlock()

		if ready {
			w.WriteHeader(http.StatusOK)
		} else {
			w.WriteHeader(http.StatusServiceUnavailable)
		}

		_, err := w.Write([]byte(strconv.FormatBool(ready)))
		if err != nil {
			log.With("error", err).Errorf("Failed to write ready response: %v", err)
		}
	})

	// context used to stop worker components from signal or component failures
	ctx, stop := context.WithCancel(context.Background())
	defer stop()

	// used to report errors from components
	var exitCode int
	componentFailed := make(chan error, 1)
	var wg sync.WaitGroup

	go func() {
		log.Infof("Listening on %s", *listenAddress)
		err := http.ListenAndServe(*listenAddress, nil)
		if err != nil {
			componentFailed <- fmt.Errorf("http listener stopped: %v", err)
		}
	}()

	// Go routine responsible for starting shutdown sequence based of signals or
	// component failures
	sigs := make(chan os.Signal, 1)
	signal.Notify(sigs, syscall.SIGINT, syscall.SIGTERM)
	wg.Add(1)
	go func() {
		defer wg.Done()
		select {
		case sig := <-sigs:
			log.Infof("Received os signal '%s'. Terminating...", sig)
		case err := <-componentFailed:
			if err != nil {
				log.Errorf("Component failed: %v", err)
				exitCode = 1
			}
		}
		stop()
	}()

	wg.Add(1)
	go func() {
		defer wg.Done()
		log.Info("Snyk API scraper starting")
		defer log.Info("Snyk API scraper stopped")
		err := runAPIPolling(ctx, *snykAPIURL, *snykRESTAPIURL, *snykRESTAPIVersion, *snykAPIToken, *snykOrganizations, *snykTargets, *snykOrigins, *snykProjectFilter, secondDuration(*snykInterval), secondDuration(*requestTimeout))
		if err != nil {
			componentFailed <- fmt.Errorf("snyk api scraper: %w", err)
		}
	}()

	// wait for all components to stop
	wg.Wait()
	if exitCode != 0 {
		log.Errorf("Snyk exporter exited with exit %d", exitCode)
		os.Exit(exitCode)
	} else {
		log.Infof("Snyk exporter exited with exit 0")
	}
}

func secondDuration(seconds int) time.Duration {
	return time.Duration(seconds) * time.Second
}

func runAPIPolling(ctx context.Context, url string, restUrl string, apiVersion string, token string, organizationIDs []string, targets []string, origins []string, projectFilter string, requestInterval, requestTimeout time.Duration) error {
	client := client{
		httpClient: &http.Client{
			Timeout: requestTimeout,
		},
		token:         token,
		baseLegacyUrl: url,
		baseURL:       restUrl,
		apiVersion:    apiVersion,
	}
	organizations, err := getOrganizations(&client, organizationIDs)
	if err != nil {
		return err
	}
	log.Infof("Running Snyk API scraper for organizations: %v", strings.Join(organizationNames(organizations), ", "))

	// kick off a poll right away to get metrics available right after startup
	pollOrgsAndTargets(organizations, targets, origins, projectFilter, ctx, client)

	ticker := time.NewTicker(requestInterval)
	defer ticker.Stop()
	for {
		select {
		case <-ctx.Done():
			return nil
		case <-ticker.C:
			pollOrgsAndTargets(organizations, targets, origins, projectFilter, ctx, client)
		}
	}
}

// loop through provided orgs and targets
func pollOrgsAndTargets(organizations []org, targets []string, origins []string, projectFilter string, ctx context.Context, client client) {
	var gaugeResults []gaugeResult
	for _, organization := range organizations {
		log.Infof("Collecting for organization '%s'", organization.Name)
		if len(targets) == 0 {
			gaugeResults = pollAPI(ctx, &client, organization, "", origins, projectFilter, gaugeResults)
		} else {
			for _, target := range targets {
				log.Infof("Collecting for target starting with '%s'", target)
				gaugeResults = pollAPI(ctx, &client, organization, target, origins, projectFilter, gaugeResults)
			}
		}
	}
	registerMetrics(gaugeResults)
}

func registerMetrics(gaugeResults []gaugeResult) {
	log.Infof("Exposing %d results as metrics", len(gaugeResults))
	scrapeMutex.Lock()
	register(gaugeResults)
	scrapeMutex.Unlock()
	readyMutex.Lock()
	ready = true
	readyMutex.Unlock()
}

// pollAPI collects data from provided organizations and registers them in the
// prometheus registry.
func pollAPI(ctx context.Context, client *client, organization org, target string, origins []string, projectFilter string, gaugeResults []gaugeResult) []gaugeResult {
	//var gaugeResults []gaugeResult
	results, err := collect(ctx, client, organization, target, origins, projectFilter)
	if err != nil {
		log.With("error", err).
			With("organzationName", organization.Name).
			With("organzationId", organization.ID).
			Errorf("Collection failed for organization '%s': %v", organization.Name, err)
		return nil
	}
	if target != "" {
		log.Infof("Recorded %d results for organization '%s' and target '%v'", len(results), organization.Name, target)
	} else {
		log.Infof("Recorded %d results for organization '%s'", len(results), organization.Name)
	}
	gaugeResults = append(gaugeResults, results...)
	// stop right away in case of the context being cancelled. This ensures that
	// we don't wait for a complete collect run for all organizations before
	// stopping.
	select {
	case <-ctx.Done():
		return nil
	default:
	}
	return gaugeResults
}

func organizationNames(orgs []org) []string {
	var names []string
	for _, org := range orgs {
		names = append(names, org.Name)
	}
	return names
}

func getOrganizations(client *client, organizationIDs []string) ([]org, error) {
	orgsResponse, err := client.getOrganizations()
	if err != nil {
		return nil, err
	}
	organizations := orgsResponse.Orgs
	if len(organizationIDs) != 0 {
		organizations = filterByIDs(orgsResponse.Orgs, organizationIDs)
		if len(organizations) == 0 {
			return nil, fmt.Errorf("no organizations match the filter: '%v'", strings.Join(organizationIDs, ","))
		}
	}
	return organizations, nil
}

func filterByIDs(organizations []org, ids []string) []org {
	var filtered []org
	for i := range organizations {
		for _, id := range ids {
			if organizations[i].ID == id {
				filtered = append(filtered, organizations[i])
			}
		}
	}
	return filtered
}

// register registers results in the vulnerbility gauge. To handle changing
// flags, e.g. ignored, upgradeable the metric is cleared before setting new
// values.
// See https://github.com/lunarway/snyk_exporter/issues/21 for details.
func register(results []gaugeResult) {
	vulnerabilityGauge.Reset()
	for _, r := range results {
		for _, result := range r.results {
			vulnerabilityGauge.WithLabelValues(r.organization, r.target, r.project, r.projectType, result.id, result.issueType, result.title, result.severity, strconv.FormatBool(result.ignored), strconv.FormatBool(result.upgradeable), strconv.FormatBool(result.patchable), strconv.FormatBool(r.isMonitored), result.cve).Set(float64(result.count))
		}
	}
}

type gaugeResult struct {
	organization string
	target       string
	project      string
	projectType  string
	isMonitored  bool
	results      []aggregateResult
}

func collect(ctx context.Context, client *client, organization org, target string, origins []string, projectFilter string) ([]gaugeResult, error) {
	projects, err := client.getProjects(organization.ID, target, origins, projectFilter)
	if err != nil {
		return nil, fmt.Errorf("get projects for organization: %w", err)
	}

	var gaugeResults []gaugeResult
	for _, project := range projects.Data {
		start := time.Now()
		issues, err := client.getIssues(organization.ID, project.ID)
		duration := time.Since(start)
		if err != nil {
			log.Errorf("Failed to get issues for organization %s (%s) and project %s (%s): duration %v:  %v", organization.Name, organization.ID, project.Attributes.Name, project.ID, duration, err)
			continue
		}
		results := aggregateIssues(issues.Issues)

		gaugeResults = append(gaugeResults, gaugeResult{
			organization: organization.Name,
			target:       strings.Split(project.Attributes.Name, ":")[0],
			//target:      project.Name,
			project:     project.Attributes.Name,
			projectType: project.Attributes.Type,
			results:     results,
			isMonitored: project.Attributes.Status == "active",
		})
		log.Debugf("Collected data in %v for %s %s", duration, project.ID, project.Attributes.Name)
		// stop right away in case of the context being cancelled. This ensures that
		// we don't wait for a complete collect run for all projects before
		// stopping.
		select {
		case <-ctx.Done():
			return nil, nil
		default:
		}
	}
	return gaugeResults, nil
}

type aggregateResult struct {
	id          string
	issueType   string
	title       string
	severity    string
	cve         string
	ignored     bool
	upgradeable bool
	patchable   bool
	count       int
}

func aggregationKey(i issue) string {
	return fmt.Sprintf("%s_%s_%s_%s_%t_%t_%t", i.ID, i.IssueData.Severity, i.IssueType, i.IssueData.Title, i.Ignored, i.FixInfo.Upgradeable, i.FixInfo.Patchable)
}

func aggregateIssues(issues []issue) []aggregateResult {
	aggregateResults := make(map[string]aggregateResult)

	for _, issue := range issues {
		aggregate, ok := aggregateResults[aggregationKey(issue)]
		if !ok {
			cve := ""
			if len(issue.IssueData.Identifiers.CVE) > 0 {
				cve = issue.IssueData.Identifiers.CVE[0]
			}

			aggregate = aggregateResult{
				id:          issue.ID,
				issueType:   issue.IssueType,
				title:       issue.IssueData.Title,
				severity:    issue.IssueData.Severity,
				count:       0,
				ignored:     issue.Ignored,
				upgradeable: issue.FixInfo.Upgradeable,
				patchable:   issue.FixInfo.Patchable,
				cve:         cve,
			}
		}
		aggregate.count++
		aggregateResults[aggregationKey(issue)] = aggregate
	}
	var output []aggregateResult
	for i := range aggregateResults {
		output = append(output, aggregateResults[i])
	}
	return output
}
