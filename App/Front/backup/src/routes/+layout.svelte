<script lang="ts">
	import './layout.css';
	import Navbar from '$lib/commons/layout/Navbar.svelte';
	import Footer from '$lib/commons/layout/Footer.svelte';

	let { children } = $props();
</script>

<div class="flex min-h-screen flex-col">
	<!-- Top Navbar -->
	<Navbar />

	<!-- Main content grows and pushes footer -->
	<main class="mx-auto flex w-full max-w-7xl flex-1 p-4">
		{@render children()}
	</main>

	<!-- Footer sticks at bottom -->
	<Footer />
</div>
