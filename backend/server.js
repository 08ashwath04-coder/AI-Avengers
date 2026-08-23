const express = require("express");
const cors = require("cors");

const askRoutes = require("./routes/ask");
const uploadRoutes = require("./routes/upload");

const app = express();

const PORT = Number(process.env.PORT) || 5000;

// Middleware
app.use(cors({ origin: process.env.FRONTEND_ORIGIN || "http://localhost:5173" }));
app.use(express.json());

// Routes
app.use("/api", askRoutes);
app.use("/api", uploadRoutes);

// Home
app.get("/", (req, res) => {
    res.json({
        message: "Second Brain AI Backend is Running"
    });
});

// Health check
app.get("/health", (req, res) => {
    res.json({
        status: "healthy"
    });
});

// Start server
app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
