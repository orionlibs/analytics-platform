import React from 'react';

import { PluginPage } from '@grafana/runtime';

import { testIds } from '@/components/testIds';

export function FilePage() {
  return (
    <PluginPage>
      <div data-testid={testIds.pageTwo.container}>
        <p>This is page two.</p>
      </div>
    </PluginPage>
  );
}
