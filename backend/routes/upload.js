const express = require("express");
const multer = require("multer");
const path = require("path");
const fs = require("fs");
const { execFileSync } = require("child_process");

const router = express.Router();
// Keep incoming files in the document-processing module's input folder so
// they are available to its extraction/chunking workflow.
const uploadDirectory = path.join(__dirname, "..", "..", "document-processing", "input");
const processorPath = path.join(__dirname, "..", "..", "document-processing", "src", "ingest.py");
fs.mkdirSync(uploadDirectory, { recursive: true });

const supportedExtensions = new Set([".pdf", ".docx", ".txt", ".csv", ".xls", ".xlsx"]);

const storage = multer.diskStorage({

    destination: (req, file, cb) => {
        cb(null, uploadDirectory);
    },

    filename: (req, file, cb) => {

        const uniqueName =
            Date.now() + "-" + file.originalname;

        cb(null, uniqueName);
    }
});

const upload = multer({
    storage: storage,
    limits: { fileSize: 50 * 1024 * 1024 },
    fileFilter: (req, file, cb) => {
        if (!supportedExtensions.has(path.extname(file.originalname).toLowerCase())) {
            return cb(new Error("Unsupported file type. Please upload PDF, DOCX, TXT, CSV, XLS, or XLSX."));
        }
        cb(null, true);
    }
});

router.post("/upload", (req, res) => {
    upload.single("file")(req, res, (uploadError) => {
        if (uploadError) {
            return res.status(400).json({ error: uploadError.message });
        }

        if (!req.file) {
            return res.status(400).json({ error: "No file uploaded" });
        }

        try {
            const output = execFileSync("python", [processorPath, req.file.path], {
                encoding: "utf8",
                timeout: 30000,
                windowsHide: true
            });
            const result = JSON.parse(output.trim());
            if (result.error) throw new Error(result.error);
            res.json({
                message: "File uploaded and processed successfully",
                filename: req.file.filename,
                originalName: req.file.originalname,
                records: result.records
            });
        } catch (error) {
            fs.unlink(req.file.path, () => {});
            res.status(422).json({ error: "Unable to process this file. Please try another file." });
        }
    });
});

module.exports = router;
