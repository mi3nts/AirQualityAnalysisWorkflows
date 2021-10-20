#!/usr/bin/env zx

const DATASET_DIR = "/dataset";
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

console.log("Ingestion starting");
const fullPaths = await globby(['/dataset/**/*.csv']);
const ingestionPromises = fullPaths.map((fullPath) => $`./ingest.mjs --csv ${fullPath}`);
await Promise.all(ingestionPromises);

console.log("Ingestion done");

process.exit(0);