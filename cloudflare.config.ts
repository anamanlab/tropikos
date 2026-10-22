import { defineConfig } from "cf/config";

export default defineConfig({
	worker: {
		name: "tropikos-arquitetos",
		compatibilityDate: "2026-10-22",
		assets: {
			htmlHandling: "auto-trailing-slash",
			notFoundHandling: "404-page",
		},
	},
});
