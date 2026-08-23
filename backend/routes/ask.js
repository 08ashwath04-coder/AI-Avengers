const express = require("express");
const router = express.Router();

const AI_SEARCH_URL = process.env.AI_SEARCH_URL || "http://127.0.0.1:8000";

router.post("/ask", async (req, res) => {

    const { question } = req.body;

    if (!question) {
        return res.status(400).json({
            error: "Question is required"
        });
    }

    try {
        const response = await fetch(`${AI_SEARCH_URL}/ask`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ question })
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            return res.status(response.status).json({
                error: data.detail || "AI Search could not answer the question."
            });
        }

        res.json({ question, ...data });
    } catch (error) {
        res.status(503).json({
            error: "AI Search service is unavailable. Start it on port 8000 and try again."
        });
    }
});

module.exports = router;
