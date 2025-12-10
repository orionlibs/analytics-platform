const { baseURL, fetchCookie, login } = require('../api-utils');
const teamExists = async (name) => {
  // GET /api/teams/search?query=&page=1&perpage=30&accesscontrol=true
  const searchResponse = await fetchCookie(`${baseURL}/api/teams/search?query=&page=1&perpage=30&accesscontrol=true`);

  if (searchResponse.ok) {
    const searchResults = await searchResponse.json();

    if (searchResults.totalCount) {
      const teamId = searchResults.teams.find((team) => team.name === name)?.id;
      return !!teamId;
    }
  } else {
    throw new Error(`Failed to search for role ${name}`);
  }
  return false;
};

const makeTeam = async (name) => {
  const teamCreateResponse = await fetchCookie(`${baseURL}/api/teams`, {
    body: JSON.stringify({ email: '', name }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
  });
  if (teamCreateResponse.ok) {
    return (await teamCreateResponse.json()).teamId;
  } else {
    throw new Error(`Failed to create ${name} team`);
  }
};

const addUsersToTeam = async (teamId, users) => {
  if (users.length) {
    const searchResponse = await fetchCookie(`${baseURL}/api/org/users/lookup?query=&limit=100`);

    if (searchResponse.ok) {
      const allUsers = await searchResponse.json();
      if (allUsers.length) {
        for (const user of users) {
          const userId = allUsers.find((u) => u.login === user)?.userId;
          if (userId) {
            const addResponse = await fetchCookie(`${baseURL}/api/access-control/teams/${teamId}/users/${userId}`, {
              body: JSON.stringify({ permission: 'Member' }),
              headers: { 'Content-Type': 'application/json' },
              method: 'POST',
            });
            if (!addResponse.ok) {
              console.error(`Failed to add ${user} to ${name} team`, addResponse.statusText());
            }
          } else {
            console.error(`Failed to find ${user} to add to ${name} team`);
          }
        }
      }
    } else {
      throw new Error(`Failed to search for users`);
    }
  }
};

module.exports = {
  addUsersToTeam,
  makeTeam,
  teamExists,
};
