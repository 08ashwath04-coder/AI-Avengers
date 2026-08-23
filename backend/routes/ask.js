const express = require("express");
const router = express.Router();

router.post("/ask", (req, res) => {

    const { question } = req.body;

    if (!question) {
        return res.status(400).json({
            error: "Question is required"
        });
    }

    // Temporary answer
    // Later this will connect to Member 3's AI/Search module.

    const answer = "Students must maintain 75% attendance.";
    const source = "College Handbook";

    res.json({
        question: question,
        answer: answer,
        source: source
    });
});

module.exports = router;