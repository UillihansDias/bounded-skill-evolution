"use strict";
const path = "BOUNDED_SKILL_EVOLUTION_REMINDER.md";
const owner = "bounded-skill-evolution";
const content = "Use bounded-skill-evolution for explicit reusable improvement or recurring failures. Preserve scope, baseline and evidence; eligibility is not publication authority.";
async function handler(event) {
  if (!event || event.type !== "agent" || event.action !== "bootstrap") return;
  if (typeof event.sessionKey !== "string" || event.sessionKey.includes(":subagent:")) return;
  const files = event.context && event.context.bootstrapFiles;
  if (!Array.isArray(files)) return;
  const owned = f => f && f.path === path && f.owner === owner && f.virtual === true;
  if (files.some(f => f && f.path === path && !owned(f))) return;
  event.context.bootstrapFiles = files.filter(f => !owned(f));
  event.context.bootstrapFiles.push({name:path,path,content,owner,virtual:true,missing:false});
}
module.exports = handler;
module.exports.default = handler;
