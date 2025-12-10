const { baseURL, fetchCookie, login } = require('../api-utils');
const deleteUser = async (name) => {
  const searchResponse = await fetchCookie(
    `${baseURL}/api/users/search?perpage=50&page=0&query=${name}&activeLast30Days=false`
  );

  if (searchResponse.ok) {
    const searchResults = await searchResponse.json();
    if (!searchResults.totalCount) {
      console.log(`User ${name} not found`);
    } else {
      const userId = searchResults.users.find((user) => user.name === name)?.id;
      if (userId) {
        const deleteResponse = await fetchCookie(`${baseURL}/api/org/users/${userId}`, { method: 'DELETE' });
        if (!deleteResponse.ok) {
          console.error(`Failed to delete ${name} user`, deleteResponse.statusText());
        }
      }
    }
  } else {
    throw new Error(`Failed to search for ${name} user`);
  }
};

const run = async () => {
  await login();
  console.log('Deleting [e2eAdmin]');
  await deleteUser('e2eAdmin');
  console.log('Deleting [e2eViewer]');
  await deleteUser('e2eViewer');
  console.log('Deleting [e2eEditor]');
  await deleteUser('e2eEditor');
  console.log('Deleting [e2eExemptions]');
  await deleteUser('e2eExemptions');
  console.log('Deleting [e2eConfig]');
  await deleteUser('e2eConfig');
  console.log('Deleting [e2ePluginAccess]');
  await deleteUser('e2ePluginAccess');
  console.log('Deleting [e2eNonAdmin]');
  await deleteUser('e2eNonAdmin');
  console.log('Deleting [e2eNoAccess]');
  await deleteUser('e2eNoAccess');
};

run().then(() => console.log('delete-users: Done'));
