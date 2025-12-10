/*
 * Copyright The OpenTelemetry Authors
 * SPDX-License-Identifier: Apache-2.0
 */

import { getAllEntries } from "@/lib/store";
import { marked } from "marked";

export const dynamic = "force-dynamic";
export const revalidate = 60;

// Convert markdown to HTML for RSS feeds
function markdownToHtml(markdown: string): string {
  try {
    // Use marked.parse with synchronous option to ensure it returns a string
    return marked.parse(markdown, { async: false }) as string;
  } catch (error) {
    console.warn("Failed to convert markdown to HTML:", error);
    return markdown;
  }
}

// Process GitHub-specific markdown like PR references, commit SHAs, etc.
function processGitHubMarkdown(text: string, repoFullName: string): string {
  let processedText = text;

  // Replace PR references first (including those in parentheses)
  const prPattern = /(?:^|\s|[([])#(\d+)(?=[\s\n\])]|$)/g;
  processedText = processedText.replace(prPattern, (match, issue) => {
    const prefix = match.startsWith("(") || match.startsWith("[") ? match[0] : " ";
    return `${prefix}[#${issue}](https://github.com/${repoFullName}/issues/${issue})`;
  });

  // Replace commit SHAs
  const shaPattern = /(\s|^)([0-9a-f]{40})(?=[\s\n]|$)/g;
  processedText = processedText.replace(shaPattern, (match, space, sha) => {
    return `${space}[${sha}](https://github.com/${repoFullName}/commit/${sha})`;
  });

  // Replace user mentions
  const userPattern = /(?:^|\s)@([a-zA-Z0-9-]+)(?=[\s\n]|$)/g;
  processedText = processedText.replace(userPattern, (match, username) => {
    return ` [@${username}](https://github.com/${username})`;
  });

  // Replace repository references with issue numbers
  const repoPattern = /([a-zA-Z0-9-]+\/[a-zA-Z0-9-._-]+)#(\d+)(?=[\s\n]|$)/g;
  processedText = processedText.replace(repoPattern, (match, repo, issue) => {
    return `[${repo}#${issue}](https://github.com/${repo}/issues/${issue})`;
  });

  return processedText;
}

export async function GET() {
  const entries = await getAllEntries();
  const baseUrl =
    process.env.NEXT_PUBLIC_BASE_URL || "https://changelog.opentelemetry.io";

  const rss = `<?xml version="1.0" encoding="UTF-8" ?>
    <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
      <channel>
        <title>OpenTelemetry Changelog</title>
        <link>${baseUrl}</link>
        <description>Latest changes across OpenTelemetry repositories</description>
        <atom:link href="${baseUrl}/feed" rel="self" type="application/rss+xml" />
        <language>en-US</language>
        ${entries
          .map(
            (entry) => {
              // Process GitHub markdown first, then convert to HTML
              const processedDescription = processGitHubMarkdown(entry.description, entry.metadata.sourceRepo);
              const htmlDescription = markdownToHtml(processedDescription);
              
              return `
          <item>
            <title><![CDATA[${entry.title}]]></title>
            <link>${baseUrl}/entry/${entry.id}</link>
            <guid isPermaLink="false">${entry.id}</guid>
            <pubDate>${new Date(entry.date).toUTCString()}</pubDate>
            <description><![CDATA[${htmlDescription}]]></description>
            ${
              entry.metadata.sourceRepo
                ? `
              <category><![CDATA[${entry.metadata.sourceRepo}]]></category>
            `
                : ""
            }
          </item>
        `}
          )
          .join("")}
      </channel>
    </rss>`;

  return new Response(rss, {
    headers: {
      "Content-Type": "application/xml;charset=utf-8",
      "Cache-Control": "public, s-maxage=60, stale-while-revalidate=300",
    },
  });
}
