/**
 * Task Manager – Frontend Application
 *
 * A vanilla JavaScript single-page application that communicates with the
 * Task Manager REST API.  Supports listing tasks, creating new tasks, and
 * marking tasks as done.
 *
 * The API base URL defaults to http://localhost:8000 and can be overridden
 * by setting `window.TASK_API_BASE_URL` before this script loads.
 */

(function () {
    "use strict";

    // -----------------------------------------------------------------------
    // Configuration
    // -----------------------------------------------------------------------

    /** @type {string} Base URL of the Task Manager API (no trailing slash). */
    const BASE_URL = (window.TASK_API_BASE_URL || "http://localhost:8000").replace(
        /\/+$/,
        ""
    );

    // -----------------------------------------------------------------------
    // DOM references
    // -----------------------------------------------------------------------

    const taskForm = document.getElementById("task-form");
    const titleInput = document.getElementById("task-title");
    const descriptionInput = document.getElementById("task-description");
    const submitBtn = document.getElementById("submit-btn");
    const taskListEl = document.getElementById("task-list");
    const loadingIndicator = document.getElementById("loading-indicator");
    const emptyMessage = document.getElementById("empty-message");
    const errorBanner = document.getElementById("error-banner");
    const errorMessage = document.getElementById("error-message");
    const errorClose = document.getElementById("error-close");

    // -----------------------------------------------------------------------
    // Error handling
    // -----------------------------------------------------------------------

    /**
     * Display an error message to the user via the error banner.
     * @param {string} message - Human-readable error text.
     */
    function showError(message) {
        errorMessage.textContent = message;
        errorBanner.hidden = false;
    }

    /** Hide the error banner. */
    function hideError() {
        errorBanner.hidden = true;
        errorMessage.textContent = "";
    }

    errorClose.addEventListener("click", hideError);

    // -----------------------------------------------------------------------
    // API helpers
    // -----------------------------------------------------------------------

    /**
     * Fetch all tasks from the API.
     * @returns {Promise<Array<Object>>} Array of task objects.
     */
    async function fetchTasks() {
        const response = await fetch(BASE_URL + "/tasks", {
            method: "GET",
            headers: { "Accept": "application/json" },
        });

        if (!response.ok) {
            const detail = await extractErrorDetail(response);
            throw new Error(detail || "Failed to fetch tasks (" + response.status + ")");
        }

        return response.json();
    }

    /**
     * Create a new task via the API.
     * @param {string} title - Task title.
     * @param {string} description - Task description.
     * @returns {Promise<Object>} The created task object.
     */
    async function createTask(title, description) {
        const response = await fetch(BASE_URL + "/tasks", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({ title: title, description: description }),
        });

        if (!response.ok) {
            const detail = await extractErrorDetail(response);
            throw new Error(detail || "Failed to create task (" + response.status + ")");
        }

        return response.json();
    }

    /**
     * Mark a task as done via the API.
     * @param {number} taskId - The task's ID.
     * @returns {Promise<Object>} The updated task object.
     */
    async function markTaskDone(taskId) {
        const response = await fetch(BASE_URL + "/tasks/" + taskId, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({ status: "done" }),
        });

        if (!response.ok) {
            const detail = await extractErrorDetail(response);
            throw new Error(detail || "Failed to update task (" + response.status + ")");
        }

        return response.json();
    }

    /**
     * Try to extract a human-readable error message from an API error response.
     * @param {Response} response - The fetch Response object.
     * @returns {Promise<string|null>} Extracted detail or null.
     */
    async function extractErrorDetail(response) {
        try {
            const body = await response.json();
            if (typeof body.detail === "string") {
                return body.detail;
            }
            if (Array.isArray(body.detail)) {
                return body.detail
                    .map(function (err) {
                        return err.msg || JSON.stringify(err);
                    })
                    .join("; ");
            }
            return null;
        } catch (_e) {
            return null;
        }
    }

    // -----------------------------------------------------------------------
    // Rendering
    // -----------------------------------------------------------------------

    /**
     * Escape HTML special characters to prevent XSS.
     * @param {string} text - Raw text to escape.
     * @returns {string} HTML-safe string.
     */
    function escapeHtml(text) {
        var div = document.createElement("div");
        div.appendChild(document.createTextNode(text));
        return div.innerHTML;
    }

    /**
     * Render an array of task objects into the task list element.
     * @param {Array<Object>} tasks - Array of task objects from the API.
     */
    function renderTasks(tasks) {
        taskListEl.innerHTML = "";

        if (tasks.length === 0) {
            emptyMessage.hidden = false;
            return;
        }

        emptyMessage.hidden = true;

        tasks.forEach(function (task) {
            var li = document.createElement("li");
            if (task.status === "done") {
                li.classList.add("task-done");
            }

            // Task info container
            var infoDiv = document.createElement("div");
            infoDiv.className = "task-info";

            var titleSpan = document.createElement("div");
            titleSpan.className = "task-title";
            titleSpan.textContent = task.title;
            infoDiv.appendChild(titleSpan);

            if (task.description) {
                var descDiv = document.createElement("div");
                descDiv.className = "task-description";
                descDiv.textContent = task.description;
                infoDiv.appendChild(descDiv);
            }

            // Meta row: status badge
            var metaDiv = document.createElement("div");
            metaDiv.className = "task-meta";

            var badge = document.createElement("span");
            badge.className = "badge badge-" + escapeHtml(task.status);
            badge.textContent = task.status;
            metaDiv.appendChild(badge);

            infoDiv.appendChild(metaDiv);
            li.appendChild(infoDiv);

            // Actions column
            var actionsDiv = document.createElement("div");
            actionsDiv.className = "task-actions";

            if (task.status !== "done") {
                var doneBtn = document.createElement("button");
                doneBtn.className = "btn btn-done";
                doneBtn.textContent = "Mark Done";
                doneBtn.setAttribute("data-task-id", task.id);
                doneBtn.addEventListener("click", handleMarkDone);
                actionsDiv.appendChild(doneBtn);
            }

            li.appendChild(actionsDiv);
            taskListEl.appendChild(li);
        });
    }

    // -----------------------------------------------------------------------
    // Event handlers
    // -----------------------------------------------------------------------

    /**
     * Load and render all tasks from the API.
     */
    async function loadTasks() {
        loadingIndicator.hidden = false;
        emptyMessage.hidden = true;
        taskListEl.innerHTML = "";

        try {
            var tasks = await fetchTasks();
            renderTasks(tasks);
        } catch (err) {
            showError("Could not load tasks: " + err.message);
        } finally {
            loadingIndicator.hidden = true;
        }
    }

    /**
     * Handle form submission to create a new task.
     * @param {Event} event - The submit event.
     */
    async function handleFormSubmit(event) {
        event.preventDefault();
        hideError();

        var title = titleInput.value.trim();
        var description = descriptionInput.value.trim();

        if (!title) {
            showError("Task title is required.");
            titleInput.focus();
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = "Adding…";

        try {
            await createTask(title, description);
            titleInput.value = "";
            descriptionInput.value = "";
            await loadTasks();
        } catch (err) {
            showError("Could not create task: " + err.message);
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = "Add Task";
        }
    }

    /**
     * Handle click on a "Mark Done" button.
     * @param {Event} event - The click event.
     */
    async function handleMarkDone(event) {
        hideError();

        var button = event.currentTarget;
        var taskId = parseInt(button.getAttribute("data-task-id"), 10);

        button.disabled = true;
        button.textContent = "Updating…";

        try {
            await markTaskDone(taskId);
            await loadTasks();
        } catch (err) {
            showError("Could not update task: " + err.message);
            button.disabled = false;
            button.textContent = "Mark Done";
        }
    }

    // -----------------------------------------------------------------------
    // Initialisation
    // -----------------------------------------------------------------------

    taskForm.addEventListener("submit", handleFormSubmit);

    // Load tasks on page load
    loadTasks();
})();
