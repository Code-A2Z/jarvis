from github import Github
import streamlit as st
import subprocess

def createRepository(user):
  repoName = st.text_input("Enter the repository name")
  if st.button("Create Repository") and repoName != "":
    repo = user.create_repo(repoName)
    st.success(f"Repository '{repo.name}' created successfully!", icon="🎉")

def listRepositories(user):
  repos = user.get_repos()
  st.toast("Your repositories!", icon="😀")
  for i, repo in enumerate(repos):
    st.info(f"{i+1}. {repo.name}")

def createIssue(user):
  repoName = st.selectbox("Select the repository", [repo.name for repo in user.get_repos()])
  issueTitle = st.text_input("Enter the issue title")
  if st.button("Create Issue") and repoName != "" and issueTitle != "":
    repo = user.get_repo(repoName)
    issue = repo.create_issue(title=issueTitle)
    st.success(f"Issue '{issue.title}' created successfully in '{repo.name}' Repository!", icon="🎉")

def createPullRequest(user):
  repoName = st.selectbox("Select the repository", [repo.name for repo in user.get_repos()])
  title = st.text_input("Enter the pull request title")
  headBranch = st.text_input("Enter the head branch")
  baseBranch = st.text_input("Enter the base branch")
  if st.button("Create Pull Request") and repoName != "" and title != "" and headBranch != "" and baseBranch != "":
    repo = user.get_repo(repoName)
    head = f"{user.login}:{headBranch}"
    base = baseBranch
    pr = repo.create_pull(title=title, head=head, base=base)
    st.success(f"Pull request '{pr.title}' created successfully in '{repo.name}'!", icon="🎉")

def removeFiles():
  subprocess.run(["git", "reset"])
  st.toast("All files removed from the staging area successfully.", icon="🎉")

def commitFiles():
  files = st.text_area("Enter the file names to commit (separated by commas)").split(",")
  message = st.text_input("Enter the commit message")
  subprocess.run(["git", "add"] + files.split())
  subprocess.run(["git", "commit", "-m", message])
  st.toast("Files committed successfully!", icon="🎉")

def pushCommits():
  subprocess.run(["git", "push"])
  st.toast("Commits pushed successfully!", icon="🎉")

def restoreAllFiles():
  try:
    subprocess.run(["git", "restore", "--staged", "."])
    subprocess.run(["git", "restore", "."])
    st.toast("All files restored successfully.", icon="🎉")
  except Exception as e:
    st.toast(f"Error occurred while restoring files: {str(e)}", icon="⚠️")

def github():
  st.markdown("## Github Automation 🤖")
  access_token = st.text_input("Enter your Github access token")

  if access_token != "":
    github = Github(access_token)
    user = github.get_user()

    choice = st.selectbox("Select a task", [None, "Create Repository", "List Repositories", "Create Issue", "Create Pull Request", "Remove Files from Staging Area", "Commit Files", "Push Commits", "Restore all files from Staging Area"], key="github_choice")

    if choice == "Create Repository":
      createRepository(user)
    elif choice == "List Repositories":
      listRepositories(user)
    elif choice == "Create Issue":
      createIssue(user)
    elif choice == "Create Pull Request":
      createPullRequest(user)
    elif choice == "Remove Files from Staging Area":
      removeFiles()
    elif choice == "Commit Files":
      commitFiles()
    elif choice == "Push Commits":
      pushCommits()
    elif choice == "Restore all files from Staging Area":
      restoreAllFiles()
    else:
      st.warning("Invalid choice!", icon="⚠️")

  else:
    st.warning("Please enter your Github access token to proceed.", icon="⚠️")
