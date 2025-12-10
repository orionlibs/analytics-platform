<?php

namespace App\Grafana;

use Grafana\Foundation\Dashboard\Dashboard;
use GuzzleHttp;

class Client
{
    private GuzzleHttp\Client $http;

    public function __construct(
        private readonly Config $config
    )
    {
        $this->http = new GuzzleHttp\Client([
            'base_uri' => 'http://'.$this->config->grafanaHost,
            'auth'     => [$this->config->grafanaUser, $this->config->grafanaPassword],
        ]);
    }

    public function findOrCreateFolder(string $name): string
    {
        $response = $this->http->request('GET', '/api/search?type=dash-folder&query='.urlencode($name));
        if ($response->getStatusCode() !== 200) {
            throw new \RuntimeException("could not fetch folders list: expected 200, got {$response->getStatusCode()}");
        }

        $decoded = json_decode((string) $response->getBody(), true);

        // The folder exists.
        if (count($decoded) === 1) {
            return $decoded[0]['uid'];
        }

        // The folder doesn't exist: we create it.
        $response = $this->http->request('POST', '/api/folders', [
            'json' => [
                'title' => $name,
            ],
        ]);
        if ($response->getStatusCode() !== 200) {
            throw new \RuntimeException("could not create new folder: expected 200, got {$response->getStatusCode()}");
        }

        $decoded = json_decode((string) $response->getBody(), true);

        return $decoded['uid'];
    }

    public function persistDashboard(string $folderUid, Dashboard $dashboard): void
    {
        $response = $this->http->request('POST', '/api/dashboards/db', [
            'json' => [
                'dashboard' => $dashboard,
                'folderUid'  => $folderUid,
                'overwrite' => true,
            ],
        ]);
        if ($response->getStatusCode() !== 200) {
            throw new \RuntimeException("could not persist dashboard: expected 200, got {$response->getStatusCode()}");
        }
    }
}