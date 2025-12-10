import React, { CSSProperties, useCallback, useContext, useEffect, useState } from 'react';

import { css, cx } from '@emotion/css';
import Markdown from 'markdown-to-jsx';
import ReactDOM from 'react-dom/client';

import { GrafanaTheme2 } from '@grafana/data';
import { Button, Divider, IconButton, useStyles2 } from '@grafana/ui';

import { DocbookPicker } from './DocbookPicker';
import { LandingContent } from '@/components/LandingContent';
import { ProviderWrapper } from '@/components/ProviderWrapper';
import { DocbooksDrawerContext } from '@/context/docbooks-drawer-context';
import { useFileContent } from '@/hooks/api';

type Props = {};

export function GlobalFloater(_: Props) {
  const styles = useStyles2(getStyles);

  const [isDrawerOpen, setDrawerOpen] = useState(false);

  const toggleDrawer = useCallback(() => setDrawerOpen(!isDrawerOpen), [setDrawerOpen, isDrawerOpen]);

  const { setOpenFile } = useContext(DocbooksDrawerContext);
  const { data: fileContent } = useFileContent();

  useEffect(() => {
    // Press d followed by b to open docbooks

    let prevKey = 'x';
    let prevTime = Number.NaN;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLElement) {
        if (e.target.tagName === 'input') {
          console.log('REJECTED TARGET', e.target);
          return;
        }
      }

      const deltaTime = e.timeStamp - prevTime;

      if (prevKey === 'd' && e.key === 'b' && deltaTime < 1000) {
        setDrawerOpen(true);
      }

      prevKey = e.key;
      prevTime = e.timeStamp;
    };
    document.addEventListener('keydown', handleKeyDown, true);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [setDrawerOpen]);

  const widthOverride: CSSProperties = isDrawerOpen ? {} : { width: 0 };

  return (
    <div>
      <div className={cx(styles.drawer, 'scrollbar-view')} style={widthOverride}>
        {isDrawerOpen && (
          <div className={styles.drawerContents} style={widthOverride}>
            <div className={styles.controlsContainer}>
              <DocbookPicker />
              {fileContent && (
                <Button variant={'secondary'} onClick={() => setOpenFile(null)}>
                  Close
                </Button>
              )}
            </div>
            <Divider direction={'horizontal'} />
            {fileContent ? <Markdown>{fileContent}</Markdown> : <LandingContent />}
          </div>
        )}
      </div>

      <IconButton
        className={styles.drawerButton}
        aria-label="Open docbooks"
        size="xxxl"
        tooltip={'Docbooks'}
        variant="primary"
        name={'book-open'}
        onClick={toggleDrawer}
      >
        Run Books
      </IconButton>
    </div>
  );
}

function getStyles(theme: GrafanaTheme2) {
  const drawerWidth = 'calc(100vw / 3)';

  return {
    controlsContainer: css({
      alignItems: 'flex-start',
      display: 'flex',
      flexDirection: 'row',
      gap: theme.spacing(2),
      marginTop: theme.spacing(1),
    }),
    drawer: css({
      backgroundColor: theme.colors.background.primary,
      borderLeft: `solid 1px ${theme.colors.border.weak}`,
      height: 'calc(100vh - 64px)',
      marginLeft: theme.spacing(1),
      padding: theme.spacing(1),
      transition: 'width 0.2s ease-in-out',
      width: drawerWidth,
    }),
    drawerButton: css({
      bottom: theme.spacing(2),
      position: 'absolute',
      right: theme.spacing(2),
      zIndex: 1000, // Under drawer, but above Grafana
    }),
    drawerContents: css({
      display: 'flex',
      flexDirection: 'column',
      gap: theme.spacing(2),
      height: '100%',
      img: {
        maxWidth: '100%',
      },
      marginLeft: theme.spacing(1),
      overflowY: 'scroll',
      paddingLeft: theme.spacing(2),
    }),
  };
}

export function setUpGlobalFloater() {
  const floater = document.createElement('div');
  const pageContent = document.getElementById('pageContent');

  if (pageContent == null || pageContent?.parentElement === null) {
    setTimeout(setUpGlobalFloater, 100);
    return;
  }

  floater.id = 'grafana-docbooks-app-floater';
  pageContent.parentElement.appendChild(floater);
  ReactDOM.createRoot(floater).render(
    <ProviderWrapper>
      <GlobalFloater />
    </ProviderWrapper>
  );
}
