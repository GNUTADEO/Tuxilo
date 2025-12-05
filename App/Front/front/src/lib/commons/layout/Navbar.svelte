<script>
	import Logo from '$lib/commons/logos/Logo.svelte';
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
			<li><a href="/">Link</a></li>
			<li>
				<details>
					<summary>Parent</summary>
					<ul class="bg-base-100 rounded-t-none p-2">
						<li><a href="/">Link 1</a></li>
						<li><a href="/">Link 2</a></li>
					</ul>
				</details>
			</li>
		</ul>
	</div>
</div>
