import { DataSourceInstanceSettings } from '@grafana/data';
import { DataSourceWithBackend } from '@grafana/runtime';

import { DocBooksDatasourceOptions, DocBooksQuery } from './types';

export class DataSource extends DataSourceWithBackend<DocBooksQuery, DocBooksDatasourceOptions> {
  constructor(instanceSettings: DataSourceInstanceSettings<DocBooksDatasourceOptions>) {
    super(instanceSettings);
  }
}
