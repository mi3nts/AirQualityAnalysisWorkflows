#!/usr/bin/env zx

const DATASET_DIR = "/data/dataset";
$.verbose = false;

// Run graphite daemon
nothrow($`/entrypoint &>/dev/null`);

// Check if the container is running
while (1) {
  try {
    await $`ss -tulpn | grep ":2003"`;
  } catch (p) {
    // sleep for 5 seconds
    await new Promise(resolve => setTimeout(resolve, 5000));
    continue;
  }
  break;
}

const subfolders = await fs.readdir(DATASET_DIR);

for (let subfolder of subfolders) {
  for (let filePath of await fs.readdir(path.join(DATASET_DIR, subfolder))) {
    let fullPath = path.join(DATASET_DIR, subfolder, filePath);
    console.log(fullPath);
    await $`./ingest.mjs --csv ${fullPath}`;
  }
}

// keep running
while (1) {}