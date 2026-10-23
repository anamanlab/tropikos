import { bindings, defineConfig } from "cf/config";

export default defineConfig({
	worker: {
		name: "tropikos-arquitetos",
		compatibilityDate: "2026-10-22",
		entrypoint: "./src/worker.ts",
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "404-page",
			// Run the Worker first for media so it can serve byte ranges.
			// All other requests are still served directly as static assets.
			runWorkerFirst: ["/media/*"],
		},
		env: {
			ASSETS: bindings.assets(),
		},
	},
});
