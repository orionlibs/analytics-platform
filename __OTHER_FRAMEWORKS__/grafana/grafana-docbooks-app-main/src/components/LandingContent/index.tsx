import React from 'react';

import { Icon } from '@grafana/ui';

export const LandingContent = () => {
  return (
    <div>
      <h1>
        <Icon name={'book-open'} size={'xxl'} /> Docbooks
      </h1>
      <p>Docbooks is a plugin to render your documentation where you need it most. In Grafana!</p>
      <h2>Getting started</h2>
      <p>
        Docbooks is fueled by the <code>Docbooks</code> datasource type. If you have not done so already, add a Docbooks
        datasource and connect it to the source of your information. To add a runbook data source:
        <ol>
          <li>Click Connections &gt; Data sources.</li>
          <li>In the Source field, select the source repository of your docbook.</li>
          <li>Enter the details of the data source and add an Auth Token.</li>
          <li>Click Save & test.</li>
          <li>To verify your setup, click Table of contents. You should see the contents of your runbook.</li>
        </ol>
      </p>
    </div>
  );
};
