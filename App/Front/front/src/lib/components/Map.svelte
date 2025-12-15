<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import type L from 'leaflet';

	interface Embalse {
		id: number;
		nombre: string;
		latitud: number;
		longitud: number;
	}

	interface Props {
		selectedEmbalseId?: number | null;
		onEmbalsesLoaded?: (embalses: Embalse[]) => void;
	}

	let { selectedEmbalseId, onEmbalsesLoaded }: Props = $props();

	let mapElement: HTMLDivElement;
	let map: L.Map;
	let markers: Map<number, L.Marker> = new Map();
	let embalses: Embalse[] = [];

	onMount(async () => {
		const L = await import('leaflet');
		
		// Initialize the map
		map = L.map(mapElement).setView([4.7110, -74.0721], 6);
		
		// Add OpenStreetMap tile layer
		L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
			maxZoom: 19
		}).addTo(map);
		
		// Fetch embalses from API
		try {
			const response = await fetch('http://localhost:8000/public/embalses/');
			const data = await response.json();
			embalses = data.embalses;
			
			// Add markers for each embalse
			embalses.forEach((embalse) => {
				const marker = L.marker([embalse.latitud, embalse.longitud])
					.addTo(map)
					.bindPopup(`<b>${embalse.nombre}</b>`);
				markers.set(embalse.id, marker);
			});

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
			const embalse = embalses.find(e => e.id === Number(selectedEmbalseId));
			if (embalse) {
				console.log('Zooming to:', embalse.nombre, embalse.latitud, embalse.longitud);
				map.setView([embalse.latitud, embalse.longitud], 14);
				markers.get(Number(selectedEmbalseId))?.openPopup();
			}
		}
	});

	onDestroy(() => {
		if (map) {
			map.remove();
		}
	});
</script>

<svelte:head>
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
		integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
		crossorigin=""/>
</svelte:head>

<div bind:this={mapElement} class="w-full h-full rounded-xl"></div>

<style>
	div {
		min-height: 400px;
	}
</style>
