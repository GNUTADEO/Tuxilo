<script>
    import Map from '$lib/components/Map.svelte';
    const seriesUrl = "/assets/working-cat.jpg";
    
    let embalses = $state([]);
    let selectedEmbalseId = $state(null);
    
    function handleEmbalsesLoaded(loadedEmbalses) {
        embalses = loadedEmbalses;
    }
    
    function handleEmbalseChange(event) {
        selectedEmbalseId = event.target.value ? Number(event.target.value) : null;
        console.log('Selected embalse ID:', selectedEmbalseId);
    }
</script>

<div class="flex h-full w-full gap-4">

    <!-- LEFT SIDEBAR -->
    <div class="w-1/3 max-w-sm">
        <div class="card bg-base-100 shadow-xl h-full p-4">

            <h1 class="text-2xl font-bold mb-4">Controles</h1>

            <div class="flex flex-col gap-4">

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
                        <span class="label-text font-semibold">ENSO</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">NAO</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">SOI</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">OPP</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">ONI</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <div class="form-control">
                    <label class="label">
                        <span class="label-text font-semibold">TSM</span>
                    </label>
                    <input type="number" class="input input-bordered w-full" placeholder="0.0" />
                </div>

                <button class="btn btn-primary mt-4 w-full">Correr</button>

            </div>
        </div>
    </div>


    <!-- RIGHT COLUMN (MAP + SERIES) -->
    <div class="flex-1 flex flex-col gap-4">

        <!-- BIG MAP -->
        <div class="card bg-base-100 shadow-xl p-2 h-[65vh]">
            <Map selectedEmbalseId={selectedEmbalseId} onEmbalsesLoaded={handleEmbalsesLoaded} />
        </div>

        <!-- SMALL TIMESERIES -->
        <div class="card bg-base-100 shadow-xl p-2 h-[25vh]">
            <iframe
                src={seriesUrl}
                title="timeseries"
                class="w-full h-full rounded-xl"
            ></iframe>
        </div>

    </div>
</div>
