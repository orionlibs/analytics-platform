const makeFetchCookie = require('fetch-cookie');

const fetchCookie = makeFetchCookie(fetch);
const baseURL = process.env.CI ? 'http://grafana:3000' : 'http://127.0.0.1:3000';

const login = async () => {
  console.log('Logging in as admin');
  await fetchCookie(`${baseURL}/login`, {
    body: JSON.stringify({ password: 'admin', user: 'admin' }),
    headers: { 'Content-Type': 'application/json' },
    method: 'POST',
  });
};

module.exports = {
  baseURL,
  fetchCookie,
  login,
};
