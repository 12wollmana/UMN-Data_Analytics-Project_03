const serverBaseURL = "http://127.0.0.1:5000";
const nullLabel = "Unknown";

/**
 * Global variables for the state of the page.
 */
let state = {};

/**
 * HTML elements on the page as d3 objects.
 */
const elements = {
    divLoading: d3.select(".loading"),
    selectYear: d3.select("#selectYear"),
    buttonApplySettings: d3.select("#buttonApplySettings"),
    colError: d3.select(".col__error"),
    divErrorMessage: d3.select(".alert-danger"),
};

/**
 * This error will be thrown when
 * there is no data to make a chart out of.
 */
class NoDataError extends Error {
    /**
     * Creates an error for when there's no data
     * to make a chart from.
     * @param {string} message
     * Message to display.
     */
    constructor(message) {
        super(message);
        this.name = "NoDataError";
    }
}

/**
 * Sets a sleep timer.
 *
 * From: https://stackoverflow.com/questions/33289726/combination-of-async-function-await-settimeout
 *
 * @param {int} m Time in millseconds
 */
const sleep = (m) => new Promise((r) => setTimeout(r, m));

/**
 * Main application logic.
 */
async function main() {
    await showLoading();
    bindHandlers();

    try {
    } catch (error) {
        showError("Could not initialize page.");
        throw error;
    } finally {
        hideLoading();
    }
}

main();

/**
 * Binds all handlers to their elements.
 */
function bindHandlers() {
    elements.buttonApplySettings.on("click", onApplySettings);
}

/**
 * Handler for applying settings.
 */
async function onApplySettings() {
    d3.event.preventDefault();

    await showLoading();
    hideError();
    hideChartRows();
    clearData();

    try {
        const selectElement = elements.selectYear;
        const selectedOption = selectElement.property("value");

        if (selectedOption != "None") {
        }
    } catch (error) {
        showError("Could not apply Settings.");
        throw error;
    } finally {
        hideLoading();
    }
}
/**
 * Shows an error on the page with a message.
 * @param {string} message
 * Message to show.
 */
function showError(message) {
    const columnElement = elements.colError;
    showElements(columnElement);

    const messageElement = elements.divErrorMessage;
    messageElement.text(message);
}

/**
 * Hides any error message on the page.
 */
function hideError() {
    const columnElement = elements.colError;
    hideElements(columnElement);

    const messageElement = elements.divErrorMessage;
    messageElement.text("");
}

/**
 * Clears data from page.
 */
function clearData() {}

/**
 * Populates the select years element with options.
 *
 * @param {string[]} options
 * The options to add to the element.
 */
function populateSelectYears(options) {
    const selectElement = elements.selectYear;
    options.forEach((option) => {
        const optionElement = selectElement.append("option");
        optionElement.text(option);
    });
}

/**
 * Hides the loading screen from the page.
 */
function hideLoading() {
    const loadingElement = elements.divLoading;
    hideElements(loadingElement);
}

/**
 * Shows the loading screen on the page.
 */
async function showLoading() {
    const loadingElement = elements.divLoading;
    showElements(loadingElement);
    await sleep(300); // Wait for cover-up animation to finish
}

/**
 * Formats an hour for display.
 *
 * @param {int} hour
 * The hour to format.
 */
function formatHour(hour) {
    if (hour < 0) return nullLabel;

    let isPM = hour >= 12;
    let hourDisplay = hour % 12;
    if (hourDisplay === 0) {
        hourDisplay = 12;
    }

    return `${hourDisplay}${isPM ? "PM" : "AM"}`;
}

/**
 * Hide one or more elements on the page.
 * @param {any} elements
 * Elements to hide as a d3 object.
 */
function hideElements(elements) {
    elements.classed("hidden", true);
}

/**
 * Shows one or more elements on the page.
 * @param {any} elements
 * Elements to hide as a d3 object.
 */
function showElements(elements) {
    elements.classed("hidden", false);
}
