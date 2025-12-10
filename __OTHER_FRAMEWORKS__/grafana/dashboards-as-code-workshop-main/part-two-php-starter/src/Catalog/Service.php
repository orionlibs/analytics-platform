<?php

namespace App\Catalog;

class Service
{
    public function __construct(
        public readonly string $name,
        public readonly string $description,
        public readonly bool $hasHttp,
        public readonly bool $hasGrpc,
        public readonly string $repositoryUrl,
    )
    {
    }

    public static function fromArray(array $data): static
    {
        return new static(
            name: $data['name'],
            description: $data['description'],
            hasHttp: $data['has_http'],
            hasGrpc: $data['has_grpc'],
            repositoryUrl: $data['github'],
        );
    }
}