<?php

namespace App\Catalog;

use GuzzleHttp;

class Client
{
    public function __construct(private Config $config)
    {
    }

    /**
     * @return Service[]
     */
    public function services(): array
    {
        $client = new GuzzleHttp\Client(['base_uri' => $this->config->catalogEndpoint]);
        $response = $client->request('GET', '');

        if ($response->getStatusCode() !== 200) {
            throw new \RuntimeException("could not fetch service catalog: expected 200, got {$response->getStatusCode()}");
        }

        $decoded = json_decode((string) $response->getBody(), true);

        return array_map([Service::class, 'fromArray'], $decoded);
    }
}