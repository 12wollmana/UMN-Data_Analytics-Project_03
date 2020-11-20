const serverBaseURL = "http://127.0.0.1:5000";
const apiBaseURL = `${serverBaseURL}/api`;
const apiCurrentVersion = "v1.0";
const nullLabel = "Unknown";

/**
 * Global variables for the state of the page.
 */
let state = {
  pieCharts: [],
  map: {},
  year: "",
  caseMarkers: {},
};

/**
 * HTML elements on the page as d3 objects.
 */
const elements = {
  divLoading: d3.select(".loading"),
  divMap: d3.select("#mapid"),
  divPieChartRace: d3.select(".chart--race"),
  divPieChartSex: d3.select(".chart--sex"),
  divPieChartAge: d3.select(".chart--age"),
  divChartBar: d3.select(".chart--bar"),
  selectYear: d3.select("#selectYear"),
  buttonApplySettings: d3.select("#buttonApplySettings"),
  divChartRowList: d3.selectAll(".row__charts"),
  divChartColRace: d3.select(".col__chart-race"),
  divChartColSex: d3.select(".col__chart-sex"),
  divChartColAge: d3.select(".col__chart-age"),
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
    state.map = makeMap();

    const streetLayer = makeStreetTileLayer();
    streetLayer.addTo(state.map);

    const availableYears = await loadAvailableYears();
    populateSelectYears(availableYears);
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
      const selectedYear = selectedOption;
      await updateCasesByYear(selectedYear);
      state.year = selectedYear;
      showChartRows();
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
function clearData() {
  state.year = "";
  clearCharts();
  state.map.removeLayer(state.caseMarkers);
}

/**
 * Clears all charts.
 */
function clearCharts() {
  let pieCharts = state.pieCharts;
  pieCharts.forEach((chart) => chart.dispose());
  state.pieCharts = [];
}

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
 * Updates the page with cases from a specified year.
 *
 * @param {int} year  /https://jsdoc.app/tags-param.html/
 * The year to load cases from.
 */
async function updateCasesByYear(year) {
  const allCasesByYear = await loadCasesByYear(year);
  console.log(allCasesByYear);

  const caseMarkers = createCaseClustersMarkers(allCasesByYear);
  caseMarkers.addTo(state.map);
  state.caseMarkers = caseMarkers;

  am4core.ready(() => generateAmCharts(allCasesByYear));
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
 * Hides all charts from the page.
 */
function hideChartRows() {
  const chartRowElements = elements.divChartRowList;
  hideElements(chartRowElements);
}

/**
 * Shows all charts on the page.
 */
function showChartRows() {
  const chartRowElements = elements.divChartRowList;
  showElements(chartRowElements);
}

/**
 * Creates a map on the page.
 */
function makeMap() {
  const mapContainer = elements.divMap;
  // Creating Leaflet map object with maker clusters
  var myMap = L.map(mapContainer.node(), {
    center: [44.9778, -93.265],
    zoom: 13,
  });

  return myMap;
}

/**
 * Creates a street tile layer for the map.
 */
function makeStreetTileLayer() {
  // Adding tile layer
  const streetsLayer = L.tileLayer(
    "https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}",
    {
      attribution:
        "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
      tileSize: 512,
      maxZoom: 18,
      zoomOffset: -1,
      id: "mapbox/streets-v11",
      accessToken: API_KEY,
    }
  );

  return streetsLayer;
}

/**
 * Creates a marker cluster layer from a list of cases
 * to display on the map.
 *
 * @param {any[]} cases
 * Cases to create the markers from.
 */
function createCaseClustersMarkers(cases) {
  var markers = L.markerClusterGroup();

  cases.forEach((caseInfo) => {
    const currentCase = caseInfo.case;

    const longitude = currentCase.longitude;
    const latitude = currentCase.latitude;

    if (longitude && latitude) {
      const marker = L.marker([latitude, longitude]);
      marker.bindPopup(createMarkerPopup(currentCase));
      markers.addLayer(marker);
    }
  });

  return markers;
}

/**
 * Creates a marker's popup for display in the map.
 * @param {any} currentCase
 * The current case node to display.
 */
function createMarkerPopup(currentCase) {
  const year = currentCase.year;
  const month = currentCase.month;
  const day = currentCase.day;
  const hour = currentCase.hour;
  const problem = currentCase.problem;
  const caseNumber = currentCase.caseNumber;

  let popupHTML = `
      <h5>
      Case #${caseNumber}
      </h5>
      `;

  let date = nullLabel;
  if (month > 0 && day > 0 && year > 0) {
    date = `${month}/${day}/${year}`;
  }
  popupHTML += createValueLabelHTML(date, "Date");
  popupHTML += createValueLabelHTML(formatHour(hour), "Hour");
  popupHTML += createValueLabelHTML(problem, "Reported Problem");
  popupHTML += createValueLabelHTML(currentCase.isCallTo911, "911 Call");

  const force = currentCase["force"];
  if (!force) {
    return popupHTML;
  }

  popupHTML += `<hr><h6>Police Use of Force</h6>`;
  popupHTML += createValueLabelHTML(force.forceAction, "Action");
  popupHTML += createValueLabelHTML(force.forceCategory, "Category");

  const subject = force["subject"];
  if (!subject) {
    return popupHTML;
  }

  popupHTML += `<hr><h6>Subject</h6>`;
  let age = subject.age;
  if (age < 0) {
    age = nullLabel;
  }
  popupHTML += createValueLabelHTML(age, "Age");
  popupHTML += createValueLabelHTML(subject.sex, "Sex");
  popupHTML += createValueLabelHTML(subject.race, "Race");
  popupHTML += createValueLabelHTML(
    currentCase.primaryOffense,
    "Primary Offense"
  );
  popupHTML += createValueLabelHTML(subject.resistance, "Resistance");
  popupHTML += createValueLabelHTML(subject.wasInjured, "Injured");

  return popupHTML;
}

/**
 * Creates a value-label pair in HTML format.
 *
 * @param {string} value
 * The value to display.
 *
 * @param {string?} label
 * Optional, the label to display.
 */
function createValueLabelHTML(value, label) {
  if (!value) value = nullLabel;

  let popupHTML = "";
  if (label) {
    popupHTML += `${label}: `;
  }
  popupHTML += `<span class="popup__content--value">${value}</span>`;
  popupHTML += "<br>";

  return popupHTML;
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
 * Loads all cases for the specified year from the database.
 *
 * @param {int} year
 * The year to load the cases for.
 */
async function loadCasesByYear(year) {
  const url = `${apiBaseURL}/${apiCurrentVersion}/year/${year}`;
  const allCases = await d3.json(url);
  return allCases;
}

/**
 * Loads all available years from the database.
 */
async function loadAvailableYears() {
  const url = `${apiBaseURL}/${apiCurrentVersion}/year`;
  const response = await d3.json(url);
  return response.availableYears;
}

/**
 * Generates a set of charts using amCharts.
 *
 * https://www.amcharts.com/docs/v4/
 *
 * @param {any[]} cases
 * The cases to generate the charts from.
 */
function generateAmCharts(cases) {
  am4core.useTheme(am4themes_animated);

  // Race Pie Chart
  try {
    let racePieChart = generateRacePieChart(cases);
    showRacePieChartCard();
    state.pieCharts.push(racePieChart);
  } catch (error) {
    if (error instanceof NoDataError) {
      hideRacePieChartCard();
    } else {
      throw error;
    }
  }

  try {
    let sexPieChart = generateSexPieChart(cases);
    showSexPieChartCard();
    state.pieCharts.push(sexPieChart);
  } catch (error) {
    if (error instanceof NoDataError) {
      hideSexPieChartCard();
    } else {
      throw error;
    }
  }

  try {
    let agePieChart = generateAgePieChart(cases);
    showAgePieChartCard();
    state.pieCharts.push(agePieChart);
  } catch (error) {
    if (error instanceof NoDataError) {
      hideAgePieChartCard();
    } else {
      throw error;
    }
  }
}

/**
 * Shows the pie chart card on race.
 */
function showRacePieChartCard() {
  let element = elements.divChartColRace;
  showElements(element);
}

/**
 * Shows the pie chart card on sex.
 */
function showSexPieChartCard() {
  let element = elements.divChartColSex;
  showElements(element);
}

/**
 * Shows the pie chart card on age.
 */
function showAgePieChartCard() {
  let element = elements.divChartColAge;
  showElements(element);
}

/**
 * Hides the pie chart card on race.
 */
function hideRacePieChartCard() {
  let element = elements.divChartColRace;
  hideElements(element);
}

/**
 * Hides the pie chart card on sex.
 */
function hideSexPieChartCard() {
  let element = elements.divChartColSex;
  hideElements(element);
}

/**
 * Hides the pie chart card on sex.
 */

function hideAgePieChartCard() {
  let element = elements.divChartColAge;
  hideElements(element);
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

/**
 * Creates a pie chart using amCharts.
 * This pie chart displays the subject's races.
 *
 * @param {any[]} cases
 * The cases to generate the chart from.
 */
function generateRacePieChart(cases) {
  const chartElement = elements.divPieChartRace;

  const raceData = getRaceData(cases);
  if (raceData.length > 0) {
    var chart = generateAmPieChart(chartElement, "count", "race");
    chart.data = raceData;
  } else {
    throw new NoDataError("No race data.");
  }

  return chart;
}

/**
 * Generates a amChart pie chart.
 *
 * @param {any} parentElement
 * Parent HTML element as a d3 object to append the chart to.
 *
 * @param {string} valueKey
 * Key within the data to bind to the pie value.
 *
 * @param {string} categoryKey
 * Key within the data to bind to the pie category.
 */
function generateAmPieChart(parentElement, valueKey, categoryKey) {
  // Create chart instance
  var chart = am4core.create(parentElement.node(), am4charts.PieChart);

  chart.legend = new am4charts.Legend();
  chart.legend.position = "right";
  chart.legend.scrollable = true;

  // Add and configure Series
  var pieSeries = chart.series.push(new am4charts.PieSeries());
  pieSeries.dataFields.value = valueKey;
  pieSeries.dataFields.category = categoryKey;
  pieSeries.labels.template.disabled = true;
  pieSeries.ticks.template.disabled = true;

  return chart;
}

/**
 * Gets all the race data from a list of cases.
 *
 * @param {any[]} cases
 * The cases to find the race data from.
 */
function getRaceData(cases) {
  let raceCount = {};
  for (let caseInfo of cases) {
    const caseData = caseInfo["case"];

    const force = caseData["force"];
    if (!force) break;

    const subject = force["subject"];
    if (!subject) break;

    race = subject["race"];
    if (race) {
      if (raceCount[race] > 0) {
        raceCount[race]++;
      } else {
        raceCount[race] = 1;
      }
    }
  }

  let raceStats = [];
  Object.entries(raceCount).forEach(([race, count]) => {
    raceStats.push({
      race: race,
      count: count,
    });
  });
  raceStats = raceStats.sort((a, b) => b.count - a.count);
  return raceStats;
}

/**
 * This pie chart displays the subject's sex.
 *
 * @param {any[]} cases
 * The cases to generate the chart from.
 */
function generateSexPieChart(cases) {
  const chartElement = elements.divPieChartSex;

  const sexData = getSexData(cases);
  if (sexData.length > 0) {
    var chart = generateAmPieChart(chartElement, "count", "sex");
    chart.data = sexData;
  } else {
    throw new NoDataError("No sex data.");
  }

  return chart;
}

/**
 * Gets all the sex data from a list of cases.
 *
 * @param {any[]} cases
 * The cases to find the sex data from.
 */
function getSexData(cases) {
  let sexCount = {};
  for (let caseInfo of cases) {
    const caseData = caseInfo["case"];

    const force = caseData["force"];
    if (!force) break;

    const subject = force["subject"];
    if (!subject) break;

    sex = subject["sex"];
    if (sex) {
      if (sexCount[sex] > 0) {
        sexCount[sex]++;
      } else {
        sexCount[sex] = 1;
      }
    }
  }

  let sexStats = [];
  Object.entries(sexCount).forEach(([sex, count]) => {
    sexStats.push({
      sex: sex,
      count: count,
    });
  });
  sexStats = sexStats.sort((a, b) => b.count - a.count);
  return sexStats;
}

/**
 * Creates a pie chart using amCharts.
 * This pie chart displays the subject's age.
 *
 * @param {any[]} cases
 * The cases to generate the chart from.
 */
function generateAgePieChart(cases) {
  const chartElement = elements.divPieChartAge;

  const ageData = getAgeData(cases);
  if (ageData.length > 0) {
    var chart = generateAmPieChart(chartElement, "count", "ageGroup");
    chart.data = ageData;
  } else {
    throw new NoDataError("No age data.");
  }
  return chart;
}

/**
 * Gets all the age data from a list of cases.
 *
 * @param {any[]} cases
 * The cases to find the age data from.
 */
function getAgeData(cases) {
  let ageCount = {};
  for (let caseInfo of cases) {
    const caseData = caseInfo["case"];

    const force = caseData["force"];
    if (!force) break;

    const subject = force["subject"];
    if (!subject) break;

    age = subject["age"];
    if (age < 0) {
      ageGroup = nullLabel;
    } else if (age <= 10) {
      ageGroup = "0-10";
    } else if (age > 10 && age <= 20) {
      ageGroup = "10-20";
    } else if (age > 20 && age <= 30) {
      ageGroup = "20-30";
    } else if (age > 30 && age <= 40) {
      ageGroup = "30-40";
    } else if (age > 40 && age <= 50) {
      ageGroup = "40-50";
    } else if (age > 50 && age <= 60) {
      ageGroup = "50-60";
    } else if (age > 60 && age <= 70) {
      ageGroup = "60-70";
    } else if (age > 70) {
      ageGroup = "70+";
    }

    if (ageCount[ageGroup] > 0) {
      ageCount[ageGroup]++;
    } else {
      ageCount[ageGroup] = 1;
    }
  }

  let ageStats = [];
  Object.entries(ageCount).forEach(([ageGroup, count]) => {
    ageStats.push({
      ageGroup: ageGroup,
      count: count,
    });
  });
  ageStats = ageStats.sort((a, b) => a.ageGroup.localeCompare(b.ageGroup));
  return ageStats;
}
