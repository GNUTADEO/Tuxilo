<script>
	import Logo from '$lib/assets/Logo.svelte';
</script>

<div class="navbar bg-base-100 shadow-sm">
	<div>
		<a
			class="flex items-center justify-center rounded-full p-1 hover:glass transition"
			href="/"
			aria-label="Go to homepage"
		>
			<div class="w-12 h-12"><Logo /></div>
		</a>
	</div>
	<div class="flex-1"></div>
	<div class="flex-none">
		<ul class="menu menu-horizontal px-2 gap-2 text-sm font-medium">
			<li><a href="/manual">Manual</a></li>
			<li><a href="/contacto">Contacto</a></li>
			<li><a href="https://github.com/GNUTADEO/Tuxilo/blob/main/LICENSE">Licencia</a></li>
		</ul>
	</div>
</div>
