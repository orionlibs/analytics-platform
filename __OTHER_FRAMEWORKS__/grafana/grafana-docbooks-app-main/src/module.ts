import { AppPlugin } from '@grafana/data';

import { App } from '@/components/App';
import { AppConfig } from '@/components/AppConfig';
import { setUpGlobalFloater } from '@/components/GlobalFloater';

export const plugin = new AppPlugin<{}>().setRootPage(App).addConfigPage({
  body: AppConfig,
  icon: 'cog',
  id: 'configuration',
  title: 'Configuration',
});

setUpGlobalFloater();
