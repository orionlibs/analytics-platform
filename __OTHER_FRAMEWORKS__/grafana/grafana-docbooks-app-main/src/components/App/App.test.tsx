import React from 'react';

import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';

import { AppRootProps, PluginType } from '@grafana/data';

import { App } from './App';

describe('Components/App', () => {
  let props: AppRootProps;

  beforeEach(() => {
    jest.resetAllMocks();

    props = {
      basename: 'a/sample-app',
      meta: {
        enabled: true,
        id: 'sample-app',
        jsonData: {},
        name: 'Sample App',
        type: PluginType.app,
      },
      onNavChanged: jest.fn(),
      path: '',
      query: {},
    } as unknown as AppRootProps;
  });

  test('renders without an error"', () => {
    render(
      <BrowserRouter>
        <App {...props} />
      </BrowserRouter>
    );

    expect(screen.queryByText(/this is page one./i)).toBeInTheDocument();
  });
});
