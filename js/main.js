/**
 * Created by dligtenb on 07.05.2015.
 * Main JavaScript file, Initializes map
 */

$(document).ready(function () {
    // Swiss Style background map
    var swissStyle = baseMap.createLayer(
       config.background_maps.swiss_style.url,
       config.background_maps.swiss_style.attribution_url,
       config.background_maps.swiss_style.attribution_text
    );

    // Mapbox Satellite background map
    var mapbox = baseMap.createLayer(
        config.background_maps.mapbox_satellite.url,
        config.background_maps.mapbox_satellite.attribution_url,
        config.background_maps.mapbox_satellite.attribution_text
    );

    // initiate map
    var map = baseMap.create(swissStyle);

    // add base tiles to the map
    var baseMaps={
        "OSM Swiss-Style":swissStyle,
        "Mapbox Satellite":mapbox
    };

    position.setStartPosition(map);
    // initiate position updater
    position.updateCookies(map);

    map.locate();
    map.on('locationfound', function(e){
        L.marker(e.latlng).addTo(map);

        L.ZoomToLocation = mapControls.zoomToLocation(e, map);
        map.addControl(new L.ZoomToLocation());
    });

    L.FitBounds = mapControls.boundControl(baseMap.bounds());
    // add control elements to the map
    L.control.layers(baseMaps).addTo(map);
    map.addControl(new L.FitBounds());

});