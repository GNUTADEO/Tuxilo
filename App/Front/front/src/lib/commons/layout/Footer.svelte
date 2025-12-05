<script>
	import Logo from '$lib/commons/logos/Logo.svelte';
	import { Github, Mail, Instagram } from '@lucide/svelte';
	const year = new Date().getFullYear();
</script>

<footer class="footer sm:footer-horizontal bg-neutral text-neutral-content p-10">
	<aside>
		<a
			class="flex items-center justify-center rounded-full p-1 hover:glass transition"
			href="/"
			aria-label="Go to homepage"
		>
			<div>
				<div class="w-12 h-12">
					<Logo />
				</div>
			</div>
		</a>
		<p class="mt-2">
			<strong>Explorations from the edge.</strong>
			<br />
			© {year} <a href="https://github.com/spanishHans" target="_blank">SpanishHans</a>
		</p>
	</aside>
	<nav>
		<h6 class="footer-title">Lets talk!</h6>
		<div class="grid grid-flow-col gap-4">
			<a
				href="https://github.com/spanishHans"
				target="_blank"
				rel="noopener"
				aria-label="Github"
			>
				<Github class="w-10 h-10 hover:text-primary rounded-full p-2 hover:glass" />
			</a>
			<a
				href="mailto: juanj.martinezg@utadeo.edu.co"
				aria-label="Mail"
			>
				<Mail class="w-10 h-10 hover:text-primary rounded-full p-2 hover:glass" />
			</a>
			<a
				href="https://www.instagram.com/juanjomarg/"
				target="_blank"
				rel="noopener"
				aria-label="Instagram"
			>
				<Instagram class="w-10 h-10 hover:text-primary rounded-full p-2 hover:glass" />
			</a>
		</div>
	</nav>
</footer>
