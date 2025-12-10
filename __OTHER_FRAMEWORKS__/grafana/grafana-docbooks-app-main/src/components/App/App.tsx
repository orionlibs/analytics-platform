import React from 'react';

import { Route, Routes } from 'react-router-dom';

import { AppRootProps } from '@grafana/data';

import { ROUTES } from '@/constants';
import { FilePage, TableOfContents } from '@/pages';

export function App(props: AppRootProps) {
  return (
    <Routes>
      <Route path={`${ROUTES.FilePage}/:datasourceUid/:file`} element={<FilePage />} />

      {/* Default page */}
      <Route path="*" element={<TableOfContents />} />
    </Routes>
  );
}
