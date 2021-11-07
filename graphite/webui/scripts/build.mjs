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

let numberOfFilesIngested = 0;
const fullPaths = await globby(['/dataset/**/*.csv']);
console.log(`Ingesting ${fullPaths.length} file(s)`);
const ingestionPromises = fullPaths.map((fullPath) => $`./ingest.mjs --csv ${fullPath}`.then(() => {
  console.log(`Ingested ${++numberOfFilesIngested}`);
}));
await Promise.all(ingestionPromises);

console.log("Ingestion done");

// Confirm if ingestion was successful
if (await globby(['/opt/graphite/storage/whisper/data']).length === 0) {
  console.error('Ingested data folder not found');
  process.exit(1);
}
// Preserve data folder
await(nothrow($`cp -R /opt/graphite/storage/whisper/data /igdata`));

process.exit(0);
