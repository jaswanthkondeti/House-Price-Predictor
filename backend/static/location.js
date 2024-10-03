var map;
var marker;

function initMap() {
  map = L.map("map").setView([12.9716, 77.5946], 13); // Default to Bengaluru
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
  }).addTo(map);
}

function updateMap(lat, lon) {
  if (marker) {
    map.removeLayer(marker);
  }
  map.setView([lat, lon], 13);
  marker = L.marker([lat, lon]).addTo(map);
}

function getCoordinates(location) {
  var url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(
    location
  )}`;

  $.getJSON(url, function (data) {
    if (data.length > 0) {
      var lat = data[0].lat;
      var lon = data[0].lon;
      updateMap(lat, lon);
    } else {
      alert("Location not found!");
    }
  }).fail(function () {
    alert("Failed to fetch location data.");
  });
}

function getbath() {
  var ubath = document.getElementsByName("bath");
  for (var i = 0; i < ubath.length; i++) {
    if (ubath[i].checked) {
      return parseInt(ubath[i].value);
    }
  }
  return -1;
}

function getbhk() {
  var ubhk = document.getElementsByName("bhk");
  for (var i = 0; i < ubhk.length; i++) {
    if (ubhk[i].checked) {
      return parseInt(ubhk[i].value);
    }
  }
  return -1;
}

function onClickedEstimatedPrice() {
  console.log("estimate price button clicked");
  var sqft = document.getElementById("usqft");
  var bhk = getbhk();
  var bath = getbath();
  var location = document.getElementById("ulocations");
  var estprice = document.getElementById("ueprice");

  var url = "http://127.0.0.1:3001/predict_homeprice";

  $.ajax({
    url: url,
    type: "POST",
    contentType: "application/json", // Set content type to JSON
    data: JSON.stringify({
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bath,
      location: location.value,
    }),
    success: function (data, status) {
      console.log(data.estimated_price);
      estprice.innerHTML =
        "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
      console.log(status);
    },
    error: function (xhr, status, error) {
      console.log("Request failed:", status, error);
    },
  });

  // Fetch the coordinates of the selected location and update the map
  getCoordinates(location.value);
}

function onPageload() {
  console.log("Document loaded");
  var url = "http://127.0.0.1:3001/get_locations";
  $.get(url, function (data, status) {
    console.log("Got response from the request");
    if (data) {
      var locations = data.locations;
      var ulocations = document.getElementById("ulocations");
      $("#ulocations").empty();
      for (var i in locations) {
        var opt = new Option(locations[i], locations[i]);
        $("#ulocations").append(opt);
      }
    }
  });

  // Initialize the map after loading locations
  initMap();
}

// Ensure everything is set up after the page loads
window.onload = onPageload;
