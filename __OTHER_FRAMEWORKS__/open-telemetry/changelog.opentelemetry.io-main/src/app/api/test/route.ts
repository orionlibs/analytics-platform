/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import { saveEntry } from "@/lib/store";
import { ChangelogEntry } from "@/types/entry";

export async function POST(request: Request) {
  // Only allow in development
  if (process.env.NODE_ENV !== "development") {
    return new Response("Test endpoint only available in development", {
      status: 403,
    });
  }

  // Get state from query parameters if provided, default to "opened"
  const url = new URL(request.url);
  const state = url.searchParams.get("state") || "opened";
  const validStates = ["opened", "closed", "merged", "released"];
  
  const testEntry: ChangelogEntry = {
    id: Date.now(), // Use timestamp as ID for test entries
    title: `Test Entry ${new Date().toISOString()} (${state})`,
    description: "This is a test entry with **bold text**, *italic* and a [link text](http://example.com) to verify markdown handling in RSS feed.",
    date: new Date().toISOString(),
    metadata: {
      sourceRepo: "open-telemetry/test-repo",
      state: validStates.includes(state) ? state as "opened" | "closed" | "merged" | "released" : "opened",
      url: "https://github.com/open-telemetry/test-repo/pull/123",
      author: "test-user",
    },
  };

  try {
    await saveEntry(testEntry);
    return new Response("Test entry added", { status: 200 });
  } catch (error) {
    console.error("Error adding test entry:", error);
    return new Response("Error adding test entry", { status: 500 });
  }
}
