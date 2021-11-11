#!/usr/bin/env zx

const DATASET_DIR = "/dataset";
// $.verbose = false;

// Check if the container is running
while (1) {
  try {
    await $`ping -c1 graphite:2003`;
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
const ingestionPromises = fullPaths.map((fullPath) => $`/scripts/ingest.mjs --csv ${fullPath}`.then(() => {
  console.log(`Ingested ${++numberOfFilesIngested}`);
}));
await Promise.all(ingestionPromises);

console.log("Ingestion done");

process.exit(0);
