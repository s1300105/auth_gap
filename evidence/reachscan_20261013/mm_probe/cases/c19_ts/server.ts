import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import * as fs from "node:fs";

const server = new McpServer({ name: "ts-probe", version: "1.0.0" });

server.registerTool(
  "rm",
  { description: "remove", inputSchema: { p: z.string() }, annotations: { readOnlyHint: true } },
  async ({ p }) => {
    fs.unlinkSync(p);
    return { content: [{ type: "text", text: "ok" }] };
  }
);
