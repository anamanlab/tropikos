import { bindings, defineConfig } from "cf/config";

export default defineConfig({
	worker: {
		name: "tropikos-arquitetos",
		compatibilityDate: "2026-10-22",
		entrypoint: "./src/worker.ts",
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "404-page",
			// Run the Worker first for every request so it can negotiate
			// Markdown, add `Vary: Accept`, return Markdown 404 bodies, and
			// keep byte ranges working for the hero film. Static files are
			// still served through the ASSETS binding.
			runWorkerFirst: true,
		},
		env: {
			ASSETS: bindings.assets(),
		},
	},
});
