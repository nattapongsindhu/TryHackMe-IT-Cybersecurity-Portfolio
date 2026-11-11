# 02 — Linux Fundamentals

_Notes from the Linux, command-line and privilege-escalation work._

## Permissions are the attack surface

When asking "how would someone go from a user shell to root here", there are four places to look
before anything fancy:

1. **SUID binaries** — a program that runs as its owner regardless of who invoked it. Useful by design,
   catastrophic when it trusts its environment.
2. **Writable service files** — a unit or script the service account executes and another user can edit.
3. **Sudo entries** — the interesting ones are not `ALL=(ALL) ALL` but the narrow, specific rules
   nobody reviewed.
4. **Scheduled jobs** — cron and timers that run as root and read from a directory someone else can write.

None of these require an exploit. They require a misconfiguration and a curious user.

## The command line is the job

An analyst working on a Linux host needs a small set of reflexes:

| Reflex | Command family |
| :--- | :--- |
| What is running right now | `ps aux`, `top`, `ss -tulpn` |
| What happened recently | `journalctl`, `tail /var/log/auth.log` |
| What is scheduled | `crontab -l`, `systemctl list-timers` |
| What changed on disk | `find -newer`, `ls -la` on temp directories |
| Who is logged in | `who`, `w`, `last` |

The point is not memorising flags. It is being able to answer "what is true about this host right now"
in under a minute.

## Logs are deliberately spread out

Authentication, kernel, service and application events land in different places on purpose. A single
suspicious login usually has evidence in two of them:

- the authentication log says a session opened,
- the process or service log says what that session did.

Reading only one of the two produces either a false alarm or a missed one.

## Read-only first

Before changing anything on a suspected host:

1. record the process list,
2. record listening sockets,
3. record scheduled jobs and recently modified files,
4. *then* act.

Restarting a service or rebooting the box destroys exactly the evidence you will be asked for later.
This is the Linux version of the same rule that applies on Windows with memory capture.

## Where I am still learning

- Deep systemd unit debugging (why a service failed, in detail).
- Kernel-level tracing (`bpftrace`, `auditd` rule design).
- Package and supply-chain integrity checks.

These are on the [next steps](../README.md#9-next-steps) list rather than pretended.
