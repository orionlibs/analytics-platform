package main

import (
	"embed"
	"fmt"
	"log"
	"net/http"
	"os"
)

//go:embed static/*
//nolint:gochecknoglobals
var embedFS embed.FS

func main() {
	httpPort := "8080"
	if port := os.Getenv("HTTP_PORT"); port != "" {
		httpPort = port
	}

	services, err := embedFS.ReadFile("static/services.json")
	if err != nil {
		log.Fatal(err)
	}

	http.Handle("/api/services", http.HandlerFunc(func(writer http.ResponseWriter, request *http.Request) {
		writer.Header().Set("Content-Type", "application/json")
		writer.Write(services)
	}))

	log.Print(fmt.Sprintf("Listening on :%s...", httpPort))
	err = http.ListenAndServe(":"+httpPort, nil)
	if err != nil {
		log.Fatal(err)
	}
}
