import fs from 'fs';
import path from 'path';

import { Catalog } from './catalog';
import { dashboardForService } from './dashboard';
import { Client } from './grafana';
import { dashboardManifest } from './manifests';

const manifestsDir = './resources';

const printDevelopmentDashboard = (): void => {
    const service = {
        name: 'products',
        description: 'A service related to products',
        has_http: true,
        has_grpc: true,
        github: 'http://github.com/org/products-service'
    };

    const dashboard = dashboardForService(service);

    const manifest = dashboardManifest('', dashboard.build());
    console.log(JSON.stringify(manifest, null, 2));
};

const fetchServicesAndDeploy = async (): Promise<void> => {
    const grafana = Client.withConfigFromEnv(process.env);
    const catalog = Catalog.withConfigFromEnv(process.env);
    const services = await catalog.services();

    for (const service of services) {
        const dashboard = dashboardForService(service);
        const folderUid = await grafana.findOrCreateFolder(service.name);

        await grafana.persistDashboard(folderUid, dashboard);
    }

    console.log(`${services.length} dashboards deployed`);
};

const fetchServicesAndGenerateManifests = async (): Promise<void> => {
    const grafana = Client.withConfigFromEnv(process.env);
    const catalog = Catalog.withConfigFromEnv(process.env);
    const services = await catalog.services();

    if (!fs.existsSync(manifestsDir)) {
        fs.mkdirSync(manifestsDir);
    }

    for (const service of services) {
        const dashboard = dashboardForService(service).build();
        const folderUid = await grafana.findOrCreateFolder(service.name);

        const manifest = dashboardManifest(folderUid, dashboard);
        const filename = path.join(manifestsDir, `${dashboard.uid!}.json`);
        fs.writeFileSync(filename, JSON.stringify(manifest, null, 2));
    }

    console.log(`${services.length} manifests generated in ${manifestsDir}`);
};

(async () => {
    const deploy = process.argv.includes('--deploy');
    const manifests = process.argv.includes('--manifests');
    const help = process.argv.includes('--help') || process.argv.includes('-h');

    if (help) {
        console.log('Usage:');
        console.log("\t--deploy\tFetch the list of services from the catalog and deploy a dashboard for each entry");
        console.log("\t--manifests\tFetch the list of services from the catalog and generate a dashboard manifest for each entry");
        process.exit(1);
    }

    if (deploy) {
        // Fetch the list services from the catalog and deploy a dashboard for
        // each of them
        await fetchServicesAndDeploy();
        return;
    }

    if (manifests) {
        // Fetch the list services from the catalog and generate a dashboard manifest
        // for each of them.
        await fetchServicesAndGenerateManifests();
        return;
    }

    // By default, assume we're in "development mode" and print a single
    // dashboard to stdout.
    printDevelopmentDashboard();
})();
