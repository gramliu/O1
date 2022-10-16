const { App } = require("@slack/bolt");
const dotenv = require("dotenv");
const { parse } = require("csv-parse/sync");
const { readFileSync, writeFileSync } = require("fs");

dotenv.config();

const app = new App({
  token: process.env.SLACK_TOKEN,
  signingSecret: process.env.SIGNING_SECRET,
});

async function createChannels() {
  for (let i = 1; i <= 12; i++) {
    app.client.conversations.create({ name: `big-little-family-${i}` });
  }
}

async function getChannels() {
  const response = await app.client.conversations.list();
  const channels = response.channels
    .map((entry) => ({ name: entry.name, id: entry.id }))
    .filter(({ name }) => name.includes("big-little-"));
  const mapping = {};
  for (const channel of channels) {
    mapping[channel.name] = channel.id;
  }
  return mapping;
}

async function getUserId(user) {
  const { email } = user;
  try {
    const response = await app.client.users.lookupByEmail({ email });
    if (response.ok) {
      return response.user.id;
    } else {
      console.error("Unable to find user: ", user);
    }
  } catch (err) {
    console.error("Unable to find user: ", user);
  }
  return null;
}

async function pullUserIds() {
  const data = readFileSync("data.csv");
  const records = parse(data, {
    delimiter: "\t",
  });

  const users = records.map(([name, email, familyNum]) => ({
    name,
    email,
    familyNum,
  }));

  for (const user of users) {
    const { email } = user;
    user.id = await getUserId(user);
  }

  const lines = [];
  for (const user of users) {
    const line = `${user.email}\t${user.id ?? ""}\t${user.familyNum}`;
    lines.push(line);
  }
  writeFileSync("ids.tsv", lines.join("\n"));

  return users;
}

function getUsers() {
  const data = readFileSync("ids.tsv");
  const records = parse(data, {
    delimiter: "\t",
  });
  const users = records.map(([email, id, familyNum]) => ({
    email,
    id: id.length == 0 ? null : id,
    familyNum: parseInt(familyNum),
  }));
  return users;
}

async function main() {
  const channels = await getChannels();
  const users = getUsers();

  await pullUserIds();

  // for (let i = 1; i <= 12; i++) {
  //   const channelId = channels[`big-little-family-${i}`];
  //   const matchingUsers = users.filter(({ familyNum }) => familyNum == i);
  //   const userIds = matchingUsers
  //     .map((user) => user.id)
  //     .filter((entry) => entry != null)
  //     .join(",");
  //   console.log("Inviting to channel: ", `big-little-family-${i}`, channelId);
  //   console.log(userIds);
  //   await app.client.conversations.invite({
  //     channel: channelId,
  //     users: userIds,
  //   });
  // }
}

main();
