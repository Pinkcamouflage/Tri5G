var CartoDB_DarkMatter = L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
	attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
	subdomains: 'abcd',
	maxZoom: 20
});

var CartoDB_Positron = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
  subdomains: 'abcd',
  maxZoom: 20
});

var baseLayers = {
  'Dark Matter': CartoDB_DarkMatter,
  'Positron': CartoDB_Positron,
  // Add other base layers if needed
};

var overlayLayers = {};
  
var map = L.map('map',{
  zoomControl:false,
  zoom : 10,
  center : [51.341499, 12.375594],
  layers : [CartoDB_Positron]
});

var layerControl = L.control.layers(baseLayers, overlayLayers, { position: 'bottomright' }).addTo(map);

// Initialize empty layer groups for HexagonMarkers and CircleMarkers
var hexagonMarkerLayerGroup = L.layerGroup();
var circleMarkerLayerGroup = L.layerGroup();

function addLayerToMap(layer, layerName) {
  // Create a unique name for the layer if not provided
  if (!layerName) {
    layerName = 'Layer ' + Object.keys(layerGroup._layers).length;
  }

  // Add the layer to the layer group
  layerGroup.addLayer(layer);

  // Add the layer to the Layer Control with the given name
  var overlayLayers = {};
  overlayLayers[layerName] = layer;
  L.control.layers(null, overlayLayers).addTo(map);

  // Return the name of the added layer
  return layerName;
}

// HANDLING THE WIDGET MOVABILITY/DRAGABILITY
var widgetMap = document.getElementById('widget_map');
var isDraggingWidget = false;
var offsetXWidget = 0;
var offsetYWidget = 0;

var upload_button = document.getElementById('widget_button_upload');
var upload_container = document.getElementById('upload_menu_container');
var isDraggingUpload = false;
var offsetXUpload = 0;
var offsetYUpload = 0;

var database_form_button = document.getElementById('database_menu_button');
var database_connection_container = document.getElementById('database_upload_container');
var isDraggingDatabase = false;
var offsetXDatabase = 0;
var offsetYDatabase = 0;

widgetMap.addEventListener('mousedown', function(e) {
    isDraggingWidget = true;
    offsetXWidget = e.clientX - widgetMap.offsetLeft;
    offsetYWidget = e.clientY - widgetMap.offsetTop;
});

widgetMap.addEventListener('mousemove', function(e) {
    if (isDraggingWidget) {
        widgetMap.style.left = (e.clientX - offsetXWidget) + 'px';
        widgetMap.style.top = (e.clientY - offsetYWidget) + 'px';
    }
});

widgetMap.addEventListener('mouseup', function() {
    isDraggingWidget = false;
});

upload_container.addEventListener('mousedown', function(e) {
    isDraggingUpload = true;
    offsetXUpload = e.clientX - upload_container.offsetLeft;
    offsetYUpload = e.clientY - upload_container.offsetTop;
});

upload_container.addEventListener('mousemove', function(e) {
    if (isDraggingUpload) {
        upload_container.style.left = (e.clientX - offsetXUpload) + 'px';
        upload_container.style.top = (e.clientY - offsetYUpload) + 'px';
    }
});

upload_container.addEventListener('mouseup', function() {
    isDraggingUpload = false;
});

document.addEventListener('mouseup', function() {
    isDraggingDatabase = false;
});

upload_button.addEventListener('click', function() {
    if (upload_container.style.display === 'none') {
        upload_container.style.display = 'flex';
    } else {
        upload_container.style.display = 'none';
    }
});

database_form_button.addEventListener('click', function() {
    if (server_output_formular.style.display === 'none') {
      server_output_formular.style.display = 'flex';
    } else {
      server_output_formular.style.display = 'none';
    }
});

// HANDLING THE WIDGET MOVABILITY/DRAGABILITY END

//Handling the requests to store information within a userbase
function request_collection_storage_to_userbase(event){
  event.preventDefault();
}

function sendDatabaseFormToServer(event) {
  event.preventDefault();

  fetch(databaseConnectUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'), // Make sure to obtain the CSRF token correctly
    },
    body: JSON.stringify({}), // Send an empty JSON object as the request body
  })
    .then((response) => {
      if (response.status === 200) {
        // Handle the successful response here
        response.json().then((data) => {
          handleDatabaseFormResponse(data);
        });
      } else {
        // Handle the error response here
        console.error('Error:', response.statusText);
        
        // Additional error handling code, e.g., handleServerError(response.status);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
      
      // Additional error handling code, e.g., handleFetchError(error);
    });
  
  var outputDiv = document.getElementById('server_output_formular');
  var stepDiv = document.getElementById('step_container3');
  outputDiv.style.display = 'block';
  stepDiv.style.display = 'none';
}

function handleDatabaseFormResponse(response) {
  var outputDiv = document.getElementById('server_output_formular');
  outputDiv.innerHTML = '';
  
  for (var collectionName in response) {
    if (response.hasOwnProperty(collectionName)) {
      var keys = response[collectionName];
      var collectionDiv = createCollectionDiv(collectionName, keys);
      outputDiv.appendChild(collectionDiv);
    }
  }
}

function createCollectionDiv(collectionName, keys) {
  var collectionDiv = document.createElement('div');
  collectionDiv.classList.add('option');
  collectionDiv.setAttribute('title', collectionName);

  // Create a heading for the collection
  var collectionHeading = document.createElement('h3');
  collectionHeading.textContent = collectionName;
  collectionDiv.appendChild(collectionHeading);

  // Create a sublist for the collection keys
  var sublist = document.createElement('ul');
  sublist.classList.add('sublist');
  keys.forEach(function (key) {
      var keyElement = document.createElement('li');
      keyElement.textContent = key;
      sublist.appendChild(keyElement);
  });
  collectionDiv.appendChild(sublist);

  // Create a toggle button
  var toggleButton = createToggleButton(collectionName);
  collectionDiv.appendChild(toggleButton);

  return collectionDiv;
}

function createToggleButton(collectionName){
  var toggleButton = document.createElement('button');
  toggleButton.textContent = '+';
  toggleButton.classList.add('toggle-button', 'green-button');
  toggleButton.setAttribute('data-state', 'green');

  // Add a click event listener to the toggle button
  toggleButton.addEventListener('click', function () {
    toggleButtonClickHandler(toggleButton,collectionName);
  });

  return toggleButton;
}

function handleServerError(statusCode) {
  console.error('Error: ' + statusCode);
}

function createToggleHandler(button,collectionName) {
  return function () {
    const currentState = button.getAttribute('data-state');
    if (currentState === 'green') {
      button.classList.remove('green-button');
      button.classList.add('red-button');
      button.textContent = '-';
      button.setAttribute('data-state', 'red');
      postAddCollection(collectionName);
    } else {
      button.classList.remove('red-button');
      button.classList.add('green-button');
      button.textContent = '+';
      button.setAttribute('data-state', 'green');
      postDeleteCollection(collectionName);
    }
  };
}

// Create an object to manage layers
var layerManager = {
  layers: {},
  addLayer: function (name, layer) {
    this.layers[name] = layer;
    layer.addTo(map);
  },
  removeLayer: function (name) {
    if (this.layers[name]) {
      map.removeLayer(this.layers[name]);
      delete this.layers[name];
    }
  },
};

function postAddCollection(collectionName) {
  fetch(addCollectionUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({ collectionName }),
  })
    .then((response) => {
      if (response.status === 200) {
        // Handle the successful response here
        response.json().then((data) => {
          // Create separate layers for CircleMarkers and HexagonMarkers
          const circleMarkerLayer = L.layerGroup();
          const hexagonMarkerLayer = L.layerGroup();

          // Add CircleMarkers and HexagonMarkers to their respective layers
          renderCircleMarkersOnLayer(circleMarkerLayer, data.geojson.CircleMarkers);
          renderHexagonMarkersOnLayer(hexagonMarkerLayer, data.geojson.HexagonMarkers);

          // Create a new group layer for each collection and add CircleMarker and HexagonMarker layers to it
          const collectionCircleLayer = L.layerGroup([circleMarkerLayer]);
          const collectionHexagonLayer = L.layerGroup([hexagonMarkerLayer]);

          // Add the collection layers to the map
          collectionCircleLayer.addTo(map);
          collectionHexagonLayer.addTo(map);

          // Add the collection layers to the layer manager
          layerManager.addLayer(collectionName + ' CircleMarker', collectionCircleLayer);
          layerManager.addLayer(collectionName + ' HexagonMarker', collectionHexagonLayer);

          // Update the layer control
          layerControl.addOverlay(collectionCircleLayer, collectionName + ' CircleMarker');
          layerControl.addOverlay(collectionHexagonLayer, collectionName + ' HexagonMarker');
        });
      } else {
        // Handle the error response here
        console.error('Error:', response.statusText);
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}

function renderCircleMarkersOnLayer(layer, circle_markers) {
  circle_markers.forEach(function (circleMarker) {
    var location = circleMarker.location;
    var radius = circleMarker.radius || 10;
    var color = circleMarker.color || 'blue';
    var fill = circleMarker.fill || true;
    var fillColor = circleMarker.fill_color || 'blue';
    var fillOpacity = circleMarker.fill_opacity || 0.5;
    var popup = circleMarker.popup || null;

    var marker = L.circle(location, {
      radius: radius,
      color: color,
      fill: fill,
      fillColor: fillColor,
      fillOpacity: fillOpacity,
    });

    if (popup) {
      marker.bindPopup(popup);
    }

    marker.addTo(layer); // Add the marker to the specified layer
  });
}

function renderHexagonMarkersOnLayer(layer, hexagon_markers) {
  hexagon_markers.forEach(function (hexagonMarker) {
    var hexagonVertices = hexagonMarker.hexagon_vertices;
    var color = hexagonMarker.color || 'black';
    var fillColor = hexagonMarker.fill_color || 'blue';
    var fillOpacity = hexagonMarker.fill_opacity || 0.4;
    var hexagonID = hexagonMarker.hex_id;
    var center = hexagonMarker.center;
    var properties = hexagonMarker.properties || {}; // You may need to customize this based on your data

    var polygon = L.polygon(hexagonVertices, {
      color: color,
      fillColor: fillColor,
      fillOpacity: fillOpacity,
    });

    if (Object.keys(properties).length > 0) {
      var popupContent = '<b>Hexagon ID:</b> ' + hexagonID + '<br>';
      for (var key in properties) {
        if (properties.hasOwnProperty(key)) {
          popupContent += `<b>${key}:</b> ${properties[key]}<br>`;
        }
      }
      polygon.bindPopup(popupContent);
    }

    polygon.addTo(layer); // Add the polygon to the specified layer
  });
}

function renderCircleMarkersOnMap(layer, circle_markers) {
  circle_markers.forEach(function (circleMarker) {
    var location = circleMarker.location;
    var radius = circleMarker.radius || 10;
    var color = circleMarker.color || 'blue';
    var fill = circleMarker.fill || true;
    var fillColor = circleMarker.fill_color || 'blue';
    var fillOpacity = circleMarker.fill_opacity || 0.5;
    var popup = circleMarker.popup || null;

    var marker = L.circle(location, {
      radius: radius,
      color: color,
      fill: fill,
      fillColor: fillColor,
      fillOpacity: fillOpacity,
    });

    if (popup) {
      marker.bindPopup(popup);
    }

    marker.addTo(layer); // Add the marker to the specified layer
  });
}

function renderHexagonMarkersOnMap(layer, hexagon_markers) {
  hexagon_markers.forEach(function (hexagonMarker) {
    var hexagonVertices = hexagonMarker.hexagon_vertices;
    var color = hexagonMarker.color || 'black';
    var fillColor = hexagonMarker.fill_color || 'blue';
    var fillOpacity = hexagonMarker.fill_opacity || 0.4;
    var hexagonID = hexagonMarker.hex_id;
    var center = hexagonMarker.center;
    var properties = hexagonMarker.properties || {}; // You may need to customize this based on your data

    var polygon = L.polygon(hexagonVertices, {
      color: color,
      fillColor: fillColor,
      fillOpacity: fillOpacity,
    });

    if (Object.keys(properties).length > 0) {
      var popupContent = '<b>Hexagon ID:</b> ' + hexagonID + '<br>';
      for (var key in properties) {
        if (properties.hasOwnProperty(key)) {
          popupContent += `<b>${key}:</b> ${properties[key]}<br>`;
        }
      }
      polygon.bindPopup(popupContent);
    }

    polygon.addTo(layer); // Add the polygon to the specified layer
  });
}

function postDeleteCollection(collectionName){
  fetch(deleteCollectionUrl,{ //string still needs to be adapted
    method: 'POST',
    headers:{
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify({collectionName})})
    .then((response) => {
      // Handle the response as needed
      if (response.status === 200) {
        // Success
      } else {
        // Error handling
      }
    })
    .catch((error) => {
      // Handle any errors that occur during the fetch.
      console.error('Error:', error);
    });
}

function toggleButtonClickHandler(button,collectionName){
    createToggleHandler(button,collectionName)();
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
}

var connectButton = document.getElementById('database_menu_button');
connectButton.addEventListener('click', sendDatabaseFormToServer);

// HANDLING THE DIFFERENT HTML DIVS FOR THE UPLOAD FORMULA
var stepContainer = document.getElementById('step_container2');


// Function to hide all containers except the one to be shown
function showContainer(containerToShow) {
    if (containerToShow === 'kpi') {
        kpiUploadContainer.style.display = 'block';
        databaseUploadContainer.style.display = 'none';
        fileUploadContainer.style.display = 'none';
        stepContainer.style.display = 'none';
    } else if (containerToShow === 'database') {
        kpiUploadContainer.style.display = 'none';
        databaseUploadContainer.style.display = 'block';
        fileUploadContainer.style.display = 'none';
        stepContainer.style.display = 'none';
    } else if (containerToShow === 'fileUpload') {
        kpiUploadContainer.style.display = 'none';
        databaseUploadContainer.style.display = 'none';
        fileUploadContainer.style.display = 'block';
        stepContainer.style.display = 'none';
    }
    stepContainer.style.display = 'none';
}

// Event listeners for the KPI, Database, and File Upload buttons
var databaseButton = document.getElementById('database_menu_button');
databaseButton.addEventListener('click', function () {
    showContainer('database');
});



































