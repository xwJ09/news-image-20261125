// Entry point for the news-image-20261125 entry (Node 22, stdlib only).
//
// The entry is the pre-drawn PNG sitting next to this file. This program
// copies it, byte for byte, into the output directory so the grader sees
// exactly the image in the repository. It takes no network and no input
// besides the output directory:
//
//   MAKEFUN_OUTPUT_DIR   where entry.png is written (default: "out")
//
// Run it locally with:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "out";

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, join(targetDir, "entry.png"));
