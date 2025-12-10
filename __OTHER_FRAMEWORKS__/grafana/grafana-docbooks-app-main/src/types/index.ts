export interface Tree {
  sha: string;
  tree: TreeElement[];
  truncated: boolean;
  url: string;
}

export interface TreeElement {
  mode: string;
  path: string;
  sha: string;
  size?: number;
  type: 'blob' | 'commit' | 'tree';
  url: string;
}
