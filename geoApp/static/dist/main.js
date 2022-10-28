var map = L.map("map", {
  zoomControl: false,
  attributionControl: false,
}).setView([27.619602336079257, 85.53852145850216], 17);
L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    attribution:
      "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
  }
).addTo(map);
var mylocation = L.marker([27.756947, 85.330594]).addTo(map).openPopup();

var OpenTopoMap = L.tileLayer(
  "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
  {
    maxZoom: 17,
    attribution:
      'Map data: &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://viewfinderpanoramas.org">SRTM</a> | Map style: &copy; <a href="https://opentopomap.org">OpenTopoMap</a> (<a href="https://creativecommons.org/licenses/by-sa/3.0/">CC-BY-SA</a>)',
  }
);

var GrayMap = L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}",
  {
    attribution: "Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ",
    maxZoom: 16,
  }
);
var Carto = L.tileLayer(
  "https://{s}.basemaps.cartocdn.com/rastertiles/voyager_labels_under/{z}/{x}/{y}{r}.png",
  {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: "abcd",
    maxZoom: 20,
  }
);
var WorldImagery = L.tileLayer(
  "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
  {
    attribution:
      "Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community",
  }
);

// Map Coordinate display
map.on("mousemove", function (e) {
  $(".coordinate").html(`Lat:${e.latlng.lat} Lng:${e.latlng.lng}`);
});
// web project

// Load Json data Marker
var markers = L.markerClusterGroup();
var marker = L.geoJSON(data, {
  onEachFeature: function (feature, layer) {
    layer.bindPopup(feature.properties.name);
  },
});
marker.addTo(markers);
markers.addTo(map);

// Leaflet Layer control
var baseMaps = {
  Topo: OpenTopoMap,
  Grey: GrayMap,
  Carto: Carto,
  Imagery: WorldImagery,
};
// var overlayMaps = {
//   "GeoJson Marker": markers,
//   mylocation: mylocation,
// };
// L.control
//   .layers(baseMaps, overlayMaps, { collapsed: false, position: "topleft" })
//   .addTo(map);
