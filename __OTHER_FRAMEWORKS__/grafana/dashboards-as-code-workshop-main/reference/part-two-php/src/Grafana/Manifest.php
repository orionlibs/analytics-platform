<?php

namespace App\Grafana;

use Grafana\Foundation\Dashboard\Dashboard;
use Grafana\Foundation\Resource;

class Manifest
{
    public static function dashboard(string $folderUid, Dashboard $dashboard): Resource\Manifest
    {
        return new Resource\Manifest(
            apiVersion: 'dashboard.grafana.app/v1beta1',
            kind: 'Dashboard',
            metadata: new Resource\Metadata(
                annotations: [
                    "grafana.app/folder" => $folderUid,
                ],
                name: $dashboard->uid,
            ),
            spec: $dashboard,
        );
    }
}
