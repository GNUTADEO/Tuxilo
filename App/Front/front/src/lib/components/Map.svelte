<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	type Leaflet = typeof import('leaflet');

	let L: Leaflet;
	let map: any;
	let markers = new Map<number, any>();
	let stationMarker: any = null;
	let embalses: Embalse[] = [];

	interface Embalse {
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
		showNearestStation?: boolean;
	}

	let { selectedEmbalseId, onEmbalsesLoaded, showNearestStation = false }: Props = $props();

	let mapElement: HTMLDivElement;

	onMount(async () => {
		L = await import('leaflet');
		map = L.map(mapElement).setView([4.711, -74.0721], 6);

		// Add OpenStreetMap tile layer
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution:
				'&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			maxZoom: 19
		}).addTo(map);

		// Fetch embalses from API
		try {
			const response = await fetch('http://localhost:8000/public/embalses/');
			const response_geojson = await fetch('http://localhost:8000/public/embalses/geojson');

			const data = await response.json();
			const geojson = await response_geojson.json();

			embalses = data.embalses;

			// Add markers for each embalse
			embalses.forEach((embalse) => {
				const marker = L.marker([embalse.latitud, embalse.longitud])
					.addTo(map)
					.bindPopup(`<b>${embalse.nombre}</b>`);
				markers.set(embalse.id, marker);
			});

			L.geoJSON(geojson, {
				style: { color: '#3388ff', weight: 2, fillOpacity: 0.4 },
				onEachFeature: (feature, layer) => {
					layer.bindPopup(`<b>${feature.properties.nombre}</b><br>
                        Area: ${feature.properties.area_km2} km²`);
				}
			}).addTo(map);

			if (onEmbalsesLoaded) {
				onEmbalsesLoaded(embalses);
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
