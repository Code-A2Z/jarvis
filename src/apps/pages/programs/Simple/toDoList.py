import streamlit as st

def toDoList():
  if 'tasks' not in st.session_state:
    st.session_state.tasks = []

  task_title = st.text_input("Task Title", "")
  task_description = st.text_area("Task Description", "")

  if st.button("Add Task"):
    if task_title:
      st.session_state.tasks.append({"title": task_title, "description": task_description, "completed": False})
      st.toast("Task added successfully!", icon="✅")
    else:
      st.toast("Please provide a task title.", icon="🚨")

  if st.session_state.tasks:
    st.divider()
    st.subheader("Your Tasks")

    filter_option = st.selectbox("Filter Tasks", ["All", "Completed", "Pending"])
    filtered_tasks = []

    if filter_option == "Completed":
      filtered_tasks = [task for task in st.session_state.tasks if task["completed"]]
    elif filter_option == "Pending":
      filtered_tasks = [task for task in st.session_state.tasks if not task["completed"]]
    else:
      filtered_tasks = st.session_state.tasks

    for i, task in enumerate(filtered_tasks):
      col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
      with col1:
        task_done = st.checkbox("", value=task["completed"], key=f"task_done_{i}")
      with col2:
        st.write(f"**{task['title']}** - {task['description']}")
      with col3:
        if st.button("❌", key=f"delete_{i}"):
            st.session_state.tasks.remove(task)
            st.rerun()

      if task_done:
        st.session_state.tasks[i]["completed"] = True
      else:
        st.session_state.tasks[i]["completed"] = False

    total_tasks = len(st.session_state.tasks)
    completed_tasks = sum(1 for task in st.session_state.tasks if task["completed"])
    st.progress(completed_tasks / total_tasks)
    st.toast(f"Progress: {completed_tasks}/{total_tasks} tasks completed.", icon="📊")
