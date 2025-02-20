📌 YouTube Live Chat Moderation Bot
A powerful bot designed to detect and block spam messages, prevent bot attacks, and ensure only real viewers interact in a YouTube Live Stream.

🚀 Features
✅ Detect & Remove Spam Messages – Filters repetitive, bot-like messages.
✅ Auto-Ban Spammers – Bans users sending too many spam messages.
✅ Timeout Feature – Places users in a temporary timeout if detected as bots.
✅ Live Monitoring – Continuously scans YouTube live chat in real time.
✅ User-Friendly Setup – Just provide the live stream link, and the bot does the rest.

🔧 Installation & Setup
1️⃣ Clone the Repository

git clone https://github.com/YOUR-USERNAME/YOUR-REPO.git
cd YOUR-REPO

2️⃣ Install Dependencies

pip install -r requirements.txt
3️⃣ Set Up Google API Credentials

Go to Google Cloud Console.
Create a new project and enable YouTube Data API v3.
Create OAuth 2.0 Client Credentials (set Application Type as Desktop App).
Download client_secret.json and place it inside the project folder.

4️⃣ Run the Bot

python main.py
Follow the authentication steps to grant permission.

🛠️ Configuration
Modify config.py (if available) to customize bot behavior:

SPAM_THRESHOLD = 3  # Number of repeated messages before banning a user
TIMEOUT_DURATION = 300  # Timeout in seconds

⚠️ Limitations
❌ Cannot Remove Bot Views (Only YouTube can handle fake view detection).
❌ Cannot Ban Users from Watching (Only chat moderation is possible).

💡 Future Enhancements
🔹 Improve spam detection using AI-based text analysis.
🔹 Implement custom filtering for specific words or links.
🔹 Auto-detect suspicious accounts based on account age or activity.

👨‍💻 Contributing
Fork the repository.
Create a new branch: git checkout -b feature-branch.
Make your changes and commit: git commit -m "Added new feature".
Push to GitHub: git push origin feature-branch.
Open a Pull Request.
