<?php

namespace App\Grafana;

class Config
{
    public function __construct(
        public readonly string $grafanaHost,
        public readonly string $grafanaUser,
        public readonly string $grafanaPassword,
    )
    {
    }

    public static function fromEnv(array $env): static
    {
        return new static(
            grafanaHost: $env['GRAFANA_HOST'] ?? 'localhost:3000',
            grafanaUser: $env['GRAFANA_USER'] ?? 'admin',
            grafanaPassword: $env['GRAFANA_PASSWORD'] ?? 'admin',
        );
    }
}
