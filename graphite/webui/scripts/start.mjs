#!/usr/bin/env zx

// Run entrypoint
$`/entrypoint`;

// Check if data folder does not exist already
if (await globby(['/opt/graphite/storage/whisper/data']).length === 0) {
  console.log('Data folder does not exist; copying from previous data');
  await $`cp -R /igdata /opt/graphite/storage/whisper/data`;
}