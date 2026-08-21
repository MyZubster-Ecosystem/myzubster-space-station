# MyZubster Space Station

> 🌍 **Understand MyZubster in your language:** [Global multilingual guide](https://github.com/MyZubster-Ecosystem/myzubster/blob/main/docs/i18n/README.md) — English, Italiano, Español, Français, Deutsch, Português, 中文, 日本語, 한국어, العربية, हिन्दी, Русский, Türkçe, Bahasa Indonesia, Polski, Українська, বাংলা, اردو, فارسی, Kiswahili.
>
> MyZubster connects real-world observations, verifiable evidence, collaborative bounties and platform rewards. **MYZ is currently an internal reward/accounting ledger; external XMR/token/blockchain settlement is separate and independently verified.**

Software MVP and simulation track for robotics, telemetry, mission workflows and Gateway integration inside the MyZubster ecosystem.

## Status

**Software MVP / active development.** This repository is a software vertical-slice project. It does **not** imply that MyZubster operates a physical or orbital space station.

The target vertical slice is:

```text
Mission -> Robot/simulator -> Telemetry -> Persistence/Audit -> API -> Dashboard -> Gateway
```

Simulation should be used before physical robot integration.

## Components

| Component | Purpose | Positioning |
|---|---|---|
| Station Core | mission/robot application services | MVP track |
| Robot Registry | robot/device identity and status | MVP track |
| Mission API | mission lifecycle | MVP track |
| Telemetry | ingestion, validation and retrieval | development |
| Gateway integration | connection to MyZubster Gateway | development |
| EVA IONI simulator | reproducible telemetry source | development |
| Dashboard | operator/user interface | development |
| Payment/reward integration | bounty/settlement boundary | gated; not automatically blockchain-settled |

Verify the source tree and automated tests before treating an item as complete.

## Development

The repository may contain Python and Node.js components. Follow the dependency files in the current branch.

Typical station-core setup where applicable:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Prefer synthetic fixtures and simulator telemetry for local validation.

## Safety

- Simulator-first for command/telemetry workflows.
- Physical robot commands require authentication, bounded parameters and fail-safe behavior.
- No mission/bounty should require unauthorized access to restricted infrastructure or collection of sensitive operational details.
- Do not store credentials, private keys or wallet seeds in source or telemetry logs.

## Bounty program

Space Station work is tracked through GitHub issues, including software bounties for simulator, telemetry, dashboard and integration tasks.

The canonical policy is:

- [MyZubster Bounty System](https://github.com/MyZubster-Ecosystem/myzubster/blob/main/BOUNTIES.md)
- [Ecosystem Architecture](https://github.com/MyZubster-Ecosystem/myzubster/blob/main/docs/ECOSYSTEM.md)

Historical `250 MYZ` bounty definitions represent project-declared work rewards. MYZ in the current core platform is an internal reward/accounting ledger, and issue closure/merge does not prove external settlement.

Any XMR/token payment component remains separate and requires independently verifiable settlement evidence before `PAID`.

See `BOUNTIES.md` for this repository's local scope.

## Related repositories

- [myzubster](https://github.com/MyZubster-Ecosystem/myzubster) — canonical core/bounty rules
- [EVA-IONI](https://github.com/MyZubster-Ecosystem/EVA-IONI) — simulator/robotics track
- [MyZubster-Robot](https://github.com/MyZubster-Ecosystem/MyZubster-Robot) — robotics track
- [MyZubsterGateway](https://github.com/MyZubster-Ecosystem/MyZubsterGateway) — Gateway/settlement boundary

## Contributing

Use open issues, add reproducible tests and explicitly distinguish simulator evidence from physical-hardware validation.

## License

See `LICENSE` for authoritative terms.

---

## Official project identity

MyZubster is maintained within the [MyZubster-Ecosystem](https://github.com/MyZubster-Ecosystem) organization. Canonical public administrator/maintainer reference: **[Daniel Ioni (@DanielIoni-creator)](https://github.com/DanielIoni-creator)**.

This link is a stable public project-identity reference. By itself, it is not a cryptographic signature or legal identity certification.
