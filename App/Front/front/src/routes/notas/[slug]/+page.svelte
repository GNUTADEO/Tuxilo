<script lang="ts">
    import { marked } from 'marked';

    export let data: {
        raw: string;
    };

    const html = marked.parse(data.raw);
</script>

<article class="prose mx-auto my-12 w-full max-w-4xl">
    {@html html}
</article>
