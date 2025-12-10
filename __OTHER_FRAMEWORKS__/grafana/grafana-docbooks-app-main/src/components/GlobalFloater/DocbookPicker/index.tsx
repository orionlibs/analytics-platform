import React, { useContext } from 'react';

import { basename, dirname, extname } from 'path-module';

import { Button, Dropdown, Menu, MenuItemProps } from '@grafana/ui';

import { DocbooksDrawerContext } from '@/context/docbooks-drawer-context';
import { useTableOfContents } from '@/hooks/api';

const TableOfContentsMenu = () => {
  const toc = useTableOfContents();
  const { setOpenFile } = useContext(DocbooksDrawerContext);

  return (
    <Menu>
      {Object.entries(toc).map(
        ([
          datasource,
          {
            datasourceUid,
            tree: { tree },
          },
        ]) => {
          const dirs = tree.reduce(
            (
              acc: {
                [k: string]: Array<React.ReactElement<MenuItemProps, string | React.JSXElementConstructor<any>>>;
              },
              node
            ) => {
              //const dir = node.type === 'tree' ? node.path : getDirectory(node.path);
              const dir = node.type === 'tree' ? node.path : dirname(node.path);
              if (!acc[dir]) {
                acc[dir] = [];
              }
              // Only add to the group if it's a markdown file
              if (node.type === 'blob' && extname(node.path) === '.md') {
                acc[dir].push(
                  <Menu.Item
                    label={basename(node.path, '.md')}
                    onClick={() => {
                      setOpenFile({ datasourceUid, filePath: node.path });
                    }}
                  />
                );
              }
              return acc;
            },
            {}
          );
          // TODO: When rendering the directories, look for directories that would be under other directories and render them as submenus
          return (
            <Menu.Group key={`toc-group-${datasource}`} label={datasource}>
              {dirs['.'] && dirs['.'].length > 0 && dirs['.']}
              {Object.entries(dirs).map(([dir, items]) => {
                // root items are rendered separately
                if (dir === '.' || items.length === 0) {
                  return null;
                }
                return <Menu.Item key={`toc-group-${datasource}-${dir}`} label={dir} childItems={items} />;
              })}
            </Menu.Group>
          );
        }
      )}
    </Menu>
  );
};

export const DocbookPicker = () => {
  return (
    <Dropdown overlay={<TableOfContentsMenu />}>
      <Button variant={'secondary'} icon={'table'}>
        Table of contents
      </Button>
    </Dropdown>
  );
};
