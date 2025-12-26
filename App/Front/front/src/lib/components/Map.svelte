<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	type Leaflet = typeof import('leaflet');

	let L: Leaflet;
	let map: any;
	let markers = new Map<number, any>();
	let stationMarker: any = null;
	let embalses: Embalse[] = [];
	let estaciones_flow: Flow[] = [];
	let estaciones_rain: Rain[] = [];
	let semestres: Semestre[] = [];
	
	let ICONS: {
      embalse: any;
      flow: any;
      rain: any;
    };

	interface Semestre {
		id: number;
		periodo: string;
	}

	interface Embalse {
		id: number;
		nombre: string;
		latitud: number;
		longitud: number;
	}

	interface Flow {
		id: number;
		nombre: string;
		latitud: number;
		longitud: number;
	}

	interface Rain {
		id: number;
		nombre: string;
		latitud: number;
		longitud: number;
	}

	interface Station {
		station_id: string;
		station_name: string;
		river_name: string;
		latitude: number;
		longitude: number;
		distance_km?: number;
	}

	interface Props {
		selectedEmbalseId?: number | null;
		onEmbalsesLoaded?: (embalses: Embalse[]) => void;
		onSemestresLoaded?: (semestres: Semestre[]) => void;
		showNearestStation?: boolean;
	}

	let { selectedEmbalseId, onEmbalsesLoaded, onSemestresLoaded, showNearestStation = false }: Props = $props();

	let mapElement: HTMLDivElement;

	onMount(async () => {
		L = await import('leaflet');
		ICONS = {
          embalse: new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
          }),
        
          flow: new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
          }),
        
          rain: new L.Icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
            shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41],
          }),
        };
		map = L.map(mapElement).setView([4.711, -74.0721], 6);

		// Add OpenStreetMap tile layer
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution:
				'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			maxZoom: 19
		}).addTo(map);

		// Fetch embalses from API
		try {
			const embalses_points_response = await fetch('http://localhost:8000/public/embalses/points');
			const estaciones_flow_points_response = await fetch('http://localhost:8000/public/estaciones/flow');
			const estaciones_rain_points_response = await fetch('http://localhost:8000/public/estaciones/rain');

			const embalses_polygons_response = await fetch('http://localhost:8000/public/embalses/polygons');
			const semestres_response = await fetch('http://localhost:8000/public/data/semestres');

			const embalses_points_data = await embalses_points_response.json();
			const estaciones_flow_data = await estaciones_flow_points_response.json();
			const estaciones_rain_data = await estaciones_rain_points_response.json();

			const embalses_polygons_data = await embalses_polygons_response.json();
			const semestres_data = await semestres_response.json();

			embalses = embalses_points_data.features;
			estaciones_flow = estaciones_flow_data.features;
			estaciones_rain = estaciones_rain_data.features;
			semestres = semestres_data.features;

			// Add markers for each embalse
			embalses.forEach((embalse) => {
				const marker = L.marker(
					[embalse.latitud, embalse.longitud],
					{ icon: ICONS.embalse }
				).addTo(map)
					.bindPopup(`<b>${embalse.nombre}</b><br>
					    Latitud: ${embalse.latitud}<br>
					    Longitud: ${embalse.longitud}`);
				markers.set(embalse.id, marker);
			});

			estaciones_flow.forEach((estacion_flow) => {
				const marker = L.marker(
					[estacion_flow.latitud, estacion_flow.longitud],
					{ icon: ICONS.flow }
				).addTo(map)
					.bindPopup(`<b>${estacion_flow.nombre}</b><br>
					    Latitud: ${estacion_flow.latitud}<br>
					    Longitud: ${estacion_flow.longitud}`);
				markers.set(estacion_flow.id, marker);
			});

			estaciones_rain.forEach((estacion_rain) => {
				const marker = L.marker(
					[estacion_rain.latitud, estacion_rain.longitud],
					{ icon: ICONS.rain }
				).addTo(map)
					.bindPopup(`<b>${estacion_rain.nombre}</b><br>
					    Latitud: ${estacion_rain.latitud}<br>
					    Longitud: ${estacion_rain.longitud}`);
				markers.set(estacion_rain.id, marker);
			});

			L.geoJSON(embalses_polygons_data, {
				style: { color: '#3388ff', weight: 2, fillOpacity: 0.4 },
				onEachFeature: (feature, layer) => {
					layer.bindPopup(`<b>${feature.properties.nombre}</b><br>
                        Area: ${feature.properties.area_km2} km²`);
				}
			}).addTo(map);

			if (onEmbalsesLoaded) {
				onEmbalsesLoaded(embalses);
			}
			if (onSemestresLoaded) {
				onSemestresLoaded(semestres);
			}
		} catch (error) {
			console.error('Error fetching embalses:', error);
		}
	});

	$effect(() => {
		console.log('Effect triggered:', {
			map: !!map,
			selectedEmbalseId,
			hasMarker: selectedEmbalseId ? markers.has(Number(selectedEmbalseId)) : false,
			markersSize: markers.size,
			embalsesLength: embalses.length
		});

		if (map && selectedEmbalseId && markers.has(Number(selectedEmbalseId))) {
			const embalse = embalses.find((e) => e.id === Number(selectedEmbalseId));
			if (embalse) {
				console.log('Zooming to:', embalse.nombre, embalse.latitud, embalse.longitud);
				map.setView([embalse.latitud, embalse.longitud], 14);
				markers.get(Number(selectedEmbalseId))?.openPopup();
			}

			// Fetch and show nearest station if showNearestStation is true
			if (showNearestStation) {
				fetchNearestStation(Number(selectedEmbalseId));
			} else {
				// Remove station marker if showNearestStation is false
				if (stationMarker && map) {
					map.removeLayer(stationMarker);
					stationMarker = null;
				}
			}
		}
	});

	async function fetchNearestStation(embalseId: number) {
		try {
			const L = await import('leaflet');
			const response = await fetch(`http://localhost:8000/public/stations/nearest/${embalseId}`);
			const data = await response.json();

			if (data.station && map) {
				// Remove previous station marker if exists
				if (stationMarker) {
					map.removeLayer(stationMarker);
				}

				const station: Station = data.station;

				// Create custom icon for station
				const stationIcon = L.divIcon({
					className: 'custom-station-marker',
					html: `<div style="background-color: #ef4444; width: 30px; height: 30px; border-radius: 50%; border: 3px solid white; box-shadow: 0 2px 4px rgba(0,0,0,0.3);"></div>`,
					iconSize: [30, 30],
					iconAnchor: [15, 15]
				});

				stationMarker = L.marker([station.latitude, station.longitude], {
					icon: stationIcon
				}).addTo(map).bindPopup(`<b>${station.station_name}</b><br>
							  River: ${station.river_name}<br>
							  Distance: ${station.distance_km} km`);

				console.log('Nearest station added:', station.station_name);
			}
		} catch (error) {
			console.error('Error fetching nearest station:', error);
		}
	}

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<svelte:head>
	<link
		rel="stylesheet"
		href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
		integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
		crossorigin=""
	/>
</svelte:head>

<div bind:this={mapElement} class="h-full w-full rounded-xl"></div>

<style>
	div {
		min-height: 400px;
	}
</style>
