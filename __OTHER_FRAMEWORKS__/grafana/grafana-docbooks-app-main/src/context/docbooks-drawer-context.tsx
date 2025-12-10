import React, { createContext, useState } from 'react';

type DocbooksDrawerContextType = {
  openFile: { datasourceUid: string; filePath: string } | null;
  setOpenFile: React.Dispatch<React.SetStateAction<{ datasourceUid: string; filePath: string } | null>>;
};

export const DocbooksDrawerContext = createContext<DocbooksDrawerContextType>({} as DocbooksDrawerContextType);

export const DocbooksDrawerContextProvider = ({ children }: { children: React.ReactNode }) => {
  const [openFile, setOpenFile] = useState<{ datasourceUid: string; filePath: string } | null>(null);

  return <DocbooksDrawerContext.Provider value={{ openFile, setOpenFile }}>{children}</DocbooksDrawerContext.Provider>;
};
