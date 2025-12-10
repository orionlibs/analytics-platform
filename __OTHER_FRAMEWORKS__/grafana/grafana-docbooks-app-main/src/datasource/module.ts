import { DataSourcePlugin } from '@grafana/data';

import { ConfigEditor } from './components/ConfigEditor';
import { DataSource } from './datasource';
import { DocBooksDatasourceOptions, DocBooksQuery } from './types';

export const plugin = new DataSourcePlugin<DataSource, DocBooksQuery, DocBooksDatasourceOptions>(DataSource)
  .setConfigEditor(ConfigEditor)
