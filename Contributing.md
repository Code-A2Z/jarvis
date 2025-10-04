<h1 align="center">Contributors Guide⚡ </h1>
<h3 align="center">Welcome to our open-source project! 😍<br> We appreciate your interest in contributing.😊 <br>This guide will help you get started with the project and make your first contribution.</h3>

---

<h1 align="center">Creating first Pull Request 🌟</h1>

1. Star this repository.
2. Fork this repository.

3. Clone the forked repository.
```bash
git clone https://github.com/<your-github-username>/Jarvis.git
```

4. Navigate to the project directory.
```bash
cd Jarvis
```

5. Install Dependencies

**Step 1: Install uv (Skip if Already Installed)**

Choose the command for your operating system:

On Linux/macOS (using Bash):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows (using PowerShell):
```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Step 2: Install Project Dependencies**

Run this command in your project directory. It automatically creates and uses a virtual environment named `.venv`.
```sh
uv sync
```

6. Create a new branch.
```bash
git checkout -b <your_branch_name>
```

7. Make changes.
8. Stage your changes and commit them.
```bash
git add .
git commit -m "<your_commit_message"
```

9. Push your local commits to the remote repository.
```bash
git push -u origin <your_branch_name>
```

10. Create your Pull Request.
11. Congratulations! 🎉 you've made your contribution.

### Running the Application

1. Start the application.
```bash
uv run streamlit run Jarvis.py
```
2. Access the application.
> Open your browser and navigate to `http://localhost:8501`

---

### Communication and Support 💬
- Join the project's communication channels to interact with other contributors and seek assistance.
- If you have any questions or need help, don't hesitate to ask in the project's communication channels or comment on the relevant issue.

### Code of Conduct 😇
Please follow our project's code of conduct while contributing.</br>Treat all contributors and users with respect and create a positive and inclusive environment for everyone.

### License 📄
The project is licensed under ***MIT***. Make sure to review and comply with the license terms.</br>We hope this guide helps you get started with contributing to our open-source project. Thank you for your contribution!

### Need more help?🤔

You can refer to the following articles on basics of Git and Github and also contact the Project Mentors, in case you are stuck:

- [Forking a Repo](https://help.github.com/en/github/getting-started-with-github/fork-a-repo)
- [Cloning a Repo](https://help.github.com/en/desktop/contributing-to-projects/creating-an-issue-or-pull-request)
- [How to create a Pull Request](https://opensource.com/article/19/7/create-pull-request-github)
- [Getting started with Git and GitHub](https://towardsdatascience.com/getting-started-with-git-and-github-6fcd0f2d4ac6)
- [Learn GitHub from Scratch](https://lab.github.com/githubtraining/introduction-to-github)

---

### Note from Admin ❗

- We welcome contributions from everyone. However, please avoid spamming the repository with irrelevant issues & pull requests. We reserve the right to mark PRs as invalid if they are not relevant.

<div align="center">
  <img src="https://media.giphy.com/media/LnQjpWaON8nhr21vNW/giphy.gif" width="60"> <em><b>I love connecting with different people</b> so if you want to say <b>hi, I'll be happy to meet you more!</b> :)</em>
</div>
