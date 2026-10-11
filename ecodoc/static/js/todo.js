document.addEventListener("DOMContentLoaded", function () {
    const taskInput = document.getElementById("taskInput");
    const taskList = document.getElementById("taskList");

    // Load tasks from the server
    loadTasks();

    function addTask() {
        const taskText = taskInput.value.trim();
        if (taskText !== "") {
            addTaskToDOM(taskText);
            addTaskToDatabase(taskText); // Call Django view to add task to database
            taskInput.value = "";
        }
    }

    function addTaskToDOM(taskText) {
        const li = document.createElement("li");
        li.innerHTML = `
            <span>${taskText}</span>
            <button class="deleteTask">Delete</button>
        `;
        taskList.appendChild(li);

        const deleteButton = li.querySelector(".deleteTask");
        deleteButton.addEventListener("click", function () {
            li.remove();
            deleteTaskFromDatabase(taskText); // Call Django view to delete task from database
        });
    }

    function loadTasks() {
        fetch('/load_tasks_todo/')
            .then(response => {
                if (response.ok) {
                    return response.json();
                    
                }
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                data.tasks.forEach(taskText => {
                    addTaskToDOM(taskText);
                });
            })
            .catch(error => {
                console.error('Error loading tasks:', error);
            });
    }

    function addTaskToDatabase(taskText) {
        fetch('/add_task_todo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ taskText: taskText })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
        })
        .catch(error => {
            console.error('Error adding task:', error);
        });
    }

    function deleteTaskFromDatabase(taskText) {
        fetch('/delete_tasks_todo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ taskText: taskText })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
        })
        .catch(error => {
            console.error('Error deleting task:', error);
        });
    }

    function getCSRFToken() {
        const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
        return cookieValue ? cookieValue.pop() : '';
    }

    const addTaskButton = document.getElementById("addTask");
    addTaskButton.addEventListener("click", addTask);
});
