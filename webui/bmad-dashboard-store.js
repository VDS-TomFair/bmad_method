import { createStore } from "/js/AlpineStore.js";
import { toastFrontendError } from "/components/notifications/notification-store.js";

export const store = createStore("bmadDashboard", {
    loading: false,
    data: null,
    lastRefresh: null,
    error: "",

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
            // Send ctxid so the backend resolves state for THIS active project
            const ctxid = globalThis.getContext ? globalThis.getContext() : "";
            const resp = await fetch("/api/plugins/bmad_method/_bmad_status", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ ctxid })
            });
            if (!resp.ok) throw new Error("HTTP " + resp.status);
            const json = await resp.json();
            if (!json.success) throw new Error(json.error || "Unknown error");
            this.data = json;
            this.lastRefresh = new Date().toLocaleTimeString();
        } catch (e) {
            toastFrontendError(e.message, "BMAD Method");
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
