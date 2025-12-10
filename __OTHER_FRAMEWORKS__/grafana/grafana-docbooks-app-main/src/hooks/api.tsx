import { useContext } from 'react';

import { useQueries, useQuery } from '@tanstack/react-query';
import { dirname, resolve } from 'path-module';

import { config, getBackendSrv } from '@grafana/runtime';

import { datasourceResourceEndpoint } from '@/api';
import { DocbooksDrawerContext } from '@/context/docbooks-drawer-context';
import { Tree } from '@/types';

export const useTableOfContents = () => {
  const docbookDatasources = Object.values(config.datasources).filter(
    (ds) => ds.type === 'grafana-docbooks-datasource'
  );

  return useQueries({
    combine: (results) => {
      const toc: { [k: string]: { datasourceUid: string; tree: Tree } } = {};
      results
        .map((r) => r.data)
        .filter((d) => d)
        .forEach((treeWrapper) => {
          if (treeWrapper) {
            const { datasource, datasourceUid, tree } = treeWrapper;

            toc[datasource] = { datasourceUid, tree };
          }
        });
      return toc;
    },
    queries: docbookDatasources.map((ds) => ({
      queryFn: async () => {
        return {
          datasource: ds.name,
          datasourceUid: ds.uid,
          tree: await getBackendSrv().get<Tree>(datasourceResourceEndpoint(ds.uid) + '/table-of-contents'),
        };
      },
      queryKey: ['table-of-contents', ds.uid],
    })),
  });
};

const replaceImageLinks = (markdown: string, baseUrl: string, relativeFilePath: string): string => {
  const regex = /!\[(.*?)\]\((\.{1,2}\/.+?)\)/gm;

  return markdown.replace(regex, (match, p1, p2) => {
    const resolvedPath = resolve('/', dirname(relativeFilePath), p2);

    return `![${p1}](${baseUrl}${resolvedPath})`;
  });
};

export const useFileContent = () => {
  const { openFile } = useContext(DocbooksDrawerContext);

  const { datasourceUid, filePath } = openFile || {};

  return useQuery({
    enabled: !!openFile,
    queryFn: async () => {
      const baseUrl = datasourceResourceEndpoint(datasourceUid!) + '/file?path=docbooks';
      let fileContent = await getBackendSrv().get<string>(`${baseUrl}/${filePath}`);
      fileContent = replaceImageLinks(fileContent, baseUrl, filePath!);
      return fileContent;
    },
    queryKey: ['file-content', datasourceUid, filePath],
  });
};
