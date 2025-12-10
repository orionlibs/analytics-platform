// helper function to split the path and return filename
export const getFileName = (path: string) => {
  const pathParts = path.split('/');
  return pathParts.pop();
};

// helper function to split the path and return directory
export const getDirectory = (path: string) => {
  const pathParts = path.split('/');
  pathParts.pop(); // remove the filename
  return pathParts.join('/') || '__root__';
};
