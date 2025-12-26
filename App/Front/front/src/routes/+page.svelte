<script>
	import Map from '$lib/components/Map.svelte';

	let embalses = $state([]);
	let semestres = $state([]);
	let selectedEmbalseId = $state(null);
	let selectedSemestreId = $state(null);
	let showNearestStation = $state(false);
	let graphHtmlFile = $state('ACO_21160040_21160040.html');
	let qProyectadoData = $state(null);
	let selectedPeriodo = $state(null);
	let mediaValue = $state(null);
	let comparisonResult = $state(null);

	// Mapping of embalse IDs to their corresponding HTML graph files (rain stations)
	const embalseGraphMapping = {
		66: 'ESCUELA_TENA_35060100_35060100.html',       // Embalse Del Guavio -> ESCUELA TENA
		60: 'GUANQUICA_21201180_21201180.html',         // EMBALSE DEL NEUSA -> GUANQUICA
		46: 'ACO_21160040_21160040.html',               // Embalse del Río Prado -> ACO
		58: 'POTRERO_LARGO_21200780_21200780.html',     // Embalse de Tomine -> POTRERO LARGO
		35: 'EL_PENOL_23085110_23085110.html',          // Embalse El Peñol (Guatape) -> EL PENOL
		71: 'NORCASIA_RADIO_23050250_23050250.html',    // Embalse La Miel -> NORCASIA RADIO
		32: 'SALVAJINA_LA_26030150_26030150.html',      // Embalse La Salvajina -> LA SALVAJINA
		59: 'PISCIS_21200620_21200620.html',            // Emblase del Sisga -> PISCIS
		67: 'YAGUARA_21080030_21080030.html',           // Represa de Betania -> YAGUARA
		48: 'LA_UNION_21201320_21201320.html',          // Represa del Muña -> LA UNION
		55: 'ISLA_DEL_SANTUARIO_24015120_24015120.html' // Represa Gachaneca -> ISLA DEL SANTUARIO
	};

	function handleLoadedEmbalses(loadedEmbalses) {
		embalses = loadedEmbalses;
	}

	function handleLoadedSemestres(loadedSemestres) {
		semestres = loadedSemestres.slice(0, 10);
	}

	function handleEmbalseChange(event) {
		selectedEmbalseId = event.target.value ? Number(event.target.value) : null;
		console.log('Selected embalse ID:', selectedEmbalseId);
		
		// Update graph HTML file based on selected embalse
		if (selectedEmbalseId && embalseGraphMapping[selectedEmbalseId]) {
			graphHtmlFile = embalseGraphMapping[selectedEmbalseId];
			console.log('Updated graph file:', graphHtmlFile);
		}
		
		// Reset when changing embalse
		showNearestStation = false;
		comparisonResult = null;
		qProyectadoData = null;
		mediaValue = null;
	}

	function handleSemestreChange(event) {
		selectedSemestreId = event.target.value ? Number(event.target.value) : null;
		
		// Find the periodo string for the selected semestre
		if (selectedSemestreId) {
			const selectedSemestre = semestres.find(s => s.id === selectedSemestreId);
			selectedPeriodo = selectedSemestre ? selectedSemestre.periodo : null;
			console.log('Selected semestre ID:', selectedSemestreId, 'Periodo:', selectedPeriodo);
		}
		
		// Reset when changing semestre
		showNearestStation = false;
		comparisonResult = null;
		qProyectadoData = null;
		mediaValue = null;
	}

	async function handleCorrer() {
		if (selectedEmbalseId && selectedSemestreId && selectedPeriodo) {
			showNearestStation = true;
			console.log('Fetching q_proyectado for embalse:', selectedEmbalseId, 'and periodo:', selectedPeriodo);
			
			try {
				// Fetch q_proyectado data
				const qProyectadoResponse = await fetch(`http://localhost:8000/public/data/q_proyectado/${selectedEmbalseId}/${selectedPeriodo}`);
				
				if (!qProyectadoResponse.ok) {
					throw new Error(`Error: ${qProyectadoResponse.status} ${qProyectadoResponse.statusText}`);
				}
				
				qProyectadoData = await qProyectadoResponse.json();
				console.log('Q Proyectado Data:', qProyectadoData);
				
				// Fetch Media value from the graph HTML file
				const mediaResponse = await fetch(`http://localhost:8000/public/data/media/${graphHtmlFile}`);
				
				if (!mediaResponse.ok) {
					throw new Error(`Error fetching media: ${mediaResponse.status} ${mediaResponse.statusText}`);
				}
				
				const mediaData = await mediaResponse.json();
				mediaValue = mediaData.media;
				console.log('Media Value:', mediaValue);
				
				// Compare q_proyectado with media
				if (qProyectadoData.q_proyectado > mediaValue) {
					comparisonResult = 'above'; // Green
				} else {
					comparisonResult = 'below'; // Red
				}
				
				console.log('Comparison Result:', comparisonResult, `(${qProyectadoData.q_proyectado} vs ${mediaValue})`);
				
			} catch (error) {
				console.error('Error fetching data:', error);
				alert('Error al consultar los datos: ' + error.message);
			}
		} else {
			alert('Por favor seleccione un embalse y un semestre primero.');
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
						{#each semestres as semestre (semestre.id)}
							<option value={semestre.id}>{semestre.periodo}</option>
						{/each}
					</select>
				</div>
			</div>

			<div class="flex flex-row gap-4">
				<button class="btn btn-primary mt-4 w-full" onclick={handleCorrer}>Consultar</button>
			</div>
		</div>

		<div class="card bg-base-100 h-[45vh] w-full p-4 shadow-xl">
    		<Map
                {selectedEmbalseId}
                onEmbalsesLoaded={(e) => embalses = e}
                onSemestresLoaded={(s) => semestres = s}
                {showNearestStation}
                {comparisonResult}
            />
		</div>

		<div class="card bg-base-100 w-full p-4 shadow-xl">
            <iframe
                src="/graphs/{graphHtmlFile}"
                class="w-full border-0 rounded-xl"
                style="min-height: 620px"
                title="Graph for selected embalse"
            ></iframe>
        </div>


	</div>
</div>
