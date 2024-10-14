# Ticket to Ride bot

---

⚠️This is a work in progress. Not working yet.

# High level design

There are two applications:
* The bot which will play "Ticket to Ride", [`ticket-to-ride-bot`](./ticket-to-ride-bot).
* The tool for configuration, [`configurator`](./configurator). This tool helps 
input game data like maps, cities and their routes, screen regions, available tickets etc.


# Setup

```bash
. setup.bash
```

# Running

## Ticket to Ride bot

```bash
python ticket-to-ride-bot/main.py
```

## Configurator

```bash
python configurator/main.py
```

# License
The license in [`LICENSE`](./LICENSE) applies to all files in this repository.