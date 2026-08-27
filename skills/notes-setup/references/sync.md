---
name: notes-setup-sync
description: Sync decision for notes-setup — route by the user's sync posture, then elicit constraints rather than recommend a product. Links to official docs only.
---

# Sync — constraints, not a product pick

Sync is the one setup decision where a wrong early choice causes real pain (corruption, lost edits, mobile silently not updating). Don't recommend a product; elicit constraints and let the answer fall out.

## Route by posture (from calibration)

- **Already syncing & happy** → skip entirely. Note what they use so `VAULT.md` reflects reality.
- **Single device** → skip; mention they can add sync later.
- **Multiple devices, no sync yet** → run the constraints interview below.
- **"What's sync?"** → one short explanation first (prose, then pause), *then* the interview. Lead with the key misconception: **Obsidian Sync is the official paid option but is *not* required** — free paths cover most people.

## Four constraints decide almost everything

1. **Platforms** — all-Apple, or mixed (Windows/Android)? Desktop-only or heavy mobile?
2. **Budget** — fine with ~$4–8/mo, or strictly free?
3. **Technical comfort** — happy running a server / living in git, or wants it invisible?
4. **Privacy** — is end-to-end encryption / self-hosting a requirement?

## The map

| Situation | Option | Notes |
|-----------|--------|-------|
| Wants it to just work, will pay | **Obsidian Sync** | Smoothest cross-platform incl. iOS/Android, version history, E2E encryption. Buys you out of every gotcha below. |
| All-Apple, desktop+iOS, free | **iCloud** | Free and effortless *inside* Apple — but warn: mixing Windows into an iCloud vault has reported corruption. Apple-only or don't. |
| Mixed platforms, free, somewhat technical | **Syncthing** | Peer-to-peer, no cloud, free. No first-party iOS app (needs a bridge); devices must be reachable to sync. |
| Wants own storage backend (S3/Dropbox/WebDAV) | **Remotely Save** plugin | Flexible, works on mobile — initial mobile setup is fiddly. |
| Lives in git / wants diffs & history | **Git** (+ Obsidian Git) | Great versioning, free with a private repo — but not friction-free (merge conflicts, commit rhythm) and unstable on mobile. Desktop-centric. |
| Real-time, self-hosted, privacy-max, enjoys infra | **Self-hosted LiveSync** (CouchDB) | Google-Docs-like live sync, no subscription — at the cost of running a server. |

## Two gotchas to state to *every* user

- **Mobile is where sync methods go to die.** iOS especially: iCloud and Sync are fine, most else is flaky. Phone-heavy + won't pay → push toward iCloud (Apple-only) or Syncthing/Remotely Save with eyes open.
- **Conflicts are silent until they aren't.** Plain cloud-drive folders can duplicate or clobber a note edited on two devices. Version history (Sync, git, LiveSync) is the safety net; folder-sync has none.

## Default when they just want to be told

*"If you'll pay a little, Obsidian Sync and stop thinking about it. All-Apple and won't pay, iCloud. Mixed-platform and won't pay, Syncthing — and whatever you pick, lean on a method with version history so a conflict can't quietly eat a note."*

## Official docs

- Obsidian Sync — https://help.obsidian.md/sync
- iCloud / mobile vaults — https://help.obsidian.md/mobile
- Syncthing — https://docs.syncthing.net/
- Remotely Save — https://github.com/remotely-save/remotely-save
- Obsidian Git — https://github.com/Vinzent03/obsidian-git
- Self-hosted LiveSync — https://github.com/vrtmrz/obsidian-livesync
