// retrieves github actions for given username
async function getActions(username) {
  const url = `https://api.github.com/users/${username}/events`;
  const response = await fetch(url);
  const json = response.ok ? await response.json() : null;
  return json;
}
