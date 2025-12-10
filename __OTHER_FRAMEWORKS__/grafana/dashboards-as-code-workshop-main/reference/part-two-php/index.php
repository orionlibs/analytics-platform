<?php

error_reporting(E_ALL);

use App\Catalog;
use App\Dashboard;
use App\Grafana;
use App\Grafana\Manifest;

require_once __DIR__.'/vendor/autoload.php';

define('MANIFESTS_DIR', './resources');

$flags = getopt('', [
    'deploy',
    'manifests',
    'help',
]);

$deploy = array_key_exists('deploy', $flags);
$manifests = array_key_exists('manifests', $flags);
$help = array_key_exists('help', $flags);

if ($help) {
    echo 'Usage:'.PHP_EOL;
    echo "\t--deploy\tFetch the list of services from the catalog and deploy a dashboard for each entry".PHP_EOL;
    echo "\t--manifests\tFetch the list of services from the catalog and generate a dashboard manifest for each entry".PHP_EOL;
    exit(1);
}

$grafana = new Grafana\Client(Grafana\Config::fromEnv($_ENV));
$catalog = new Catalog\Client(Catalog\Config::fromEnv($_ENV));

// Fetch the list services from the catalog and deploy a dashboard for each
// of them.
if ($deploy) {
    $services = $catalog->services();

    foreach ($services as $service) {
        $dashboard = Dashboard\Overview::forService($service);
        $folderUid = $grafana->findOrCreateFolder($service->name);

        $grafana->persistDashboard($folderUid, $dashboard);
    }

    $servicesCount = count($services);
    echo "{$servicesCount} dashboards deployed".PHP_EOL;

    exit(0);
}

// Fetch the list services from the catalog and generate a dashboard manifest
// for each of them.
if ($manifests) {
    $services = $catalog->services();

    if (!is_dir(MANIFESTS_DIR)) {
        mkdir(MANIFESTS_DIR, 0777, recursive: true);
    }

    foreach ($services as $service) {
        $dashboard = Dashboard\Overview::forService($service);
        $folderUid = $grafana->findOrCreateFolder($service->name);

        $manifest = Manifest::dashboard($folderUid, $dashboard);
        $filepath = MANIFESTS_DIR . DIRECTORY_SEPARATOR . $dashboard->uid . '.json';
        file_put_contents($filepath, json_encode($manifest, JSON_PRETTY_PRINT));
    }

    $servicesCount = count($services);
    echo "{$servicesCount} manifests generated in ".MANIFESTS_DIR.PHP_EOL;

    exit(0);
}

// Assume we're in "development mode" and print a single dashboard to stdout.
$service = new Catalog\Service(
    'products',
    'A service related to products',
    true,
    true,
    'http://github.com/org/products-service'
);

$dashboard = Dashboard\Overview::forService($service);

$manifest = Manifest::dashboard("", $dashboard);
echo json_encode($manifest, JSON_PRETTY_PRINT).PHP_EOL;
