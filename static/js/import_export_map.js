// https://docs.mapbox.com/help/tutorials/show-changes-over-time/
// https://docs.mapbox.com/help/tutorials/create-interactive-hover-effects-with-mapbox-gl-js/
// Colores para mapas -> https://colorbrewer2.org/
// https://docs.mapbox.com/help/troubleshooting/working-with-large-geojson-data/

let num2mes = {2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo"};

let import_exports_file = "static/data/maps/imports_exports_full.min.geojson";
let covid_info_file = "static/data/maps/covid_choropleth_20m_min_full.geojson";

let map_zoom = 2.9;
let map_min_zoom = 1.5;
let map_max_zoom = 5.5;
let map_center = [16.05, 48];
let circle_opacity = 0.9;
let circle_stroke_width = 1;
let circle_stroke_opacity = 0.65;

let min_circle_size = 8;  // pixels

// 'mapbox://styles/maparla/cklu20mey0a2d17lb8p1mvbk1?optimize=true'
// 'mapbox://styles/maparla/cklv1nya20lej17qookdf496l?optimize=true'
let map_style = 'mapbox://styles/mapbox/light-v10?optimize=true';  // pixels

mapboxgl.accessToken = 'pk.eyJ1IjoibWFwYXJsYSIsImEiOiJja2x1MXNjdXoxMjJ4MnltcDE0cHFybnVnIn0.KScdyNlXfPSbxXmtE-y38Q';

let imports_map = new mapboxgl.Map({
    container: 'map-imports', // container id
    style: map_style, // style URL
    center: map_center, // starting position [lng, lat]
    zoom: map_zoom, // starting zoom
    minZoom: map_min_zoom,
    maxZoom: map_max_zoom,
    attributionControl: false
});


let exports_map = new mapboxgl.Map({
    container: 'map-exports', // container id
    style: map_style, // style URL
    center: map_center, // starting position [lng, lat]
    zoom: map_zoom, // starting zoom
    minZoom: map_min_zoom,
    maxZoom: map_max_zoom,
    attributionControl: false
});

// Create a mapbox popup
const popup = new mapboxgl.Popup({
    closeButton: false,
    closeOnClick: false
});

let start_year = 2018;
let start_month = 1;
let year_importaciones = 2018;
let year_exportaciones = 2018;
let mes_importaciones = 1;
let mes_exportaciones = 1;

// Variable to hold the active country/province on hover
let lastId;

const covid_criteria = "cases"; // cases - deaths


// https://docs.mapbox.com/mapbox-gl-js/style-spec/layers/#circle
imports_map.on('load', function () {


    // Add a layer showing the state polygons.
    imports_map.addLayer({
        id: 'imports-covid-layer',
        type: 'fill',
        source: {
            type: 'geojson',
            data: covid_info_file
        },
        paint: {
            'fill-color': [
                'interpolate',
                ['linear'],
                ['number', ['get', covid_criteria]],
                0,      'rgba(0,   0,   0,   0)',
                5000,   'rgba(255, 237, 160, 0.8)',
                100000, 'rgba(254, 178, 76,  0.8)',
                250000, 'rgba(252, 78,  42,  0.7)',
                500000, 'rgba(128, 0,   38,  0.7)',
            ],
            //'fill-outline-color': 'rgba(200, 100, 240, 1)'
        },
    });

    imports_map.addLayer({
        id: 'imports-layer',
        type: 'circle',
        source: {
            type: 'geojson',
            data: import_exports_file
        },
        paint: {
            // https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#*
            // Vamos a definir el tamaño del circulo como el valor de las importaciones * un factor de escalado
            // tras esto, habrán sitios con importaciones muy pequeñas por lo que definimos
            // un tamaño mínimo de 6 pixeles
            //'circle-radius': ["max", min_circle_size, ["*", ['number', ['get', 'Imports']], 0.00000055]],
            'circle-radius': [
                "interpolate", ["linear"], ["zoom"],
                // cuando el zoom es map_min_zoom, escalamos el circulo por valor importaciones * 0.00000007
                map_min_zoom, ["max", min_circle_size, ["*", ['number', ['get', 'Imports']], 0.00000007]],
                // cuando el zoom es map_max_zoom, escalamos el circulo por valor importaciones * 0.0000012
                map_max_zoom, ["max", min_circle_size, ["*", ['number', ['get', 'Imports']], 0.0000012]]
            ],
            'circle-color': [
                'interpolate',
                ['linear'],
                ['number', ['get', 'Imports']],
                0,        'rgba(242, 240, 247, 1)',
                5240014,  'rgba(203, 201, 226, 1)',
                21720044, 'rgba(158, 154, 200, 1)',
                36200073, 'rgba(106, 81,  163, 1)',
            ],
            'circle-opacity': circle_opacity,
            'circle-stroke-width': circle_stroke_width,
            'circle-stroke-opacity': circle_stroke_opacity
        }
    });

    // Initial state
    imports_map.setFilter('imports-layer',
        ['all',
            ['==', ['number', ['get', 'Year']], start_year],
            ['==', ['number', ['get', 'Month']], start_month],
            ['>', ['number', ['get', 'Imports']], 0],
        ]
    );

    imports_map.setFilter('imports-covid-layer',
        ['all',
            ['==', ['number', ['get', 'Year']], start_year],
            ['==', ['number', ['get', 'Month']], start_month]
        ]
    );

});

// https://docs.mapbox.com/mapbox-gl-js/style-spec/layers/#circle
exports_map.on('load', function () {

    // Add a layer showing the state polygons.
    exports_map.addLayer({
        id: 'exports-covid-layer',
        type: 'fill',
        source: {
            type: 'geojson',
            data: covid_info_file
        },
        paint: {
            'fill-color': [
                'interpolate',
                ['linear'],
                ['number', ['get', covid_criteria]],
                0,      'rgba(0,   0,   0,   0)',
                5000,   'rgba(255, 237, 160, 0.8)',
                100000, 'rgba(254, 178, 76,  0.8)',
                250000, 'rgba(252, 78,  42,  0.7)',
                500000, 'rgba(128, 0,   38,  0.7)',
            ],
            //'fill-outline-color': 'rgba(200, 100, 240, 1)'
        },
    });

    exports_map.addLayer({
        id: 'exports-layer',
        type: 'circle',
        source: {
            type: 'geojson',
            data: import_exports_file
        },
        paint: {
            // https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#*
            // Vamos a definir el tamaño del circulo como el valor de las importaciones * un factor de escalado
            // tras esto, habrán sitios con importaciones muy pequeñas por lo que definimos
            // un tamaño mínimo de 6 pixeles                                                    00000055
            //'circle-radius': ["max", min_circle_size, ["*", ['number', ['get', 'Exports']], 0.0000001]],
            'circle-radius': [
                "interpolate", ["linear"], ["zoom"],
                // cuando el zoom es map_min_zoom, escalamos el circulo por valor importaciones * 0.00000007
                map_min_zoom, ["max", min_circle_size, ["*", ['number', ['get', 'Exports']], 0.000000015]],
                // cuando el zoom es map_max_zoom, escalamos el circulo por valor importaciones * 0.0000012
                map_max_zoom, ["max", min_circle_size, ["*", ['number', ['get', 'Exports']], 0.0000002]]
            ],
            'circle-color': [
                'interpolate',
                ['linear'],
                ['number', ['get', 'Exports']],
                0,        'rgba(242, 240, 247, 1)',
                5240014,  'rgba(203, 201, 226, 1)',
                21720044, 'rgba(158, 154, 200, 1)',
                36200073, 'rgba(106, 81,  163, 1)',
            ],
            'circle-opacity': circle_opacity,
            'circle-stroke-width': circle_stroke_width,
            'circle-stroke-opacity': circle_stroke_opacity
        }
    });

    // Initial state
    exports_map.setFilter('exports-layer',
        ['all',
            ['==', ['number', ['get', 'Year']], start_year],
            ['==', ['number', ['get', 'Month']], start_month],
            ['>', ['number', ['get', 'Exports']], 0],
        ]
    );

    exports_map.setFilter('exports-covid-layer',
        ['all',
            ['==', ['number', ['get', 'Year']], start_year],
            ['==', ['number', ['get', 'Month']], start_month]
        ]
    );

});

function map_export_import_popup(map, e, consulta, covid_layer, transaction_text) {
    // Get the id from the properties
    const id = e.features[0].properties.id;

    // Only if the id are different we process the tooltip
    if (id !== lastId) {
        lastId = id;

        // Change the pointer type on move move
        map.getCanvas().style.cursor = 'pointer';

        // e.features[0]["properties"]
        // {Month: 3, Year: 2019, Imports: 8147589, Exports: 0, Reporter: "Ireland (Eire)"}
        let item = e.features[0]["properties"];

        // Espacio cada tres números para leerlo mejor https://stackoverflow.com/a/32889998/6689880
        const transaction_vals = display_numero(item[consulta]);
        const reporter = item["Reporter"];
        const year = item["Year"];
        const month = item["Month"];
        const countryISO = item["countryISO"].toLowerCase();

        const coordinates = e.features[0].geometry.coordinates.slice();

        //const countryFlagHTML = `<img src="https://www.countryflags.io/${countryISO}/shiny/48.png"></img>`;
        const countryFlagHTML = `<img src="static/icons/country-flags-main/svg/${countryISO}.svg" class="country_flag"></img>`;

        const covid_layer_info = map.querySourceFeatures(covid_layer);
        let covid_length = covid_layer_info.length;
        let covid_info = "";
        for (let i = 0; i < covid_length; i++) {
            let covid_item = covid_layer_info[i]["properties"];
            let covid_item_pais = covid_item["Reporter"];
            let covid_item_year = covid_item["Year"];
            let covid_item_month = covid_item["Month"];
            if( covid_item_pais === reporter && covid_item_year === year && covid_item_month === month ){
                let covid_item_cases = display_numero(covid_item["cases"]);
                let covid_item_deaths = display_numero(covid_item["deaths"]);
                covid_info += `<p class="font-semibold mt-2">Covid</p>`;
                covid_info += `<p>Casos: ${covid_item_cases}</p>`;
                covid_info += `<p>Muertes: ${covid_item_deaths}</p>`;
                break;
            }
        }

        const HTML = `<div class="text-center text-base flex flex-col flex-wrap justify-center items-center p-3">
                          <p class="font-bold border-b-2 border-gray-500">${reporter}</p>
                          <p class="font-semibold mt-2">${transaction_text}</p>
                          <p>${transaction_vals}€</p>
                          ${covid_info}
                          ${countryFlagHTML}
                          </div>`;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
            coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        popup
            .setLngLat(coordinates)
            .setHTML(HTML)
            .addTo(map);
    }
}


$(document).ready(function () {

    $(".toggle-buttons > button").click(function(e){
        $( this ).siblings().removeClass();
        $( this ).removeClass();
        $( this ).siblings().addClass("unselected_choice");
        $( this ).addClass("selected_choice");
    });

    // #######################
    // --------- IMPORTACIONES
    // #######################

    imports_map.on('mousemove', 'imports-layer', function (e) {
        map_export_import_popup(imports_map, e, "Imports", "imports-covid-layer", "Importado");
    });

    imports_map.on('mouseleave', 'imports-layer', function () {
        imports_map.getCanvas().style.cursor = '';
        lastId = undefined;
        popup.remove();
    });


    $("#year_importaciones > button").click(function(e){
        year_importaciones = parseInt($( this ).attr("num-year"));
        // update the map
        imports_map.setFilter('imports-layer',
            ['all',
                ['==', ['number', ['get', 'Year']], year_importaciones],
                ['==', ['number', ['get', 'Month']], mes_importaciones],
                ['>', ['number', ['get', 'Imports']], 0],
            ]
        );

        imports_map.setFilter('imports-covid-layer',
            ['all',
                ['==', ['number', ['get', 'Year']], year_importaciones],
                ['==', ['number', ['get', 'Month']], mes_importaciones],
            ]
        );
    });

    $("#meses_importaciones > button").click(function(e){
        mes_importaciones = parseInt($( this ).attr("num-mes"));
        // update the map
        imports_map.setFilter('imports-layer',
            ['all',
                ['==', ['number', ['get', 'Month']], mes_importaciones],
                ['==', ['number', ['get', 'Year']], year_importaciones],
                ['>', ['number', ['get', 'Imports']], 0],
            ]
        );

        imports_map.setFilter('imports-covid-layer',
            ['all',
                ['==', ['number', ['get', 'Month']], mes_importaciones],
                ['==', ['number', ['get', 'Year']], year_importaciones],
            ]
        );
    });

    // #######################
    // --------- EXPORTACIONES
    // #######################

    exports_map.on('mousemove', 'exports-layer', function (e) {
        map_export_import_popup(exports_map, e, "Exports", "exports-covid-layer", "Exportado");
    });

    exports_map.on('mouseleave', 'exports-layer', function () {
        exports_map.getCanvas().style.cursor = '';
        lastId = undefined;
        popup.remove();
    });

    $("#year_exportaciones > button").click(function(e){
        year_exportaciones = parseInt($( this ).attr("num-year"));
        // update the map
        exports_map.setFilter('exports-layer',
            ['all',
                ['==', ['number', ['get', 'Year']], year_exportaciones],
                ['==', ['number', ['get', 'Month']], mes_exportaciones],
                ['>', ['number', ['get', 'Exports']], 0],
            ]
        );

        exports_map.setFilter('exports-covid-layer',
            ['all',
                ['==', ['number', ['get', 'Year']], year_exportaciones],
                ['==', ['number', ['get', 'Month']], mes_exportaciones],
            ]
        );
    });

    $("#meses_exportaciones > button").click(function(e){
        mes_exportaciones = parseInt($( this ).attr("num-mes"));
        // update the map
        exports_map.setFilter('exports-layer',
            ['all',
                ['==', ['number', ['get', 'Month']], mes_exportaciones],
                ['==', ['number', ['get', 'Year']], year_exportaciones],
                ['>', ['number', ['get', 'Imports']], 0],
            ]
        );

        exports_map.setFilter('exports-covid-layer',
            ['all',
                ['==', ['number', ['get', 'Month']], mes_exportaciones],
                ['==', ['number', ['get', 'Year']], year_exportaciones],
            ]
        );
    });


});
