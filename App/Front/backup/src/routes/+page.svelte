<script>
    import Map from '$lib/components/Map.svelte';
    const seriesUrl = "$lib/assets/working-cat.jpg";

    let embalses = $state([]);
    let selectedEmbalseId = $state(null);
    let showNearestStation = $state(false);

    function handleEmbalsesLoaded(loadedEmbalses) {
        embalses = loadedEmbalses;
    }

    function handleEmbalseChange(event) {
        selectedEmbalseId = event.target.value ? Number(event.target.value) : null;
        console.log('Selected embalse ID:', selectedEmbalseId);
        // Reset when changing embalse
        showNearestStation = false;
    }

    function handleCorrer() {
        if (selectedEmbalseId) {
            showNearestStation = true;
            console.log('Showing nearest station for embalse:', selectedEmbalseId);
        } else {
            alert('Por favor seleccione un embalse primero');
        }
    }
</script>

<div class="flex flex-col h-full w-full gap-4">

    <!-- LEFT SIDEBAR -->
    <div class="w-full ">
        <div class="card bg-base-100 shadow-xl h-full w-full p-4">

            <h1 class="text-2xl font-bold mb-4">Controles</h1>

            <div class="flex flex-row gap-4">

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">Embalse</span>
                    </label>
                    <select class="select select-bordered w-full" onchange={handleEmbalseChange}>
                        <option value="">Seleccione un embalse</option>
                        {#each embalses as embalse}
                            <option value={embalse.id}>{embalse.nombre}</option>
                        {/each}
                    </select>
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">Embalse</span>
                    </label>
                    <select class="select select-bordered w-full" onchange={handleEmbalseChange}>
                        <option value="">Seleccione un embalse</option>
                        {#each embalses as embalse}
                            <option value={embalse.id}>{embalse.nombre}</option>
                        {/each}
                    </select>
                </div>

            </div>

            <div class="flex flex-row gap-4">
                <button class="btn btn-primary mt-4 w-full" onclick={handleCorrer}>Consultar</button>
            </div>
        </div>
    </div>


    <!-- RIGHT COLUMN (MAP + SERIES) -->
    <div class="flex-1 flex flex-col gap-4">

        <!-- BIG MAP -->
        <div class="card bg-base-100 shadow-xl p-2 h-[65vh]">
            <Map selectedEmbalseId={selectedEmbalseId} onEmbalsesLoaded={handleEmbalsesLoaded} showNearestStation={showNearestStation} />
        </div>

    </div>
    
    <div class="flex-1 flex flex-col gap-4">

        <!-- SMALL TIMESERIES -->
        <div class="card bg-base-100 shadow-xl p-2 h-[25vh]">
            <enhanced:img
              class="object-contain w-auto h-10"
              src="$lib/images/working-cat.jpg"
              alt="Go to dashboard"
            />
        </div>

    </div>
</div>
