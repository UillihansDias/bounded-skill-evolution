"use strict";
const assert = require("node:assert/strict");
const handler = require("../hooks/openclaw/handler.js");
(async () => {
  for(const event of [null,{}, {type:"other"}, {type:"agent",action:"bootstrap",context:{bootstrapFiles:[]}}]) await handler(event);
  const e = {type:"agent",action:"bootstrap",sessionKey:"agent:main",context:{bootstrapFiles:[]}};
  await handler(e);assert.equal(e.context.bootstrapFiles.length,1);
  await handler(e);assert.equal(e.context.bootstrapFiles.length,1);
  const sub = {type:"agent",action:"bootstrap",sessionKey:"agent:x:subagent:y",context:{bootstrapFiles:[]}};
  await handler(sub);assert.equal(sub.context.bootstrapFiles.length,0);
  const other = {path:"BOUNDED_SKILL_EVOLUTION_REMINDER.md",virtual:true,content:"not ours"};
  const collision = {type:"agent",action:"bootstrap",sessionKey:"agent:main",context:{bootstrapFiles:[other]}};
  await handler(collision);assert.deepEqual(collision.context.bootstrapFiles,[other]);
  console.log("PASS: malformed events, main injection, idempotency, subagent exclusion, foreign collision");
})().catch(e=>{console.error(e);process.exit(1)});
