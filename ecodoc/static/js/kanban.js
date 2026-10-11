window.addEventListener('load', () => {
    loadTasks();
});

const tasks = [];
const columns = document.querySelectorAll('.tasks');
const taskModal = document.getElementById('task-modal');
const taskNameInput = document.getElementById('task-name');
const taskDescriptionInput = document.getElementById('task-description');
const taskDeadlineInput = document.getElementById('task-deadline');
const closeModalButton = document.querySelector('.close');
const addTaskButton = document.querySelector('.add-task-button');

columns.forEach(column => {
    column.addEventListener('dragover', allowDrop);
    column.addEventListener('drop', (event) => {
        event.preventDefault();
        const taskId = event.dataTransfer.getData('text/plain');
        const taskElement = document.getElementById(taskId);
        const taskName = taskElement.dataset.name; // Get task name from dataset
        moveTaskToColumn(taskName, getColumnIndex(column));
        column.appendChild(taskElement);
    });
});

function allowDrop(event) {
    event.preventDefault();
}

function openModal() {
    taskModal.style.display = 'block';
}

function closeModal() {
    taskModal.style.display = 'none';
    taskNameInput.value = '';  
    taskDescriptionInput.value = '';  
    taskDeadlineInput.value = '';  
  }

function addTask() {
    const taskName = taskNameInput.value;
    const taskDescription= taskDescriptionInput.value;
    const taskDeadline = taskDeadlineInput.value;
    if (taskName.trim() !== '' && taskDeadline.trim() !== '') {
        const task = {
            id: 'task' + tasks.length,
            name: taskName,
            description:taskDescription,
            deadline: taskDeadline
        };
        fetch('/save_task/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify(task)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log('Task saved successfully:', data);
        })
        .catch(error => {
            console.error('Error saving task:', error);
        });
        tasks.push(task);
        const todoColumn = document.getElementById('to-do');
        todoColumn.appendChild(createTaskElement(task));
        closeModal();
    }
}


function getCSRFToken() {
    const cookieValue = document.cookie.match('(^|;)\\s*csrftoken\\s*=\\s*([^;]+)');
    return cookieValue ? cookieValue.pop() : '';
}


function createTaskElement(task) {
    const taskElement = document.createElement('div');
    taskElement.className = 'task';
    taskElement.id = 'task' + tasks.length;
    taskElement.draggable = true;
    taskElement.dataset.name = task.name; // Set task name as a dataset attribute
    taskElement.innerHTML = `
        <strong>${task.name}</strong><br>
        Description: ${task.description}<br>
        Deadline: ${task.deadline}`;
    taskElement.addEventListener('dragstart', (event) => {
        event.dataTransfer.setData('text/plain', event.target.id);
    });
    taskElement.addEventListener('dblclick', () => {
        const confirmation = confirm('Are you sure you want to delete this task?');
        if (confirmation) {
            taskElement.remove();
            taskName=taskElement.dataset.name
            deleteTaskFromFirebase(taskName); // Pass task name for deletion
        }
    });

    return taskElement;
}


function moveTaskToColumn(taskName, columnIndex) {
    const columnId = columns[columnIndex].id;
    const csrftoken = getCSRFToken(); 
    $.ajax({
        url: '/move_task_to_column/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken 
        },
        data: {
            taskName: taskName, 
            newColumn: columnId
        },
        success: function(response) {
            console.log('Task status updated successfully:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error updating task status:', error);
        }
    });
}

// Delete task from Firebase
function deleteTaskFromFirebase(taskName) {
    // Call Django view to delete task from Firebase
    const csrftoken = getCSRFToken();
    $.ajax({
        url: '/delete_task/',
        type: 'POST',
        headers: {
            'X-CSRFToken': csrftoken // Include CSRF token in headers
        },
        data: JSON.stringify({taskName: taskName}),
        contentType: 'application/json',
        success: function(response) {
            console.log('Task deleted successfully:', response);
        },
        error: function(xhr, status, error) {
            console.error('Error deleting task from Firebase:', error);
        }
    });
}


addTaskButton.addEventListener('click', addTask);
closeModalButton.addEventListener('click', closeModal);
window.addEventListener('click', (event) => {
    if (event.target == taskModal) {
        closeModal();
    }
});

function getColumnIndex(column) {
    return Array.from(columns).indexOf(column);
}

function loadTasks() {
    fetch('/load_tasks/')
      .then(response => {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Network response was not ok.');
      })
      .then(data => {
        console.log("Received data:", data);
        data.forEach(task => {
          const columnId = task.status.toLowerCase().replace(/\s/g, '-');
          console.log("Column ID:", columnId);
          const column = document.getElementById(columnId);
          console.log("Column:", column);
          if (column) {
            column.appendChild(createTaskElement(task));
          } else {
            console.error("Column not found:", columnId);
          }
        });
      })
      .catch(error => {
        console.error('Error loading tasks:', error);
      });
  }
