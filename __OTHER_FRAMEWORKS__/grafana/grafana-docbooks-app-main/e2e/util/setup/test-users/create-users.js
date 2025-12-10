const { baseURL, fetchCookie, login } = require('../api-utils');

const createUser = async (name, role) => {
  const searchResponse = await fetchCookie(
    `${baseURL}/api/users/search?perpage=50&page=0&query=${name}&activeLast30Days=false`
  );

  if (searchResponse.ok) {
    const searchResults = await searchResponse.json();
    if (!searchResults.totalCount) {
      const userCreateResponse = await fetchCookie(`${baseURL}/api/admin/users`, {
        body: JSON.stringify({ email: '', login: name, name, password: 'letmein' }),
        headers: { 'Content-Type': 'application/json' },
        method: 'POST',
      });
      if (userCreateResponse.ok) {
        const userId = (await userCreateResponse.json()).id;
        const roleUpdate = await fetchCookie(`${baseURL}/api/org/users/${userId}`, {
          body: JSON.stringify({ role }),
          headers: { 'Content-Type': 'application/json' },
          method: 'PATCH',
        });
        if (!roleUpdate.ok) {
          console.error(`Failed to update ${name} with ${role} role`, roleUpdate.statusText());
        }
      } else {
        console.error(`Failed to create ${name} user`, userCreateResponse.statusText());
      }
    } else {
      const userId = searchResults.users.find((user) => user.name === name)?.id;
      if (userId) {
        await fetchCookie(`${baseURL}/api/org/users/${userId}`, {
          body: JSON.stringify({ role }),
          headers: { 'Content-Type': 'application/json' },
          method: 'PATCH',
        });
      }
    }
  } else {
    throw new Error(`Failed to search for ${name} user`);
  }
};

const run = async () => {
  await login();
  console.log('Creating [e2eAdmin]');
  await createUser('e2eAdmin', 'Admin');
  console.log('Creating [e2eViewer]');
  await createUser('e2eViewer', 'Viewer');
  console.log('Creating [e2eEditor]');
  await createUser('e2eEditor', 'Editor');
  console.log('Creating [e2eExemptions]');
  await createUser('e2eExemptions', 'Editor');
  console.log('Creating [e2eConfig]');
  await createUser('e2eConfig', 'Editor');
  console.log('Creating [e2ePluginAccess]');
  await createUser('e2ePluginAccess', 'Editor');
  console.log('Creating [e2eNonAdmin]');
  await createUser('e2eNonAdmin', 'Viewer');
  console.log('Creating [e2eNoAccess]');
  await createUser('e2eNoAccess', 'Viewer');
};

run().then(() => console.log('create-users: Done'));
