/**
 * Yellow World — client-side JavaScript.
 */

/**
 * Return the greeting string.
 * Pure function kept separate for testability.
 * @returns {string}
 */
function getGreeting() {
  return "Yellow World";
}

/**
 * Initialise the application.
 * Adds a 'loaded' CSS class to the body element.
 */
function initApp() {
  document.body.classList.add("loaded");
  console.log("Yellow World app initialised");
}

document.addEventListener("DOMContentLoaded", initApp);
