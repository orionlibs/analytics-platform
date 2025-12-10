<?php

namespace App\Catalog;

class Config
{
    public function __construct(
        public readonly string $catalogEndpoint,
    )
    {
    }

    public static function fromEnv(array $env): static
    {
        return new static(
            catalogEndpoint: $env['CATALOG_ENDPOINT'] ?? 'http://localhost:8082/api/services',
        );
    }
}