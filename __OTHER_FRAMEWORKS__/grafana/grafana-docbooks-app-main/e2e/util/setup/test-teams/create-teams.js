const { baseURL, fetchCookie, login } = require('../api-utils');

const { kebabCase: _kebabCase } = require('lodash');

const { addRoleToTeam, getRoleUid } = require('./roles');
const { addUsersToTeam, makeTeam, teamExists } = require('./teams');
const createTeam = async (role, ...users) => {
  const teamName = _kebabCase('DBFE' + role);

  if (!(await teamExists(teamName))) {
    const roleUid = await getRoleUid(role);
    const teamId = await makeTeam(teamName);
    await addRoleToTeam(teamId, roleUid);
    await addUsersToTeam(teamId, users);
  } else {
    console.error(`Team ${teamName} already exists`);
  }
};

const run = async () => {
  await login();
  console.log('Creating [Rules Reader] team');
  await createTeam('Rules Reader', 'e2eEditor', 'e2eViewer');
  console.log('Creating [Exemptions Editor] team');
  await createTeam('Exemptions Editor', 'e2eExemptions');
  console.log('Creating [Config Editor] team');
  await createTeam('Config Editor', 'e2eConfig');
  console.log('Creating [Plugin Access] team');
  await createTeam('Plugin Access', 'e2ePluginAccess');
  console.log('Creating [Admin] team');
  await createTeam('Admin', 'e2eNonAdmin');
};

run().then(() => console.log('create-teams: Done'));
