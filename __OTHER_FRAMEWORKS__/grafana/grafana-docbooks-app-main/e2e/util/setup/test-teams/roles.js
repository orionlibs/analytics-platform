const { baseURL, fetchCookie, login } = require('../api-utils');
const getRoleUid = async (name) => {
  const searchResponse = await fetchCookie(`${baseURL}/api/access-control/roles?delegatable=true`);

  if (searchResponse.ok) {
    const allRoles = ((await searchResponse.json()) || []).filter((role) => role.group === 'Adaptive Metrics');

    const role = allRoles.find((role) => role.displayName === name);

    if (role) {
      return role.uid;
    } else {
      throw new Error(`Failed to find role ${name}`);
    }
  } else {
    throw new Error(`Failed to search for role ${name}`);
  }
};

const addRoleToTeam = (teamId, roleUid) => {
  return fetchCookie(`${baseURL}/api/access-control/teams/${teamId}/roles`, {
    body: JSON.stringify({ roleUids: [roleUid] }),
    headers: { 'Content-Type': 'application/json' },
    method: 'PUT',
  });
};

module.exports = {
  addRoleToTeam,
  getRoleUid,
};
