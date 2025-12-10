import React, { ChangeEvent } from 'react';

import { DataSourcePluginOptionsEditorProps, SelectableValue } from '@grafana/data';
import { InlineField, Input, SecretInput, Select } from '@grafana/ui';

import { DocBooksDatasourceOptions, DocBooksSecureJsonData } from '../types';

interface Props extends DataSourcePluginOptionsEditorProps<DocBooksDatasourceOptions> {}

export function ConfigEditor(props: Props) {
  const { onOptionsChange, options } = props;

  const onSourceChange = (value: SelectableValue) => {
    const jsonData = {
      ...options.jsonData,
      source: value.value,
    };
    onOptionsChange({ ...options, jsonData });
  };
  const onOwnerChange = (event: ChangeEvent<HTMLInputElement>) => {
    const jsonData = {
      ...options.jsonData,
      owner: event.target.value,
    };
    onOptionsChange({ ...options, jsonData });
  };

  const onRepoChange = (event: ChangeEvent<HTMLInputElement>) => {
    const jsonData = {
      ...options.jsonData,
      repo: event.target.value,
    };
    onOptionsChange({ ...options, jsonData });
  };

  // Secure field (only sent to the backend)
  const onAuthTokenChange = (event: ChangeEvent<HTMLInputElement>) => {
    onOptionsChange({
      ...options,
      secureJsonData: {
        authToken: event.target.value,
      },
    });
  };

  const onResetAuthToken = () => {
    onOptionsChange({
      ...options,
      secureJsonData: {
        ...options.secureJsonData,
        authToken: '',
      },
      secureJsonFields: {
        ...options.secureJsonFields,
        authToken: false,
      },
    });
  };

  const { jsonData, secureJsonFields } = options;
  const secureJsonData = (options.secureJsonData || {}) as DocBooksSecureJsonData;
  const sourceOptions: SelectableValue[] = [{ label: 'GitHub', value: 'github' }];
  const labelWidth = 20;
  const inputWidth = 40;

  return (
    <div className="gf-form-group">
      <InlineField label="Source" labelWidth={labelWidth}>
        <Select
          value={jsonData.source}
          options={sourceOptions}
          onChange={onSourceChange}
          placeholder="Source"
          width={inputWidth}
        />
      </InlineField>
      <InlineField label="Owner" labelWidth={labelWidth}>
        <Input
          onChange={onOwnerChange}
          value={jsonData.owner || ''}
          placeholder="GitHub repo owner"
          width={inputWidth}
        />
      </InlineField>
      <InlineField label="Repo" labelWidth={labelWidth}>
        <Input onChange={onRepoChange} value={jsonData.repo || ''} placeholder="GitHub repo" width={inputWidth} />
      </InlineField>
      <InlineField
        label="Auth Token"
        labelWidth={labelWidth}
        tooltip={'Make sure the auth token has read-only access to the contents of the repo'}
      >
        <SecretInput
          isConfigured={(secureJsonFields && secureJsonFields.authToken) as boolean}
          value={secureJsonData.authToken || ''}
          placeholder="GitHub auth token"
          width={inputWidth}
          onReset={onResetAuthToken}
          onChange={onAuthTokenChange}
        />
      </InlineField>
    </div>
  );
}
