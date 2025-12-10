/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

"use client";

import { useState } from "react";

export function TestControls() {
  const [status, setStatus] = useState<string>("");
  const [entryState, setEntryState] = useState<string>("opened");

  const addTestEntry = async (state: string) => {
    try {
      setStatus(`Adding test entry with state: ${state}...`);
      const response = await fetch(`/api/test?state=${state}`, {
        method: "POST",
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      setStatus(`Test entry (${state}) added! Check if the page updates.`);

      // Clear status after 3 seconds
      setTimeout(() => setStatus(""), 3000);
    } catch (error) {
      setStatus(
        `Error: ${error instanceof Error ? error.message : String(error)}`,
      );
    }
  };

  return (
    <div className="fixed bottom-4 right-4 p-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700">
      <div className="flex flex-col gap-2">
        <div className="flex gap-2">
          <select 
            value={entryState}
            onChange={(e) => setEntryState(e.target.value)}
            className="px-2 py-2 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="opened">Opened</option>
            <option value="closed">Closed</option>
            <option value="merged">Merged</option>
            <option value="released">Released</option>
          </select>
          <button
            onClick={() => addTestEntry(entryState)}
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            Add Test Entry
          </button>
        </div>
        {status && (
          <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">
            {status}
          </p>
        )}
      </div>
    </div>
  );
}
