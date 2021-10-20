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

const fullPaths = await globby(['/dataset/**/*.csv']);
for (const [i, fullPath] of fullPaths.entries()) {
  console.log(`Ingesting file ${i+1}/${fullPath.length}`)
  await $`./ingest.mjs --csv ${fullPath}`;
}

console.log("Ingestion done");

process.exit(0);