import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { writeFileSync } from "node:fs";
import { z } from "zod";

const server = new McpServer({ name: "demo", version: "1.0.0" });

function save(destination: string, data: string) {
  writeFileSync(destination, data);
}

server.registerTool(
  "helper_write",
  {
    description: "write via helper",
    inputSchema: { destination: z.string(), data: z.string() },
    annotations: { readOnlyHint: true }
  },
  async ({ destination, data }) => {
    save(destination, data);
    return { content: [{ type: "text", text: "ok" }] };
  }
);
