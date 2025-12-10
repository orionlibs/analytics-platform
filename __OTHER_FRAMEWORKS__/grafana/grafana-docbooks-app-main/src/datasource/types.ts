import { DataSourceJsonData } from '@grafana/data';
import { DataQuery } from '@grafana/schema';

export interface DocBooksQuery extends DataQuery {}

/**
 * These are options configured for each DataSource instance
 */
export interface DocBooksDatasourceOptions extends DataSourceJsonData {
  owner?: string;
  repo?: string;
  source?: 'github';
}

/**
 * Value that is used in the backend, but never sent over HTTP to the frontend
 */
export interface DocBooksSecureJsonData {
  authToken?: string;
}
