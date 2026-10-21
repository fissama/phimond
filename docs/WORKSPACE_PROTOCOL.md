# Phimond Workspace Protocol

This project follows the [shared SLP Workspace Protocol](/Users/phileanh/.config/codex-room/workflow/WORKSPACE_PROTOCOL.md). Read [AGENTS.md](../AGENTS.md) for build, phase delivery, Git, DB, and manual validation rules. Use [`.ai/README.md`](../.ai/README.md) for document authority and cold-start order, and [`.ai/ACTIVE.md`](../.ai/ACTIVE.md) for the current work pointer.

## Current initialization boundary

The approved initial Lead assignment is an architecture and roadmap assessment only. It does not authorize feature implementation or Peer coding. Lead must identify current uncommitted P10 art/client work and its owner before assigning any overlapping write scope.

The Lead plan must cover requirements, architecture, risks, milestones, dependencies, delegation, and acceptance criteria. Human approves the initial implementation scope before Peers receive writable assignments.

## Project-specific evidence

Use the master spec and active phase documents for intended behavior; use source, tests, and runtime for current behavior. A phase is complete only with its specified gameplay evidence and review. P00 is closed with a failed dev latency budget; P10 is a design foundation, not completed gameplay. Do not claim 50 CCU certification from the P00 load baseline.

Use only the `phimond_reconstruction` database. Keep `.env`, credentials, `node_modules`, and `.tools/` out of commits. Preserve unrelated work in the current checkout.
