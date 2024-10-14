(function() {
    var map = window.GeoAdmin.map;  // Access the OpenLayers map instance

    // Define custom OSM layer
    var osmLayer = new OpenLayers.Layer.OSM("High Resolution OSM",
        ["https://a.tile.openstreetmap.org/${z}/${x}/${y}.png",
         "https://b.tile.openstreetmap.org/${z}/${x}/${y}.png",
         "https://c.tile.openstreetmap.org/${z}/${x}/${y}.png"]);

    // Add the custom layer to the map
    map.addLayer(osmLayer);
    map.setBaseLayer(osmLayer);  // Set as the base layer
})();