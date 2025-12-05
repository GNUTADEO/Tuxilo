<script lang="ts">
    import { page } from '$app/stores';

    // the param from the URL
    $: file = $page.params.file;

    // build the URL dynamically
    $: iframeUrl = `https://datalake.cuspide.club/cuadernos/${file}.html`;
</script>

<div class="flex flex-1 w-full">
    <iframe
        title={file}
        src={iframeUrl}
        class="w-full h-[80vh] rounded-xl border"
    ></iframe>
</div>
