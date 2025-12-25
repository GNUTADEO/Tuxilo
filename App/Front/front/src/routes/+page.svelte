<script>
	import Map from '$lib/components/Map.svelte';

	let embalses = $state([]);
	let semestres = $state([]);
	let selectedEmbalseId = $state(null);
	let selectedSemestreId = $state(null);
	let showNearestStation = $state(false);

	function handleLoaded(loadedEmbalses) {
		embalses = loadedEmbalses;
		semestres = loadedSemestres;
	}

	function handleEmbalseChange(event) {
		selectedEmbalseId = event.target.value ? Number(event.target.value) : null;
		console.log('Selected embalse ID:', selectedEmbalseId);
		// Reset when changing embalse
		showNearestStation = false;
	}
	
	function handleSemestreChange(event) {
		selectedSemestreId = event.target.value ? Number(event.target.value) : null;
		console.log('Selected semestre ID:', selectedSemestreId);
		// Reset when changing embalse
		showNearestStation = false;
	}

	function handleCorrer() {
		if (selectedEmbalseId && selectedSemestreId) {
			showNearestStation = true;
			console.log('Showing nearest station for embalse:', selectedEmbalseId);
		} else {
			alert('Por favor seleccione un embalse primero');
		}
	}
</script>

<div class="flex h-full w-full flex-col gap-4">
    
	<div class="w-full">
		<div class="card bg-base-100 h-full w-full p-4 shadow-xl">
			<h1 class="mb-4 text-2xl font-bold">Controles</h1>

			<div class="flex flex-row gap-4">
				<div class="form-control w-1/2">
					<label class="label" for="embalse-1">
						<span class="label-text font-semibold">Embalse</span>
					</label>

					<select
						id="sel-embalse"
						class="select select-bordered w-full"
						onchange={handleEmbalseChange}
					>
						<option value="">Seleccione un embalse</option>
						{#each embalses as embalse (embalse.id)}
							<option value={embalse.id}>{embalse.nombre}</option>
						{/each}
					</select>
				</div>

				<div class="form-control w-1/2">
					<label class="label" for="embalse-1">
						<span class="label-text font-semibold">Semestre</span>
					</label>

					<select
						id="sel-semestre"
						class="select select-bordered w-full"
						onchange={handleSemestreChange}
					>
						<option value="">Seleccione un semestre</option>
<<<<<<< HEAD
						{#each embalses as embalse (embalse.id)}
							<option value={embalse.id}>{embalse.nombre}</option>
=======
						{#each semestre as semestre (semestre.id)}
							<option value={semestre.id}>{semestre.nombre}</option>
>>>>>>> deploy
						{/each}
					</select>
				</div>
			</div>

			<div class="flex flex-row gap-4">
				<button class="btn btn-primary mt-4 w-full" onclick={handleCorrer}>Consultar</button>
			</div>
		</div>
	</div>

	<div class="flex flex-1 flex-col gap-4">
		<div class="card bg-base-100 h-[65vh] p-2 shadow-xl">
			<Map {selectedEmbalseId} onEmbalsesLoaded={handleLoaded} {showNearestStation} />
		</div>
	</div>

	<div class="flex flex-1 flex-col gap-4">
		<div class="card bg-base-100 h-[25vh] p-2 shadow-xl">
			<img class="h-10 w-auto object-contain" src="/working-cat.jpg" alt="Go to dashboard" />
		</div>
	</div>
</div>
