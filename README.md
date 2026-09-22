<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![project_license][license-shield]][license-url]

<br />
<div align="center">

<h3 align="center">Bitcoin-Transactions</h3>

  <p align="center">
    A Discord bot for handling Bitcoin transaction requests via a ticket system.
    <br />
    <a href="https://github.com/emlynphoenix/Bitcoin-Transactions"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/emlynphoenix/Bitcoin-Transactions/issues/new?labels=bug">Report Bug</a>
    &middot;
    <a href="https://github.com/emlynphoenix/Bitcoin-Transactions/issues/new?labels=enhancement">Request Feature</a>
  </p>
</div>

> ⚠️ **Disclaimer:** This project is provided for educational purposes only. Use at your own risk. It has not been audited for security and should not be used to move real funds in a production setting.

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

<!-- TODO: add a screenshot of the bot/ticket system in action to images/screenshot.png -->
<!-- ![Bitcoin-Transactions Screenshot](images/screenshot.png) -->

Bitcoin-Transactions is a Discord bot that lets server members open a ticket to request a Bitcoin transaction, with details stored and tracked via a database.

<!-- TODO: replace with 2-3 real sentences on what problem this solves / why you built it -->

**Key features:**
<!-- TODO: keep the ones that are true, delete the rest, add anything missing -->
- 🎟️ Ticket system for submitting transaction requests
- 💾 MySQL-backed request tracking
- 🔐 Restricted/admin-only approval commands
- 📜 Transaction logging

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python.badge]][Python-url]
* [![Discord][Discord.badge]][Discord-url]
* [![MySQL][MySQL.badge]][MySQL-url]
* [![Windows][Windows.badge]][Windows-url]

**Also used:**
- **HeidiSQL** — MySQL database design and administration
- **Blockchain APIs** — payment detection, confirmation tracking, and network fee reporting
- **Price/exchange rate APIs** — USD to BTC conversion
- **Windows VPS (Evoxt)**, administered via RDP — hosting and deployment

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.10+
* A running MySQL server (local or remote)
* A Discord bot token — create one via the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/emlynphoenix/Bitcoin-Transactions.git
   cd Bitcoin-Transactions
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database — create a MySQL database and (if provided) run the included schema/setup script
   ```sh
   mysql -u your_user -p your_database < schema.sql
   ```
4. Create a `.env` file in the project root and add your credentials — **never commit this file**
   ```
   DISCORD_TOKEN=your_token_here
   DB_HOST=localhost
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=your_database
   ```
5. Run the bot
   ```sh
   python main.py
   ```

<!-- TODO: correct the exact install/run commands, schema filename, and any extra env variables (e.g. wallet/API keys) to match your actual setup -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<!-- TODO: replace with your real prefix/commands -->
```
!ticket        Open a new transaction request ticket
!close         Close the current ticket
!history       View your past requests
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

<!-- TODO: real planned features, or delete this section if not needed -->
- [ ] Slash command support
- [ ] Automated transaction verification
- [ ] Admin dashboard

See the [open issues](https://github.com/emlynphoenix/Bitcoin-Transactions/issues) for a full list of proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Emlyn - <!-- TODO: add your email / Discord / contact method or delete this line -->

Project Link: [https://github.com/emlynphoenix/Bitcoin-Transactions](https://github.com/emlynphoenix/Bitcoin-Transactions)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[contributors-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[forks-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/network/members
[stars-shield]: https://img.shields.io/github/stars/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[stars-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/stargazers
[issues-shield]: https://img.shields.io/github/issues/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[issues-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/issues
[license-shield]: https://img.shields.io/github/license/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[license-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/blob/main/LICENSE.txt

[Python.badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Discord.badge]: https://img.shields.io/badge/Discord-5865F2?style=for-the-badge&logo=discord&logoColor=white
[Discord-url]: https://discord.com/developers/docs/intro
[MySQL.badge]: https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/
[Windows.badge]: https://img.shields.io/badge/Windows%20VPS-0078D6?style=for-the-badge&logo=windows&logoColor=white
[Windows-url]: https://www.microsoft.com/windows/
<!-- TODO: replace with 2-3 real sentences on what problem this solves / why you built it -->

**Key features:**
<!-- TODO: keep the ones that are true, delete the rest, add anything missing -->
- 🎟️ Ticket system for submitting transaction requests
- 💾 MySQL-backed request tracking
- 🔐 Restricted/admin-only approval commands
- 📜 Transaction logging

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- TODO: swap these badges for your actual stack -->
* [![Python][Python.badge]][Python-url]
* [![Pycord][Pycord.badge]][Pycord-url]
* [![MySQL][MySQL.badge]][MySQL-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.10+
* A running MySQL server (local or remote)
* A Discord bot token — create one via the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/emlynphoenix/Bitcoin-Transactions.git
   cd Bitcoin-Transactions
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Set up the database — create a MySQL database and (if provided) run the included schema/setup script
   ```sh
   mysql -u your_user -p your_database < schema.sql
   ```
4. Create a `.env` file in the project root and add your credentials — **never commit this file**
   ```
   DISCORD_TOKEN=your_token_here
   DB_HOST=localhost
   DB_USER=your_user
   DB_PASSWORD=your_password
   DB_NAME=your_database
   ```
5. Run the bot
   ```sh
   python main.py
   ```

<!-- TODO: correct the exact install/run commands, schema filename, and any extra env variables (e.g. wallet/API keys) to match your actual setup -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<!-- TODO: replace with your real prefix/commands -->
```
!ticket        Open a new transaction request ticket
!close         Close the current ticket
!history       View your past requests
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

<!-- TODO: real planned features, or delete this section if not needed -->
- [ ] Slash command support
- [ ] Automated transaction verification
- [ ] Admin dashboard

See the [open issues](https://github.com/emlynphoenix/Bitcoin-Transactions/issues) for a full list of proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Emlyn - <!-- TODO: add your email / Discord / contact method or delete this line -->

Project Link: [https://github.com/emlynphoenix/Bitcoin-Transactions](https://github.com/emlynphoenix/Bitcoin-Transactions)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[contributors-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[forks-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/network/members
[stars-shield]: https://img.shields.io/github/stars/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[stars-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/stargazers
[issues-shield]: https://img.shields.io/github/issues/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[issues-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/issues
[license-shield]: https://img.shields.io/github/license/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[license-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/blob/main/LICENSE.txt

[Python.badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Pycord.badge]: https://img.shields.io/badge/Pycord-5865F2?style=for-the-badge&logo=discord&logoColor=white
[Pycord-url]: https://docs.pycord.dev/
[MySQL.badge]: https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/
<!-- TODO: replace with 2-3 real sentences on what problem this solves / why you built it -->

**Key features:**
<!-- TODO: keep the ones that are true, delete the rest, add anything missing -->
- 🎟️ Ticket system for submitting transaction requests
- 💾 Database-backed request tracking
- 🔐 Restricted/admin-only approval commands
- 📜 Transaction logging

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

<!-- TODO: swap these badges for your actual stack -->
* [![Python][Python.badge]][Python-url]
* [![Pycord][Pycord.badge]][Pycord-url]
* [![SQLite][SQLite.badge]][SQLite-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running, follow these steps.

### Prerequisites

* Python 3.10+
* A Discord bot token — create one via the [Discord Developer Portal](https://discord.com/developers/applications)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/emlynphoenix/Bitcoin-Transactions.git
   cd Bitcoin-Transactions
   ```
2. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root and add your credentials — **never commit this file**
   ```
   DISCORD_TOKEN=your_token_here
   ```
4. Run the bot
   ```sh
   python main.py
   ```

<!-- TODO: correct the exact install/run commands and any extra env variables (e.g. wallet/API keys) to match your actual setup -->

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<!-- TODO: replace with your real prefix/commands -->
```
!ticket        Open a new transaction request ticket
!close         Close the current ticket
!history       View your past requests
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

<!-- TODO: real planned features, or delete this section if not needed -->
- [ ] Slash command support
- [ ] Automated transaction verification
- [ ] Admin dashboard

See the [open issues](https://github.com/emlynphoenix/Bitcoin-Transactions/issues) for a full list of proposed features.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Emlyn - <!-- TODO: add your email / Discord / contact method or delete this line -->

Project Link: [https://github.com/emlynphoenix/Bitcoin-Transactions](https://github.com/emlynphoenix/Bitcoin-Transactions)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[contributors-shield]: https://img.shields.io/github/contributors/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[contributors-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[forks-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/network/members
[stars-shield]: https://img.shields.io/github/stars/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[stars-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/stargazers
[issues-shield]: https://img.shields.io/github/issues/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[issues-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/issues
[license-shield]: https://img.shields.io/github/license/emlynphoenix/Bitcoin-Transactions.svg?style=for-the-badge
[license-url]: https://github.com/emlynphoenix/Bitcoin-Transactions/blob/main/LICENSE.txt

[Python.badge]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Pycord.badge]: https://img.shields.io/badge/Pycord-5865F2?style=for-the-badge&logo=discord&logoColor=white
[Pycord-url]: https://docs.pycord.dev/
[SQLite.badge]: https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
