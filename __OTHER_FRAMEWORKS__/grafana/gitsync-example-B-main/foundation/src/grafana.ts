import { DashboardBuilder } from "@grafana/grafana-foundation-sdk/dashboard";

export interface Config {
    host: string;
    user: string;
    password: string;
}

interface folder {
    uid: string;
}

export class Client {
    private readonly config: Config;

    constructor(config: Config) {
        this.config = config;
    }

    public static withConfigFromEnv(env: Record<string, string>): Client {
        return new Client({
            host: env['GRAFANA_HOST'] ?? 'localhost:3000',
            user: env['GRAFANA_USER'] ?? 'admin',
            password: env['GRAFANA_PASSWORD'] ?? 'admin',
        });
    }

    public async findOrCreateFolder(name: string): Promise<string> {
        const searchResponse = await fetch(this.url(`/api/search?type=dash-folder&query=${encodeURIComponent(name)}`), {
            headers: {Authorization: this.authHeader()},
        }).then(response => response.json() as Promise<folder[]>);

        // The folder exists.
        if (searchResponse.length === 1) {
            return searchResponse[0].uid;
        }

        const payload = {title: name};
        const reqInit = {
            method: 'POST',
            body: JSON.stringify(payload),
            headers: {
                Authorization: this.authHeader(),
                'Content-Type': 'application/json',
            },
        };
        const createResponse = await fetch(this.url(`/api/folders`), reqInit)
            .then(response => response.json() as Promise<folder>);

        return createResponse.uid;
    }

    public async persistDashboard(folderUid: string, dashboard: DashboardBuilder): Promise<void> {
        const reqInit = {
            method: 'POST',
            body: JSON.stringify({
                dashboard: dashboard.build(),
                folderUid: folderUid,
                overwrite: true,
            }),
            headers: {
                Authorization: this.authHeader(),
                'Content-Type': 'application/json',
            },
        };
        
        await fetch(this.url(`/api/dashboards/db`), reqInit);
    }

    private url(path: string): string {
        return `http://${this.config.host}${path}`;
    }

    private authHeader(): string {
        return "Basic " + Buffer.from(`${this.config.user}:${this.config.password}`).toString('base64');
    }
}
