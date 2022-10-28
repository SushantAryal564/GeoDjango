// zoom control
L.control
  .zoom({
    position: "topright",
  })
  .addTo(map);
// add map scale
L.control.scale({ position: "bottomright" }).addTo(map);
//Full Screen map view
var mapId = document.getElementById("map");
function fullScreenView() {
  if (document.fullscreenElement) {
    document.exitFullscreen();
  } else {
    mapId.requestFullscreen();
  }
}
// Geocoder
L.Control.geocoder().addTo(map);
// print
L.control.browserPrint({ position: "topright" }).addTo(map);
// Zoom to layer
$(".zoomTo").click(function () {
  map.setView([27.756947, 85.330594], 17);
});
