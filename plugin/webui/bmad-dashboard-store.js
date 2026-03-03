import { createStore } from "/js/AlpineStore.js";

export const store = createStore("bmadDashboard", {
    loading: false,
    error: "",
    data: null,
    lastRefresh: null,

    async onOpen() {
        await this.refresh();
    },

    cleanup() {
        // nothing to clean up
    },

    async refresh() {
        this.loading = true;
        this.error = "";
        try {
            const resp = await fetch("/api/plugins/bmad/_bmad_status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})
            });
            if (!resp.ok) throw new Error("HTTP " + resp.status);
            const json = await resp.json();
            if (!json.success) throw new Error(json.error || "Unknown error");
            this.data = json;
            this.lastRefresh = new Date().toLocaleTimeString();
        } catch (e) {
            this.error = e.message;
        } finally {
            this.loading = false;
        }
    },

    get agentHealthPercent() {
        if (!this.data) return 0;
        const a = this.data.agents;
        return a.total > 0 ? Math.round((a.healthy.length / a.total) * 100) : 0;
    },

    get testStatusClass() {
        if (!this.data) return "neutral";
        const t = this.data.tests;
        if (t.status === "ok" && t.failing === 0) return "ok";
        if (t.status === "ok" && t.failing > 0) return "warn";
        return "neutral";
    },

    get phaseLabel() {
        if (!this.data) return "...";
        return this.data.state.phase;
    }
});
