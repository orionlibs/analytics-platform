export interface Service {
    name: string;
    description: string;
    has_http: boolean;
    has_grpc: boolean;
    github: string;
}

export interface CatalogConfig {
    endpoint: string;
}

export class Catalog {
    private readonly config: CatalogConfig;

    constructor(config: CatalogConfig) {
        this.config = config;
    }

    public static withConfigFromEnv(env: Record<string, string>): Catalog {
        return new Catalog({
            endpoint: env['CATALOG_ENDPOINT'] ?? 'http://localhost:8082/api/services',
        });
    }

    public async services(): Promise<Service[]> {
        return fetch(this.config.endpoint)
            .then(response => response.json() as Promise<Service[]>)
        ;
    }
}