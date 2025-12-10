package plugin

import (
	"net/http"
)

func (ds *Datasource) handleToc(w http.ResponseWriter, r *http.Request) {
	switch ds.settings.Source {
	case "github":
		ds.fetchGithubToc(w, r)
	default:
		http.Error(w, "Unsupported docbooks source", http.StatusNotImplemented)
		return
	}
}

func (ds *Datasource) handleFile(w http.ResponseWriter, r *http.Request) {
	ds.fetchGithubFile(w, r)
}

func (ds *Datasource) registerRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/table-of-contents", ds.handleToc)
	mux.HandleFunc("/file", ds.handleFile)
}
