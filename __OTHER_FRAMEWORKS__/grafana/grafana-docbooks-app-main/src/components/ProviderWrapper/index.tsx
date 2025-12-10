import React from 'react';

import { QueryClientProvider } from '@tanstack/react-query';

import { DocbooksDrawerContextProvider } from '@/context/docbooks-drawer-context';
import { queryClient } from '@/state';

type Props = {
  children: React.ReactNode;
};

export const ProviderWrapper = ({ children }: Props) => {
  return (
    <DocbooksDrawerContextProvider>
      <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
    </DocbooksDrawerContextProvider>
  );
};
