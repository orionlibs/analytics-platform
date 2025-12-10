import fs from 'fs';
import path from 'path';

import { exampleDashboard } from './dashboard';
import { Client } from './grafana';
import { dashboardManifest } from './manifests';
import { DashboardBuilder } from '@grafana/grafana-foundation-sdk/dashboard';

const manifestsDir = './resources';
const dashboardFolderName = 'Part one';

const deployDashboard = async (dashboard: DashboardBuilder): Promise<void> => {
    const grafana = Client.withConfigFromEnv(process.env);

    const folderUid = await grafana.findOrCreateFolder(dashboardFolderName);
    await grafana.persistDashboard(folderUid, dashboard);

    console.log(`dashboard deployed`);
};

const generateManifest = async (dashboard: DashboardBuilder): Promise<void> => {
    const grafana = Client.withConfigFromEnv(process.env);
    const builtDashboard = dashboard.build();

    if (!fs.existsSync(manifestsDir)) {
        fs.mkdirSync(manifestsDir);
    }

    const folderUid = await grafana.findOrCreateFolder(dashboardFolderName);
    const manifest = dashboardManifest(folderUid, builtDashboard);

    const filename = path.join(manifestsDir, `${builtDashboard.uid!}.json`);
    fs.writeFileSync(filename, JSON.stringify(manifest, null, 2));

    console.log(`manifest generated in ${manifestsDir}`);
};

(async () => {
    const deploy = process.argv.includes('--deploy');
    const manifests = process.argv.includes('--manifests');
    const help = process.argv.includes('--help') || process.argv.includes('-h');

    if (help) {
        console.log('Usage:');
        console.log("\t--deploy\tGenerate and deploy the test dashboard directly to a Grafana instance");
        console.log("\t--manifests\tGenerate a dashboard manifest for the test dashboard and write it to disk");
        process.exit(1);
    }

    const dashboard = exampleDashboard();

    if (deploy) {
        // Deploy the test dashboard directly to a Grafana instance.
        await deployDashboard(dashboard);
        return;
    }

    if (manifests) {
        // Generate a dashboard manifest for the test dashboard and write it to disk.
        await generateManifest(dashboard);
        return;
    }

    // By default: print the test dashboard to stdout.
    const manifest = dashboardManifest('', dashboard.build());
    console.log(JSON.stringify(manifest, null, 2));
})();
